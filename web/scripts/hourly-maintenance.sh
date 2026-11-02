#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WEB="$ROOT/web"
PORT="${PORT:-3000}"
LOG="${LOG:-/tmp/htmls-web-maintenance.log}"
FORCE_RESTART="${FORCE_RESTART:-0}"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" | tee -a "$LOG"
}

if command -v pnpm >/dev/null 2>&1; then
  PNPM="$(command -v pnpm)"
elif [ -x "$HOME/.local/node/bin/pnpm" ]; then
  PNPM="$HOME/.local/node/bin/pnpm"
else
  log "ERROR pnpm not found"
  exit 1
fi

log "maintenance start root=$ROOT port=$PORT force_restart=$FORCE_RESTART"

killed=0
while IFS= read -r pid; do
  [ -z "$pid" ] && continue
  cwd="$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | head -1)"
  case "$cwd" in
    "$ROOT"|"$ROOT"/*)
      if kill "$pid" 2>/dev/null; then
        killed=$((killed + 1))
        log "killed http.server pid=$pid cwd=$cwd"
      fi
      ;;
  esac
done < <(pgrep -f 'http\.server' 2>/dev/null || true)
log "stray http.server killed=$killed"

healthy=0
if curl -fsS --max-time 5 "http://127.0.0.1:${PORT}/api/pages" >/dev/null 2>&1; then
  healthy=1
fi

if [ "$healthy" -eq 1 ] && [ "$FORCE_RESTART" != "1" ]; then
  log "web healthy on port $PORT; no restart"
  exit 0
fi

listener_pids="$(lsof -nP -iTCP:${PORT} -sTCP:LISTEN -t 2>/dev/null || true)"
if [ -n "$listener_pids" ]; then
  log "stopping listener pids=$listener_pids"
  kill $listener_pids 2>/dev/null || true
  sleep 1
fi

cd "$WEB"

if [ ! -d .next ]; then
  log "build missing; running pnpm build"
  "$PNPM" build >>"$LOG" 2>&1
fi

log "starting pnpm start"
nohup "$PNPM" start >>/tmp/htmls-web-prod.log 2>&1 &
start_pid=$!
log "started pid=$start_pid"

for attempt in $(seq 1 20); do
  if curl -fsS --max-time 2 "http://127.0.0.1:${PORT}/api/pages" >/dev/null 2>&1; then
    log "web healthy after attempt=$attempt"
    exit 0
  fi
  sleep 0.5
done

log "ERROR web did not become healthy"
exit 1
