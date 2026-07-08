from __future__ import annotations

import html
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.query import events_query
DEFAULT_DB_PATH = APP_ROOT / "data" / "zhuan_os.db"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class DashboardResponse:
    def __init__(self, status: int, body: str, content_type: str = "text/html; charset=utf-8") -> None:
        self.status = status
        self.body = body
        self.content_type = content_type


def _bool_param(params: dict[str, list[str]], name: str) -> bool:
    value = params.get(name, [""])[0].lower()
    return value in {"1", "true", "yes", "on"}


def _text_param(params: dict[str, list[str]], name: str) -> str:
    return params.get(name, [""])[0].strip()


def _event_text(event: dict) -> str:
    payload = event.get("payload") or {}
    if isinstance(payload, dict):
        for key in ("text", "content", "message", "title"):
            value = payload.get(key)
            if value:
                return str(value)
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return str(payload)


def _render_events(title: str, events: list[dict]) -> str:
    rows = []
    for event in events:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(event.get('occurred_at', '')))}</td>"
            f"<td>{html.escape(str(event.get('type', '')))}</td>"
            f"<td>{html.escape(str(event.get('source', '')))}</td>"
            f"<td>{html.escape(_event_text(event))}</td>"
            "</tr>"
        )
    if not rows:
        table = '<p class="empty">No events found.</p>'
    else:
        table = (
            "<table>"
            "<thead><tr><th>Occurred</th><th>Type</th><th>Source</th><th>Payload</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody>"
            "</table>"
        )
    return f"<section><h2>{html.escape(title)}</h2>{table}</section>"


def _render_page(
    *,
    db_path: Path,
    include_test: bool,
    event_type: str,
    keyword: str,
    timezone: str,
    recent_events: list[dict],
    today_events: list[dict],
    type_events: list[dict],
    search_results: list[dict],
    error: str | None = None,
) -> str:
    checked = " checked" if include_test else ""
    error_html = f'<div class="notice">{html.escape(error)} This dashboard is read-only.</div>' if error else ""
    type_section = _render_events(f"Event Type Filter: {event_type}", type_events) if event_type else ""
    search_section = _render_events(f"Keyword Search: {keyword}", search_results) if keyword else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Zhuan OS Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #171717; background: #f7f7f4; }}
    header {{ margin-bottom: 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 6px; }}
    h2 {{ font-size: 18px; margin: 24px 0 10px; }}
    .meta, label {{ color: #555; font-size: 14px; }}
    form {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: end; padding: 12px 0; }}
    input, select, button {{ font: inherit; padding: 7px 9px; border: 1px solid #bbb; border-radius: 4px; background: white; }}
    button {{ cursor: pointer; background: #222; color: white; border-color: #222; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; vertical-align: top; border-bottom: 1px solid #ddd; padding: 8px; font-size: 14px; }}
    th {{ background: #ecece7; }}
    .notice {{ padding: 10px 12px; background: #fff3cd; border: 1px solid #e2c76c; margin: 12px 0; }}
    .empty {{ color: #666; background: white; padding: 10px; border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <header>
    <h1>Zhuan OS Dashboard</h1>
    <div class="meta">SQLite: {html.escape(str(db_path))}</div>
  </header>
  {error_html}
  <form method="get" action="/">
    <label>Type<br>
      <select name="type">
        <option value="">All</option>
        {''.join(f'<option value="{html.escape(t)}"{' selected' if t == event_type else ''}>{html.escape(t)}</option>' for t in ['quick_capture', 'study_log', 'decision_log', 'mistake_log', 'principle_log', 'review_log'])}
      </select>
    </label>
    <label>Keyword<br><input name="search" value="{html.escape(keyword)}"></label>
    <label>Timezone<br><input name="timezone" value="{html.escape(timezone)}"></label>
    <label><input type="checkbox" name="include_test" value="1"{checked}> Include test events</label>
    <button type="submit">Apply</button>
  </form>
  {_render_events('Recent Events', recent_events)}
  {_render_events('Today Events', today_events)}
  {type_section}
  {search_section}
</body>
</html>"""


def build_response(raw_path: str, db_path: str | Path = DEFAULT_DB_PATH) -> DashboardResponse:
    parsed = urlparse(raw_path)
    params = parse_qs(parsed.query)
    include_test = _bool_param(params, "include_test")
    event_type = _text_param(params, "type")
    keyword = _text_param(params, "search")
    timezone = _text_param(params, "timezone") or "+08:00"
    db = Path(db_path)

    recent_events: list[dict] = []
    today_events: list[dict] = []
    type_events: list[dict] = []
    search_results: list[dict] = []
    error: str | None = None

    try:
        recent_events = events_query.get_recent_events(db, limit=20, include_test=include_test)
        today_events = events_query.get_today_events(db, timezone=timezone, include_test=include_test)
        if event_type:
            type_events = events_query.get_events_by_type(db, event_type, limit=50, include_test=include_test)
        if keyword:
            search_results = events_query.search_events(db, keyword, limit=50, include_test=include_test)
    except FileNotFoundError as exc:
        error = str(exc)
    except Exception as exc:  # Keep the read-only dashboard reachable when the local index is invalid.
        error = f"Unable to read SQLite index: {exc}"

    body = _render_page(
        db_path=db,
        include_test=include_test,
        event_type=event_type,
        keyword=keyword,
        timezone=timezone,
        recent_events=recent_events,
        today_events=today_events,
        type_events=type_events,
        search_results=search_results,
        error=error,
    )
    return DashboardResponse(200, body)


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        response = build_response(self.path)
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response.body.encode("utf-8"))

    def do_POST(self) -> None:
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        return


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"Zhuan OS Dashboard: http://{host}:{port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    run()


