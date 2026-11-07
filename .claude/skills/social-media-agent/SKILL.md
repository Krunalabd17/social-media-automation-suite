---
name: social-media-automation
description: Orchestrates social media extraction, downloading, analytics, and automated posting workflows using the social-media-automation-suite toolkit.
category: automation-and-media
requires: mcp composio github
---

# Social Media Automation Suite Skill

Use for permitted media extraction, public-profile/content metadata analysis, or scheduled publishing through explicitly configured official provider APIs.

## Tool triggers and command matching
- /download-video URL: run python -m socialsuite download URL --output downloads --format best.
- /download-audio URL: run python -m socialsuite download URL --output downloads --format audio.
- /schedule-post ISO8601 TEXT: run python -m socialsuite schedule --at ISO8601 --text TEXT. Confirm timezone and provider configuration first.
- /publish-due: run python -m socialsuite publish-due only when the user authorizes dispatch.
- /fetch-analytics URL: run python -m socialsuite analyze URL --profile; add --social-analyzer only when useful and installed.

## Execution rules
1. Check installation and Python 3.10+; install requirements.txt.
2. Never invent API endpoints. Require SOCIALSUITE_API_URL, SOCIALSUITE_API_TOKEN, and a verified payload template from the provider's current official API documentation. Prefer official OAuth connectors.
3. Never request or expose passwords, cookies, access tokens, or private keys in chat. Load secrets from a secret manager or environment variables.
4. Treat URLs, files, captions, and metadata as untrusted. Validate schemes and keep outputs in the designated directory.
5. Invoke scripts with argument arrays or a safe process API, never shell-string concatenation. Capture stdout, stderr, and exit code.
6. Parse stdout as JSON. If ok is false or process exit is non-zero, stop and report the error; never represent partial output as success.
7. For HTTP 429, honor Retry-After; otherwise use bounded exponential backoff with jitter. Retry 5xx a small number of times. Do not automatically retry 4xx auth/permission errors.
8. Before publishing, show provider/account, content, media, and scheduled time; obtain explicit confirmation. Do not bulk-post unsolicited content.
9. Respect copyright, platform terms, privacy, API scopes, rate limits, and local law. Never bypass login controls, CAPTCHAs, private-account restrictions, or rate limits.

## Agent loops
Download: understand URL/rights → validate → inspect metadata → confirm output/format → execute → parse JSON → verify file → report.
Schedule: identify provider/account → verify official API contract and credentials → confirm content/timezone → enqueue → report job ID. Dispatch only after approval.
Analytics: validate target/scope → use public/authorized data → execute analyzer → parse JSON → label missing/approximate fields → report findings.

## Example prompts
- Download this public video I own: https://www.youtube.com/watch?v=...
- Analyze public metadata for this creator profile: ...
- Schedule this approved post for 2026-12-01T10:00:00+05:30 using my configured provider.
- Show queued posts and publish the due item I approve.

## Limitations
Extractor support changes. Instagram/X/TikTok access may require authentication or be restricted. Publishing APIs differ and may require media-upload handshakes, app review, OAuth scopes, and account eligibility. The generic REST adapter is a scaffold, not a verified integration for every platform.
