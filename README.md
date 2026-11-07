# Social Media Automation Suite

A modular Python toolkit for media extraction, metadata analysis, and configurable publishing workflows. Original integration code; no upstream source is copied.

## Capabilities
- Download: yt-dlp extraction for supported public URLs, including YouTube, TikTok, X, and eligible Instagram URLs; optional gallery-dl adapter.
- Publish: configurable REST publisher and SQLite scheduling queue. This is a transport scaffold, not a universal social API.
- Analyze: URL metadata via yt-dlp, optional Instaloader, and optional Social Analyzer CLI.
- JSON output, explicit exit codes, environment-based secrets, and Claude/Composio skill.

## Requirements and install
Python 3.10+, yt-dlp, requests; ffmpeg recommended. gallery-dl, Instaloader, and Social Analyzer are optional.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Windows PowerShell: .venv\Scripts\Activate.ps1

## Quick start
    python -m socialsuite download "https://www.youtube.com/watch?v=VIDEO_ID" --output ./downloads --format best
    python -m socialsuite download "https://www.tiktok.com/@creator/video/ID" --output ./downloads --format best
    python -m socialsuite download "https://x.com/user/status/ID" --output ./downloads --format best
    python -m socialsuite analyze "https://www.youtube.com/watch?v=VIDEO_ID"

Publishing requires a verified endpoint/payload contract from the provider's current official API documentation:

    export SOCIALSUITE_API_URL="https://api.example.com/v1/posts"
    export SOCIALSUITE_API_TOKEN="replace-me"
    export SOCIALSUITE_PAYLOAD_TEMPLATE='{"text":"{{text}}","scheduled_at":"{{scheduled_at}}"}'
    python -m socialsuite schedule --text "Hello world" --at "2026-12-01T10:00:00Z"
    python -m socialsuite publish-due

Jobs are stored in socialsuite.db. publish-due dispatches only when explicitly invoked; use cron/systemd/Task Scheduler for recurring dispatch.

## CLI
- download URL [--output DIR] [--format best|audio] [--metadata-only]
- analyze URL [--profile] [--social-analyzer]
- schedule --text TEXT --at ISO8601 [--media PATH]
- publish-due [--limit N]

## Ten reference repositories: capabilities and entry points

| Repository | Capability and representative invocation/API pattern | Integrated design |
|---|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | CLI: yt-dlp URL; Python: YoutubeDL(opts).extract_info(URL, download=True) | Primary downloader and metadata extractor |
| [Postiz](https://github.com/gitroomhq/postiz-app) | Self-hosted multi-platform scheduler; use its documented public API routes and connected-channel publishing flow (routes/auth vary by release) | Queue-based scheduling and provider adapter boundary |
| [Social Analyzer](https://github.com/qeeqbox/social-analyzer) | CLI: social-analyzer --username HANDLE --metadata; API/web modes are also available | Optional analyzer CLI adapter |
| [Instaloader](https://github.com/instaloader/instaloader) | CLI: instaloader PROFILE; Python: Profile.from_username(context, USERNAME) | Optional public Instagram profile metadata |
| [gallery-dl](https://github.com/mikf/gallery-dl) | CLI: gallery-dl URL; configuration supports per-extractor options | Optional gallery/image extraction adapter |
| [snscrape](https://github.com/JustAnotherArchivist/snscrape) | CLI pattern: snscrape --jsonl twitter-user HANDLE; supports profile/search scraper modules | Normalized social-post metadata design; upstream maintenance/compatibility should be checked |
| [twscrape](https://github.com/vladkens/twscrape) | Python: API(); await api.search("query"); CLI includes search/user commands depending on release | Reference for X-specific collection; no rotation or limit evasion |
| [MeTube](https://github.com/alexta69/metube) | Self-hosted yt-dlp web UI; HTTP job submission/queue endpoints are part of its app interface (consult current README/API before integration) | Job lifecycle and queue pattern |
| [instagrapi](https://github.com/subzeroid/instagrapi) | Python: Client(); user_info_by_username(USERNAME); media_pk_from_url(URL) | Provider-specific API boundary only; approved access only |
| [Seal](https://github.com/JunkFood02/Seal) | Android UI wrapping yt-dlp; user selects URL/format in app; no general-purpose server API | Format selection and downloader UX patterns |

The invocation patterns are representative upstream entry points, not guarantees of current behavior. Repository discovery snapshot: 2026-11-07. Check upstream docs, API versions, licenses, and platform rules before relying on them.

## Safety and security
Use only content you own, have permission to access, or are legally entitled to process. Respect copyright, platform terms, privacy, access controls, quotas, and local law. No session theft, CAPTCHA bypass, stealth fingerprinting, private-account scraping, or rate-limit evasion. Upstream extractor support does not grant permission. Publishing requires official API credentials/scopes and may require media-upload handshakes, app review, and eligible accounts.

Never commit tokens, cookies, sessions, or passwords. Prefer official OAuth and least-privilege scopes. Treat downloaded media and metadata as untrusted; restrict output paths and sandbox untrusted URLs. Add consent, quota, and audit controls before production.

## Tests
    python -m unittest discover -s tests -v

MIT applies to this integration code only. Upstream tools retain their own licenses and terms.
