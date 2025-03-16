import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.core.mail import send_mail
from django.conf import settings
from google.oauth2.service_account import Credentials
import logging

logger = logging.getLogger(__name__)



def add_to_google_sheet(data, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("harambe_service.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open_by_key("1mWN7ZGPgYEF-0FORa0yx3j-DDqON7ZPo_c5IWOjzENU")

    # Select the correct worksheet
    worksheet = sheet.worksheet(sheet_name)

    # Append the data row
    worksheet.append_row(data)


def delete_from_google_sheet(sheet_name, record_id):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("harambe_service.json", scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_key("1mWN7ZGPgYEF-0FORa0yx3j-DDqON7ZPo_c5IWOjzENU")
        worksheet = sheet.worksheet(sheet_name)

        # Find the row with the given ID
        cell = worksheet.find(str(record_id))  # Searches for ID in the sheet

        if cell:
            worksheet.delete_rows(cell.row)  
            print(f"Record {record_id} deleted from {sheet_name} in Google Sheets.")
        else:
            print(f"Record {record_id} not found in {sheet_name}.")

    except gspread.exceptions.WorksheetNotFound:
        print(f"Worksheet '{sheet_name}' not found!")
    except Exception as e:
        print(f"Google Sheets Error: {e}")





def send_email_notification(subject, message, to_email):
    """Utility function to send emails with logging."""
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email
            [to_email],  # To email
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {to_email} with subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")




def clear_google_sheet(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("harambe_service.json", scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_key("1LD-nSwWdwoGTRgm1RvPvhJqsZppm69CeSbZdWJH3-GI")
        worksheet = sheet.worksheet(sheet_name)

        # Clear all data except the header row
        worksheet.resize(1)  # Keeps the first row (header) and deletes everything else
        print(f"Cleared {sheet_name} in Google Sheets.")

    except Exception as e:
        print(f"Error clearing Google Sheet {sheet_name}: {e}")

