import pandas as pd
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Load CSV and clean roll numbers
df = pd.read_csv("students.csv", dtype=str)   # force all as strings
df['roll_number'] = df['roll_number'].str.strip().str.lstrip("0")  # remove spaces & leading zeros
roll_to_name = dict(zip(df['roll_number'], df['name']))

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").strip()
    roll_numbers = [r.strip().lstrip("0") for r in incoming_msg.split(",")]  # normalize input too

    response_lines = []
    for roll in roll_numbers:
        name = roll_to_name.get(roll, f"{roll} - Not Found")
        response_lines.append(name)

    resp = MessagingResponse()
    resp.message("\n".join(response_lines))
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
