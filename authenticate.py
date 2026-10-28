import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # run_local_server opens the browser automatically to authenticate
    creds = flow.run_local_server(port=8080, open_browser=True)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("SUCCESS: Google authentication complete and token saved permanently!")

if __name__ == "__main__":
    main()
