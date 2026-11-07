# Social Media Automation Suite

A modular Python toolkit for media extraction, metadata analysis, and configurable publishing workflows. It combines stable interfaces inspired by established open-source projects; it does not bundle or copy their source code.

## Capabilities
- Download: yt-dlp-backed extraction for supported public URLs, including YouTube, TikTok, X, and eligible Instagram URLs; optional gallery-dl adapter.
- Publish: configurable REST publisher with provider-specific endpoint, payload, and authentication settings; SQLite scheduling queue.
- Analyze: URL metadata through yt-dlp, optional Instaloader, and optional Social Analyzer CLI.
- Automation-ready JSON output, explicit exit codes, environment-based secrets, and Claude/Composio skill.

## Important constraints
Use only content you own, have permission to access, or are legally entitled to process. Respect platform terms, copyright, privacy, access controls, rate limits, and applicable law. No login/session theft, CAPTCHA bypass, stealth fingerprinting, private-account scraping, or limit evasion is implemented. Upstream extractor support does not grant permission. Use official platform APIs and approved app permissions for publishing. Provider quotas, scopes, media upload steps, and scheduling semantics vary.

## Requirements
- Python 3.10+
- yt-dlp (required)
- requests (required)
- ffmpeg recommended for audio conversion/merging
- gallery-dl, Instaloader, Social Analyzer optional

Install:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Windows PowerShell activation: .venv\Scripts\Activate.ps1

## Quick start
    python -m socialsuite download "https://www.youtube.com/watch?v=VIDEO_ID" --output ./downloads --format best
    python -m socialsuite download "https://www.tiktok.com/@creator/video/ID" --output ./downloads --format best
    python -m socialsuite download "https://x.com/user/status/ID" --output ./downloads --format best
    python -m socialsuite analyze "https://www.youtube.com/watch?v=VIDEO_ID"

Publishing requires an API endpoint and payload contract verified against the selected provider's current official documentation:
    export SOCIALSUITE_API_URL="https://api.example.com/v1/posts"
    export SOCIALSUITE_API_TOKEN="replace-me"
    export SOCIALSUITE_PAYLOAD_TEMPLATE='{"text":"{{text}}","scheduled_at":"{{scheduled_at}}"}'
    python -m socialsuite schedule --text "Hello world" --at "2026-12-01T10:00:00Z"
    python -m socialsuite publish-due

Queued jobs are stored in socialsuite.db. publish-due dispatches only when explicitly run; schedule a cron/systemd/Task Scheduler job if recurring dispatch is desired.

## CLI
- download URL [--output DIR] [--format best|audio] [--metadata-only]
- analyze URL [--profile] [--social-analyzer]
- schedule --text TEXT --at ISO8601 [--media PATH]
- publish-due [--limit N]

Commands print JSON to stdout. Errors print a JSON error object to stderr and return non-zero.

## Reference repositories and integration map

| Repository | Capabilities / invocation pattern | Integrated design |
|---|---|---|
| https://github.com/yt-dlp/yt-dlp | Video/audio extraction; CLI: yt-dlp URL; Python YoutubeDL API | Primary downloader and metadata extraction |
| https://github.com/gitroomhq/postiz-app | Multi-channel calendar and publishing application | Queue-based scheduler and provider adapter boundary |
| https://github.com/qeeqbox/social-analyzer | Username/profile discovery; CLI: social-analyzer --username HANDLE --metadata | Optional analyzer CLI adapter |
| https://github.com/instaloader/instaloader | Instagram public profile/post metadata; CLI: instaloader PROFILE | Optional Instaloader profile metadata adapter |
| https://github.com/mikf/gallery-dl | Image/gallery extraction; CLI: gallery-dl URL | Optional gallery downloader adapter |
| https://github.com/JustAnotherArchivist/snscrape | Social network search/profile scraping; CLI historically: snscrape twitter-user HANDLE | Normalized metadata design reference; verify maintenance and current platform compatibility |
| https://github.com/vladkens/twscrape | X search/profile collection; Python API and CLI | Reference for provider-specific collection; no rotation/limit evasion |
| https://github.com/alexta69/metube | Self-hosted yt-dlp queue/web UI | Job lifecycle and queue pattern |
| https://github.com/subzeroid/instagrapi | Instagram client API wrapper; Python client methods | Provider boundary only; use approved access |
| https://github.com/JunkFood02/Seal | Android downloader UX built around yt-dlp | Format selection and extraction UX patterns |

The API/CLI patterns above are representative entry points, not a guarantee of current behavior. Repository discovery snapshot: 2026-11-07. Check upstream documentation and licensing before adopting dependencies.

## Security
Never commit API tokens, cookies, sessions, or passwords. Prefer official OAuth and least-privilege scopes. Treat media and metadata as untrusted. Restrict output paths and sandbox untrusted URLs. Add consent, quota, and audit controls before production deployment.

## Tests
    python -m unittest discover -s tests -v

MIT license applies to this integration code only. Upstream tools retain their own licenses and terms.
