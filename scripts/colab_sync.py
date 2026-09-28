#!/usr/bin/env python3
"""
Colab Sync Utility
==================
Syncs local Jupyter notebooks with Google Colab (Google Drive) using service account credentials.

Usage:
    python scripts/colab_sync.py push
    python scripts/colab_sync.py pull
    python scripts/colab_sync.py status
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

DEFAULT_CREDS_PATH = Path("/Users/nathy/Downloads/cursor-sheets-mcp-508421-8d7566fa6119.json")
DEFAULT_FILE_ID = "1o5Np_h_KzrH2Sc7gyo3z5JPrNVPNcaRA"
DEFAULT_LOCAL_NB = Path(__file__).resolve().parent.parent / "notebooks" / "Backdoor_Probe_Detectability_Study.ipynb"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service(creds_path: Path):
    if not creds_path.exists():
        raise FileNotFoundError(f"Credentials file not found at: {creds_path}")
    creds = service_account.Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def check_status(service, file_id: str):
    file_meta = service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, modifiedTime, shared, capabilities"
    ).execute()
    print(f"✅ Google Colab Notebook Status:")
    print(f"  • Name: {file_meta.get('name')}")
    print(f"  • File ID: {file_meta.get('id')}")
    print(f"  • Modified Time: {file_meta.get('modifiedTime')}")
    print(f"  • Can Edit: {file_meta.get('capabilities', {}).get('canModifyContent', False)}")
    print(f"  • Can Download: {file_meta.get('capabilities', {}).get('canDownload', False)}")
    return file_meta


def pull_notebook(service, file_id: str, local_path: Path):
    print(f"📥 Pulling notebook from Colab (Drive ID: {file_id}) -> {local_path}...")
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    
    fh.seek(0)
    content = fh.read().decode("utf-8")
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Successfully pulled notebook to {local_path}")


def push_notebook(service, file_id: str, local_path: Path):
    if not local_path.exists():
        raise FileNotFoundError(f"Local notebook not found at: {local_path}")
    print(f"📤 Pushing notebook {local_path} -> Colab (Drive ID: {file_id})...")
    media = MediaFileUpload(str(local_path), mimetype="application/vnd.google.colaboratory", resumable=True)
    updated = service.files().update(fileId=file_id, media_body=media).execute()
    print(f"✅ Successfully pushed and updated Colab notebook (ID: {updated.get('id')})")


def main():
    parser = argparse.ArgumentParser(description="Sync notebooks with Google Colab")
    parser.add_argument("action", choices=["status", "pull", "push"], help="Action to perform")
    parser.add_argument("--file-id", default=DEFAULT_FILE_ID, help="Google Drive File ID")
    parser.add_argument("--creds", default=str(DEFAULT_CREDS_PATH), help="Path to Google service account JSON")
    parser.add_argument("--local-nb", default=str(DEFAULT_LOCAL_NB), help="Path to local .ipynb file")

    args = parser.parse_args()
    service = get_drive_service(Path(args.creds))

    if args.action == "status":
        check_status(service, args.file_id)
    elif args.action == "pull":
        pull_notebook(service, args.file_id, Path(args.local_nb))
    elif args.action == "push":
        push_notebook(service, args.file_id, Path(args.local_nb))


if __name__ == "__main__":
    main()
