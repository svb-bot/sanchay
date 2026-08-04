from utils.db import (
    get_db_connection,
    check_db,
    generate_notes,
    load_into_stg,
    derive_transaction_columns,
    load_into_main,
)
from utils.email_parser import (
    search_messages,
    get_message_details,
    get_gmail_service,
    save_processed_email_ids,
    clear_processed_emails,
)
import os
import pandas as pd


def get_dataframe(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == ".html":
        return pd.read_html(file_path)[0]
    else:
        return pd.read_csv(file_path)
