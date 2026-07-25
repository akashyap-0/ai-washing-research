"""Upload the local export directory to Google Drive via OAuth.

One-time setup:
  1. In Google Cloud Console, create/select a project, enable the Google
     Drive API, and create an OAuth client ID of type "Desktop app".
  2. Download its JSON and save it at config.GDRIVE_CREDENTIALS_PATH
     (default: ./credentials.json).
  3. The first run opens a browser. Sign in as advikkashyap1@gmail.com or
     ecfarmer12@gmail.com and grant access. The refresh token is cached at
     config.GDRIVE_TOKEN_PATH so later runs don't need the browser again.

Scope is drive.file: this app can only see/manage files and folders it
itself created, not the whole Drive.
"""
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import config

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_MIME = "application/vnd.google-apps.folder"


def _load_credentials():
    creds = None
    token_path = config.GDRIVE_TOKEN_PATH
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not os.path.exists(config.GDRIVE_CREDENTIALS_PATH):
            raise RuntimeError(
                f"GDRIVE_CREDENTIALS_PATH ('{config.GDRIVE_CREDENTIALS_PATH}') "
                "not found. Create an OAuth Desktop-app client in Google "
                "Cloud Console (with the Drive API enabled) and save its "
                "JSON there."
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            config.GDRIVE_CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    return creds


def get_service():
    return build("drive", "v3", credentials=_load_credentials())


def find_or_create_folder(service, name=None, parent_id=None):
    """Return the id of a Drive folder by name, creating it if absent."""
    name = name or config.GDRIVE_FOLDER_NAME
    query = f"name = '{name}' and mimeType = '{FOLDER_MIME}' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    resp = service.files().list(q=query, spaces="drive",
                                fields="files(id, name)").execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def _find_file(service, name, parent_id):
    query = f"name = '{name}' and '{parent_id}' in parents and trashed = false"
    resp = service.files().list(q=query, spaces="drive",
                                fields="files(id, name)").execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def upload_file(service, local_path, parent_id):
    """Create or update (by name) a file in `parent_id`. Returns the file id."""
    name = os.path.basename(local_path)
    media = MediaFileUpload(local_path, resumable=True)
    existing_id = _find_file(service, name, parent_id)
    if existing_id:
        return service.files().update(
            fileId=existing_id, media_body=media).execute()["id"]
    metadata = {"name": name, "parents": [parent_id]}
    return service.files().create(
        body=metadata, media_body=media, fields="id").execute()["id"]


def upload_export_dir(export_dir=None, folder_name=None):
    """Upload every file in export_dir into the named Drive folder.

    Returns (folder_id, [uploaded filenames]).
    """
    export_dir = export_dir or config.EXPORT_DIR
    service = get_service()
    folder_id = find_or_create_folder(service, name=folder_name)

    uploaded = []
    for fname in sorted(os.listdir(export_dir)):
        path = os.path.join(export_dir, fname)
        if not os.path.isfile(path):
            continue
        upload_file(service, path, folder_id)
        uploaded.append(fname)
    return folder_id, uploaded
