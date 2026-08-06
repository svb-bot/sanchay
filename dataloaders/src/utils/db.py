from mysql.connector import connect
import os
import json
import pandas as pd


def get_db_connection():
    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "sanchay"),
    )


def check_db():
    """
    Check if the database connection is successful.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            row = cursor.fetchone()
            if row is None or len(row) == 0:
                raise ValueError("Failed to fetch database name from connection")
            db_name = row[0]
            print(f"Connected to database: {db_name}")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise


def is_integer_string(x):
    """
    Check if the given string represents an integer.
    """
    s = str(x).strip()
    if s.startswith(("+", "-")):
        s = s[1:]
    return s.isdigit()


def generate_notes(row, columns={}):
    """
    Generate notes for a bill based on the row data.
    """
    notes = {}
    for column, ren_column in columns.items():
        if column in row and row[column] is not None:
            value = row.get(column, None)
            if (
                value != ""
                and value != "-"
                and pd.notna(value)
                and pd.notnull(value)
                # and isinstance(value, pd.Timestamp)
                and not (is_integer_string(value) and int(value) == 0)
            ):
                notes[ren_column] = value
    return json.dumps(notes) if notes else None


def derive_transaction_columns(df: pd.DataFrame):
    date_column_name = list(
        filter(
            lambda x: "date" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(date_column_name) > 0:
        date_column_name = date_column_name[0]
    else:
        date_column_name = None

    ref_column_name = list(
        filter(
            lambda x: "ref " in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(ref_column_name) > 0:
        ref_column_name = ref_column_name[0]
    else:
        ref_column_name = None

    deposit_column_name = list(
        filter(
            lambda x: "deposit" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(deposit_column_name) > 0:
        deposit_column_name = deposit_column_name[0]
    else:
        deposit_column_name = None

    details_column_name = list(
        filter(
            lambda x: "details" in x.lower().replace(".", " ").strip()
            or "narration" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(details_column_name) > 0:
        details_column_name = details_column_name[0]
    else:
        details_column_name = None

    withdrawal_column_name = list(
        filter(
            lambda x: "withdrawal" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(withdrawal_column_name) > 0:
        withdrawal_column_name = withdrawal_column_name[0]
    else:
        withdrawal_column_name = None

    issuer_column_name = list(
        filter(
            lambda x: "issuer" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(issuer_column_name) > 0:
        issuer_column_name = issuer_column_name[0]
    else:
        issuer_column_name = None

    consumer_column_name = list(
        filter(
            lambda x: "consumer" in x.lower().replace(".", " ").strip(),
            df.columns.to_list(),
        )
    )
    if len(consumer_column_name) > 0:
        consumer_column_name = consumer_column_name[0]
    else:
        consumer_column_name = None

    return {
        "date_column_name": date_column_name,
        "ref_column_name": ref_column_name,
        "deposit_column_name": deposit_column_name,
        "details_column_name": details_column_name,
        "withdrawal_column_name": withdrawal_column_name,
        "issuer_column_name": issuer_column_name,
        "consumer_column_name": consumer_column_name,
    }


def load_into_stg(table_name: str, df: pd.DataFrame):
    """
    Load a DataFrame into a staging table in the database.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {table_name}")

            insert_qry = (
                f"INSERT INTO {table_name} ({','.join(df.columns)})"
                + f"VALUES({','.join(['%s']*len(df.columns))});"
            )
            cursor.executemany(
                insert_qry,
                (df.values.tolist()),
            )
            print(f"{cursor.rowcount} records inserted into {table_name}")

        conn.commit()


def load_into_main(stg_table_name: str, main_table_name: str, exclusions: list = []):
    """
    Load data from a staging table into a main table in the database.
    """
    hash_exclusions = ["created_at", "updated_at"]
    hash_exclusions.extend(exclusions)
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # get columns
            cursor.execute(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{main_table_name}'"
            )
            columns = cursor.fetchall()
            columns = [
                str(col[0]) for col in columns if str(col[0]) not in hash_exclusions
            ]
            hash_columns_src = [f"COALESCE(src.{col}, '|')" for col in columns]
            hash_columns_tgt = [f"COALESCE(tgt.{col}, '|')" for col in columns]

            print(columns)

            final_insert_query = f"""
            INSERT INTO {main_table_name}({','.join(columns)}, created_at, updated_at)
            SELECT {','.join(columns)}, now(), now() FROM {stg_table_name} tgt 
            WHERE NOT EXISTS (
                SELECT 1
                FROM {main_table_name} src
                where sha1(concat({','.join(hash_columns_src)})) = sha1(concat({','.join(hash_columns_tgt)}))
            )
            """
            cursor.execute(final_insert_query)
            print(f"{cursor.rowcount} records inserted into {main_table_name}")
            conn.commit()
