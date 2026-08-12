"""Save a customer's booking into Google Sheets."""

from datetime import datetime
import os

from app.config import settings
import gspread
from langchain_core.tools import tool


def _get_worksheet():
    """Connect to Google Sheets safely when the tool is executed."""
    if not os.path.exists(settings.google_sheets_credentials_path):
        raise FileNotFoundError(
            f"Google credentials missing at: {settings.google_sheets_credentials_path}"
        )
    return (
        gspread.service_account(
            filename=settings.google_sheets_credentials_path
        )
        .open_by_key(settings.google_sheets_id)
        .sheet1
    )


@tool
def save_booking(
    name: str,
    phone: str,
    service: str,
    preferred_time: str,
    notes: str = "",
) -> str:
    """Save a customer's grooming booking to the salon's records.
    Call this ONLY after you have the customer's name, phone, the service,
    and their preferred date/time.
    """
    worksheet = _get_worksheet()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row(
        [timestamp, name, phone, service, preferred_time, notes]
    )
    return f"Booking saved for {name} ({service}, {preferred_time})."