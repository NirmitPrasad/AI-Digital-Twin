"""
Run this ONCE from your backend/ folder to authorise Google Calendar access.

Steps:
  1. Go to https://console.cloud.google.com
  2. Create a new project (or use existing)
  3. Enable "Google Calendar API"
  4. Go to APIs & Services → Credentials
  5. Click "Create Credentials" → OAuth 2.0 Client IDs
  6. Application type: Desktop app → Create
  7. Download the JSON file → save it as  backend/google_credentials.json
  8. Run:  python google_auth_setup.py
  9. A browser window opens → sign in with nirmitprasad@gmail.com → Allow
 10. token.json is created in backend/ — you're done!

After this, every event you add in the Calendar tab will automatically
appear in your Google Calendar.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES       = ["https://www.googleapis.com/auth/calendar"]
CREDS_FILE   = "google_credentials.json"
TOKEN_FILE   = "token.json"

def main():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print(f"\n❌ '{CREDS_FILE}' not found!")
                print("Download it from Google Cloud Console → APIs & Services → Credentials")
                print("Save it as 'google_credentials.json' in your backend/ folder.\n")
                return
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    print("\n✅ Google Calendar authorised successfully!")
    print(f"   token.json saved to: {os.path.abspath(TOKEN_FILE)}")
    print("\n   Restart your backend (uvicorn main:app --reload)")
    print("   Events added in the Calendar tab will now sync to Google Calendar.\n")

if __name__ == "__main__":
    main()