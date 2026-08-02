from argparse import ArgumentParser
from dotenv import load_dotenv
from utils import (
    get_gmail_service,
    search_messages,
    get_message_details,
    clear_processed_emails,
    save_processed_email_ids,
)
import re
import pandas as pd
from datetime import datetime
import dateparser
from io import StringIO
import os


def get_flipkart_bills(service):
    """
    Get Flipkart bills from Gmail and save them to a CSV file.
    """
    target_subject = "subject:(Your Order for has been successfully placed) flipkart "
    print(f"Searching for emails with title containing: '{target_subject}'...")
    found_messages = search_messages(service, target_subject)

    print(f"Found {len(found_messages)} messages.")

    data = []
    for msg in found_messages:
        details = get_message_details(service, msg["id"])
        if details:
            order_id = re.search(
                r"(?<=order id\n)(\w+)", details["full_text"], flags=re.IGNORECASE
            )
            order_date = re.search(
                r"(?<=order placed on\n)(.*)", details["full_text"], flags=re.IGNORECASE
            )
            amount = re.search(
                r"(?:amount\s+(?:paid|payable)\s*(?:Rs.|₨.)\s*)(\d+(?:\.\d+)?)",
                details["full_text"],
                flags=re.IGNORECASE,
            )
            if details["full_text"].find("Grocery Basket") > 0:
                bill_type = "Grocery"
            else:
                bill_type = "General"

            data.append(
                {
                    "id": msg["id"],
                    "order_id": order_id.group(1) if order_id else "",
                    "order_date": (
                        datetime.strptime(order_date.group(1), "%b %d, %Y").strftime(
                            "%Y-%m-%d"
                        )
                        if order_date
                        else ""
                    ),
                    "amount": (amount.group(1) if amount else ""),
                    "bill_type": bill_type,
                }
            )

    df = pd.DataFrame(data)
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(os.getcwd(), "data", f"flipkart_bills_{timestamp}.csv")
    if not df.empty:
        df.to_csv(file_path, index=False)
        save_processed_email_ids([row[0] for row in df[["id"]].values.tolist()])


def get_hpgas_bills():
    """
    Get HP Gas bills from HTML file and save them to a CSV file.
    """
    source_file = os.path.join(os.getcwd(), "data", "hpgas_bills.html")
    with open(source_file, "r") as f:
        data = f.read()

    if not data:
        return
    df = pd.read_html(StringIO(data))[0]
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(os.getcwd(), "data", f"hpgas_bills_{timestamp}.csv")
    if not df.empty:
        df.to_csv(file_path, index=False)


def get_cesc_bills(service):
    """
    Get CESC bills from Gmail and save them to a CSV file.
    """
    target_subject = (
        "subject:(alert: bill payment processed successfully) biller name: cesc limited"
    )
    print(f"Searching for emails with title containing: '{target_subject}'...")
    found_messages = search_messages(service, target_subject)

    print(f"Found {len(found_messages)} messages.")

    data = []
    for msg in found_messages[:100]:
        details = get_message_details(service, msg["id"])
        if details:
            reference_no = re.search(
                r"(?<=reference no: )(\w+)", details["full_text"], flags=re.IGNORECASE
            )
            consumer_id = re.search(
                r"(?<=customer id \(not consumer no\):)(\d+)",
                details["full_text"],
                flags=re.IGNORECASE,
            )
            issuer = re.search(
                r"(?<=biller name: )(.*)", details["full_text"], flags=re.IGNORECASE
            )
            date = re.search(
                r"(?<=payment date: )(.*)", details["full_text"], flags=re.IGNORECASE
            )
            amount = re.search(
                r"(?<=amount \(rs.\): )(.*)", details["full_text"], flags=re.IGNORECASE
            )

            data.append(
                {
                    "reference_no": reference_no.group(1) if reference_no else "",
                    "issuer": issuer.group(1) if issuer else "",
                    "consumer_id": consumer_id.group(1) if consumer_id else "",
                    "date": date.group(1) if date else "",
                    "amount": amount.group(1) if amount else "",
                    "id": msg["id"],
                }
            )

    df = pd.DataFrame(data)
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(os.getcwd(), "data", f"cesc_bills_{timestamp}.csv")
    if not df.empty:
        df.to_csv(file_path, index=False)
        save_processed_email_ids([row[0] for row in df[["id"]].values.tolist()])


def get_jiofiber_bills(service):
    """
    Get JioFiber bills from Gmail and save them to a CSV file.
    """
    target_subject = "(subject:Recharge successful for JioFiber connection having JioFixedVoice Number)"
    print(f"Searching for emails with title containing: '{target_subject}'...")
    found_messages = search_messages(service, target_subject)

    print(f"Found {len(found_messages)} messages.")

    data = []
    for msg in found_messages:
        details = get_message_details(service, msg["id"])
        if details:
            txn_id = re.search(
                r"(?<=transaction id : )(\w+)",
                details["full_text"],
                flags=re.IGNORECASE,
            )
            bill_date = dateparser.parse(details["date"][:-5])
            print(bill_date)
            amount = re.search(
                r"(?<=recharge of rs.)([\d\.]+)",
                details["full_text"],
                flags=re.IGNORECASE,
            )

            data.append(
                {
                    "id": msg["id"],
                    "txn_id": txn_id.group(1) if txn_id else "",
                    "bill_date": (
                        bill_date.strftime("%Y-%m-%d") if bill_date is not None else ""
                    ),
                    "amount": amount.group(1) if amount else "",
                }
            )

    df = pd.DataFrame(data)
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(os.getcwd(), "data", f"jiofiber_bills_{timestamp}.csv")
    if not df.empty:
        df.to_csv(file_path, index=False)
        save_processed_email_ids([row[0] for row in df[["id"]].values.tolist()])


if __name__ == "__main__":
    load_dotenv()
    possible_types = ["cesc", "flipkart", "hpgas", "jiofiber"]
    service = get_gmail_service()
    clear_processed_emails(service)

    parser = ArgumentParser(description="Pull CESC bills from email")
    # parser.add_argument(
    #     "--email", type=str, required=True, help="Email address to pull bills from"
    # )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=possible_types,
        help=f"Type of bills to loaded: {', '.join(possible_types)}",
    )
    args = parser.parse_args()

    if args.type not in possible_types:
        raise ValueError(f"Invalid bill type. Must be {', '.join(possible_types)}.")
    bill_type = args.type

    if bill_type == "cesc":
        get_cesc_bills(service)
    elif bill_type == "flipkart":
        get_flipkart_bills(service)
    elif bill_type == "hpgas":
        get_hpgas_bills()
    elif bill_type == "jiofiber":
        get_jiofiber_bills(service)
