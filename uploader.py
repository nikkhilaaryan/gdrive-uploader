import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Authenticate and return Google Drive service."""
    creds = None
  
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
     
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

 
    return build('drive', 'v3', credentials=creds)

def file_upload(file_path):
    """Upload a single file to Google Drive."""
    service = authenticate_google_drive()
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f' File uploaded successfully. File ID: {file.get("id")}')


if __name__ == '__main__':
    file_to_upload = 'mml-book.pdf'  
    if os.path.exists(file_to_upload):
        file_upload(file_to_upload)
    else:
        print("File not found. Please check the file path.")
