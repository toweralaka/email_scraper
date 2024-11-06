import imaplib
import email
# from email.header import decode_header
import pandas as pd
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetching credentials and file paths from environment variables
OUTLOOK_USER = os.getenv("OUTLOOK_USER")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
CSV_PATH = os.getenv("CSV_PATH")

# Configuration for specific email servers
IMAP_SERVERS = {
    "outlook": "outlook.office365.com",
    "gmail": "imap.gmail.com",
}

# Email subjects to look for
TARGET_SUBJECTS = ["Target Subject 1", "Target Subject 2"]

# Path to the CSV file to update
CSV_PATH = "your_file_path.csv"

# Connects to the IMAP server and fetches emails with specific subjects


def fetch_emails(server, user, password):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, password)
    mail.select("inbox")

    attachments = []

    for subject in TARGET_SUBJECTS:
        # Search for emails with the specified subject
        status, messages = mail.search(None, f'SUBJECT "{subject}"')

        # List of email IDs that match the subject
        email_ids = messages[0].split()

        for email_id in email_ids:
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            # Check if the email has attachments
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()

                    if filename:
                        # Download the attachment
                        filepath = os.path.join("attachments", filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        attachments.append(filepath)

                        # Optional: Print a message
                        print(f"Downloaded {filename}")

    mail.logout()
    return attachments

# Updates the CSV file with new attachment info


def update_csv(attachments):
    # Load or create the CSV file
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(columns=["filename", "path"])

    # Append the new attachments to the DataFrame
    for attachment in attachments:
        filename = os.path.basename(attachment)
        df = df.append(
            {"filename": filename, "path": attachment}, ignore_index=True)

    # Save the updated CSV
    df.to_csv(CSV_PATH, index=False)
    print(f"CSV updated with {len(attachments)} new entries.")

# Main function to run the entire process


def main():
    attachments = []

    # Fetch emails from both Outlook and Gmail
    for provider, server in IMAP_SERVERS.items():
        if provider == "outlook":
            attachments += fetch_emails(server, OUTLOOK_USER, OUTLOOK_PASSWORD)
        elif provider == "gmail":
            attachments += fetch_emails(server, GMAIL_USER, GMAIL_PASSWORD)

    # Update the CSV file with attachment paths
    update_csv(attachments)


if __name__ == "__main__":
    os.makedirs("attachments", exist_ok=True)
    main()
