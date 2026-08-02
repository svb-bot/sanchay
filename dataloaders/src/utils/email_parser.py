import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    TOKEN_FILE_PATH = os.path.join(os.getcwd(), "data", "token.json")
    CREDENTIALS_PATH = os.path.join(os.getcwd(), "data", "credentials.json")
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service

def save_processed_email_ids(processed_ids):
    processed_emails_file_path = os.path.join(os.getcwd(), "data", "processed_emails.txt")
    with open(processed_emails_file_path, "a") as f:
        for msg_id in processed_ids:
            f.write(f"{msg_id}\n")

# Clear Processed Emails
def clear_processed_emails(service):
    processed_emails_file_path = os.path.join(os.getcwd(), "data", "processed_emails.txt")
    if not os.path.exists(processed_emails_file_path):
        print(f"Processed emails file does not exist: {processed_emails_file_path}")
        return
    with open(processed_emails_file_path, "r") as f:
        processed_ids = f.read().splitlines()

    for msg_id in processed_ids:
        try:
            service.users().messages().trash(userId="me", id=msg_id).execute()
            print(f"Moved message {msg_id} to the trash.")
        except Exception as error:
            print(
                f"An error occurred while moving message {msg_id} to the trash: {error}"
            )

    with open(processed_emails_file_path, "w") as f:
        f.write("")


def search_messages(service, query):
    """
    Searches for messages where the subject contains the search string.
    """
    try:
        response = service.users().messages().list(userId="me", q=query).execute()
        messages = response.get("messages", [])
        return messages
    except Exception as error:
        print(f"An error occurred: {error}")
        return []


def get_message_details(service, msg_id):
    """
    Get specific message details by ID.
    """
    try:
        # pylint: disable=maybe-no-member
        message = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )

        payload = message.get("payload", {})
        headers = payload.get("headers", [])
        snippet = message.get("snippet", "")
        full_text = ""
        raw_text = ""

        if payload.get("body", {}).get("size", 0) > 0:
            raw_text = payload.get("body", {}).get("data", "")
            if len(raw_text) > 0:
                raw_text = base64.urlsafe_b64decode(full_text).decode("UTF-8")
                # Check if the message is an HTML email
                if raw_text.lower().find("html") > 0:
                    soup = BeautifulSoup(raw_text, "html.parser")
                    full_text = soup.get_text(separator="\n", strip=True)
        else:
            full_text = ""

        if full_text == "" and payload.get("parts", []):
            for part in payload.get("parts", []):
                if part.get("body", {}).get("size", 0) > 0:
                    if part.get("mimeType", "") == "text/html":
                        raw_text += part.get("body", {}).get("data", "")

            raw_text = base64.urlsafe_b64decode(raw_text).decode("UTF-8")
            if raw_text.lower().find("html") > 0:
                soup = BeautifulSoup(raw_text, "html.parser")
                full_text = soup.get_text(separator="\n", strip=True)

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "Unknown Sender"
        )
        date = next(
            (h["value"] for h in headers if h["name"] == "Date"), "Unknown Date"
        )

        return {
            "id": msg_id,
            "subject": subject,
            "from": sender,
            "date": date,
            "snippet": snippet,
            "full_text": full_text,
            "raw_text": raw_text,
        }
    except Exception as error:
        print(f"An error occurred retrieving message {msg_id}: {error}")
        return None
