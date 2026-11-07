import argparse
import json
import sys
from .downloaders import download, inspect_media
from .analyzers import analyze
from .publishers import schedule, publish_due

def emit(value, stream=sys.stdout):
    print(json.dumps(value, ensure_ascii=False, default=str), file=stream)

def main():
    p = argparse.ArgumentParser(prog="socialsuite")
    sub = p.add_subparsers(dest="command", required=True)
    d = sub.add_parser("download"); d.add_argument("url"); d.add_argument("--output", default="downloads"); d.add_argument("--format", choices=["best", "audio"], default="best"); d.add_argument("--metadata-only", action="store_true")
    a = sub.add_parser("analyze"); a.add_argument("url"); a.add_argument("--profile", action="store_true"); a.add_argument("--social-analyzer", action="store_true")
    s = sub.add_parser("schedule"); s.add_argument("--text", required=True); s.add_argument("--at", required=True, dest="scheduled_at"); s.add_argument("--media")
    q = sub.add_parser("publish-due"); q.add_argument("--limit", type=int, default=20)
    args = p.parse_args()
    try:
        if args.command == "download": result = inspect_media(args.url) if args.metadata_only else download(args.url, args.output, args.format)
        elif args.command == "analyze": result = analyze(args.url, args.profile, args.social_analyzer)
        elif args.command == "schedule": result = schedule(args.text, args.scheduled_at, args.media)
        else: result = publish_due(args.limit)
        emit({"ok": True, "result": result})
    except Exception as exc:
        emit({"ok": False, "error": str(exc)}, sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
