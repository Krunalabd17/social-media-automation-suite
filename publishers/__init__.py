"""Configurable REST publishing adapter and SQLite scheduler."""
import json
import os
import sqlite3
from datetime import datetime, timezone
import requests

def _db(): return sqlite3.connect(os.getenv("SOCIALSUITE_DB", "socialsuite.db"))
def _schema(con):
    con.execute("""CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, scheduled_at TEXT NOT NULL, media TEXT, status TEXT NOT NULL DEFAULT 'pending', response TEXT, created_at TEXT NOT NULL)""")
def _parse_time(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None: raise ValueError("scheduled_at must include a timezone")
    return dt.astimezone(timezone.utc).isoformat()
def schedule(text, scheduled_at, media=None):
    when = _parse_time(scheduled_at)
    with _db() as con:
        _schema(con)
        cur = con.execute("INSERT INTO jobs(text,scheduled_at,media,status,created_at) VALUES(?,?,?,'pending',?)", (text, when, media, datetime.now(timezone.utc).isoformat()))
        return {"job_id": cur.lastrowid, "scheduled_at": when, "status": "pending"}
def _publish(job):
    endpoint, token = os.getenv("SOCIALSUITE_API_URL"), os.getenv("SOCIALSUITE_API_TOKEN")
    template = os.getenv("SOCIALSUITE_PAYLOAD_TEMPLATE", '{"text":"{{text}}","scheduled_at":"{{scheduled_at}}"}')
    if not endpoint or not token: raise RuntimeError("SOCIALSUITE_API_URL and SOCIALSUITE_API_TOKEN are required")
    payload_text = template.replace("{{text}}", json.dumps(job["text"])[1:-1]).replace("{{scheduled_at}}", job["scheduled_at"]).replace("{{media_url}}", job.get("media") or "")
    response = requests.post(endpoint, json=json.loads(payload_text), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=30)
    if response.status_code == 429: raise RuntimeError("Provider rate limit (429); honor Retry-After before retrying")
    if response.status_code >= 500: raise RuntimeError(f"Provider temporary server error: {response.status_code}")
    response.raise_for_status()
    return {"status_code": response.status_code, "body": response.json() if response.content else {}}
def publish_due(limit=20):
    if not 1 <= limit <= 500: raise ValueError("limit must be between 1 and 500")
    now = datetime.now(timezone.utc).isoformat(); results = []
    with _db() as con:
        con.row_factory = sqlite3.Row; _schema(con)
        jobs = con.execute("SELECT * FROM jobs WHERE status='pending' AND scheduled_at<=? ORDER BY scheduled_at LIMIT ?", (now, limit)).fetchall()
        for row in jobs:
            job = dict(row)
            try:
                result = _publish(job); con.execute("UPDATE jobs SET status='published',response=? WHERE id=?", (json.dumps(result), job["id"]))
                results.append({"job_id": job["id"], "status": "published", "provider": result})
            except Exception as exc:
                con.execute("UPDATE jobs SET response=? WHERE id=?", (json.dumps({"error": str(exc)}), job["id"]))
                results.append({"job_id": job["id"], "status": "pending", "error": str(exc)})
    return {"processed": len(results), "jobs": results}
