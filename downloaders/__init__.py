"""Media extraction adapters."""
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp

ALLOWED_SCHEMES = {"http", "https"}

def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Provide an absolute http/https URL without embedded credentials")
    return parsed

def inspect_media(url):
    validate_url(url)
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    fields = ("id", "title", "description", "duration", "uploader", "uploader_id", "webpage_url", "extractor", "upload_date", "view_count", "like_count", "thumbnail")
    return {key: info.get(key) for key in fields}

def download(url, output_dir="downloads", media_format="best"):
    validate_url(url)
    target = Path(output_dir).expanduser().resolve(); target.mkdir(parents=True, exist_ok=True)
    opts = {"outtmpl": str(target / "%(extractor)s" / "%(uploader)s" / "%(title).180B [%(id)s].%(ext)s"), "noplaylist": True, "restrictfilenames": True, "quiet": True, "no_warnings": True, "ignoreerrors": False, "format": "bestaudio/best" if media_format == "audio" else "bestvideo*+bestaudio/best"}
    if media_format == "audio": opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True); path = ydl.prepare_filename(info) if info else None
    return {"id": info.get("id"), "title": info.get("title"), "extractor": info.get("extractor"), "filepath": path, "format": media_format}

def gallery_download(url, output_dir="downloads"):
    validate_url(url)
    if not shutil.which("gallery-dl"): raise RuntimeError("gallery-dl is not installed; see https://github.com/mikf/gallery-dl")
    destination = str(Path(output_dir).expanduser().resolve())
    proc = subprocess.run(["gallery-dl", "--dest", destination, url], capture_output=True, text=True, timeout=180)
    if proc.returncode: raise RuntimeError(proc.stderr[-2000:] or "gallery-dl failed")
    return {"stdout": proc.stdout[-4000:], "output_dir": destination}
