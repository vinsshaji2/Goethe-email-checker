from flask import Flask, request, jsonify, send_from_directory
import json, os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/check_email", methods=["POST"])
def check_email():
    email = request.json.get("email", "").strip().lower()

    # Load Google credentials from Vercel environment variable
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    SHEET_ID = "16US9ffxJm6JZh6V3l-zn57Y75J5b-bBbGQaZvRZkr4c"
    spreadsheet = client.open_by_key(SHEET_ID)

    TARGET_COLUMN = "EMAIL ID USED IN GOETHE-ZENTRUM TVM"

    for sheet in spreadsheet.worksheets():
        for row in sheet.get_all_records():
            if str(row.get(TARGET_COLUMN, "")).strip().lower() == email:
                return jsonify({"found": True})

    return jsonify({"found": False})

if __name__ == "__main__":
    app.run()
