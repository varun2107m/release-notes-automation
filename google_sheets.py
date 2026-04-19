import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "Release_notes"


def get_sheet_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
    client = gspread.authorize(creds)
    return client


def get_latest_release():
    """
    Reads the latest row from the Google Sheet.
    Expected columns:
    Version | Release Date | Confluence URL | Recipients | Approval Status | Approved By
    """
    client = get_sheet_client()
    sheet = client.open(SHEET_NAME).sheet1
    records = sheet.get_all_records()

    if not records:
        raise Exception("❌ No data found in the Google Sheet.")

    # Get the last row (latest release)
    latest = records[-1]

    return {
        "version": latest.get("Version", ""),
        "release_date": latest.get("Release Date", ""),
        "confluence_url": latest.get("Confluence URL", ""),
        "recipients": [r.strip() for r in str(latest.get("Recipients", "")).split(",") if r.strip()],
        "approval_status": latest.get("Approval Status", "Pending").strip(),
    }
