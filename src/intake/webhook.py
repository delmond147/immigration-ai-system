from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.airtable_client import create_lead
from src.email_service.mailer import send_welcome_email

load_dotenv()
app = FastAPI()


@app.post("/")
async def root():
    return {"message": "Immigration Law Firm AI System is running!"}


@app.post("/intake")
async def intake(request: Request):
    data = await request.json()
    print(f"📥Received intake data: {data}")

    # Extract fields form tally webhook payload
    fields = data.get("data", {}).get("fields", [])

    # Parse fields into a dictionary

    form_data = {}
    for field in fields:
        label = field.get("label", "")
        value = field.get("value", "")
        field_type = field.get("type", "")

        # Handle multiple choice - match ID to text
        if field_type == "MULTIPLE_CHOICE":
            options = field.get("options", [])
            select_ids = value if isinstance(value, list) else [value]
            matched = [opt["text"] for opt in options if opt["id"] in select_ids]
            value = matched[0] if matched else ""
        form_data[label] = value

    print("📋 Parsed form data:", form_data)

    # Extract individual fields
    name = form_data.get("Full Name", "")
    email = form_data.get("Email Address", "")
    phone = form_data.get("Phone number", "")
    case_type = form_data.get("Case Type", "")
    source = form_data.get("How did you hear about us?", "Website")

    # Save lead to Airtable

    create_lead(name=name, email=email, phone=phone, case_type=case_type, source=source)

    # Send welcome email
    if email:
        send_welcome_email(name=name, email=email, case_type=case_type)
        return {
            "status": "success",
            "message": f"Lead created and welcome email sent to {name}",
        }
