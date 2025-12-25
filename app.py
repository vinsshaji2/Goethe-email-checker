from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

SHEET_ID = "16US9ffxJm6JZh6V3l-zn57Y75J5b-bBbGQaZvRZkr4c"
spreadsheet = client.open_by_key(SHEET_ID)

from flask import send_from_directory

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/check_email", methods=["POST"])
def check_email():
    email = request.json.get("email", "").strip().lower()

    TARGET_COLUMN = "EMAIL ID USED IN GOETHE-ZENTRUM TVM"

    for worksheet in spreadsheet.worksheets():
        rows = worksheet.get_all_records()

        for row in rows:
            cell_value = str(row.get(TARGET_COLUMN, "")).strip().lower()

            if cell_value == email:
                return jsonify({
                    "found": True,
                    "sheet": worksheet.title,
                    "data": row
                })

    return jsonify({"found": False})

if __name__ == "__main__":
    app.run(debug=True)
