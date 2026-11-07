"""Metadata analyzers with optional upstream integrations."""
import importlib.util
import shutil
import subprocess
from .downloaders import inspect_media, validate_url

def analyze(url, profile=False, social_analyzer=False):
    validate_url(url); result = {"media": inspect_media(url)}
    if profile:
        result["profile_note"] = "Generic profile extraction is not guaranteed. Use an approved provider API or optional Instaloader for eligible public Instagram profiles."
        if "instagram.com" in url and importlib.util.find_spec("instaloader"):
            import instaloader
            loader = instaloader.Instaloader(quiet=True, download_pictures=False, download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False)
            username = url.rstrip("/").split("/")[-1]
            profile_obj = instaloader.Profile.from_username(loader.context, username)
            result["profile"] = {"username": profile_obj.username, "full_name": profile_obj.full_name, "biography": profile_obj.biography, "followers": profile_obj.followers, "followees": profile_obj.followees, "media_count": profile_obj.mediacount, "is_private": profile_obj.is_private}
    if social_analyzer:
        if not shutil.which("social-analyzer"): result["social_analyzer"] = {"available": False, "install": "https://github.com/qeeqbox/social-analyzer"}
        else:
            handle = url.rstrip("/").split("/")[-1].lstrip("@")
            proc = subprocess.run(["social-analyzer", "--username", handle, "--metadata"], capture_output=True, text=True, timeout=120)
            result["social_analyzer"] = {"returncode": proc.returncode, "stdout": proc.stdout[-8000:], "stderr": proc.stderr[-2000:]}
    return result
