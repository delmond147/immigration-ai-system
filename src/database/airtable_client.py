from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime, date
import os

load_dotenv()

api = Api(os.getenv("AIRTABLE_API_KEY"))
base_id = os.getenv("AIRTABLE_BASE_ID")


def get_table(table_name: str):
    return api.table(base_id, table_name)


# --- LEADS TABLE ---


def create_lead(
    name: str, email: str, phone: str, case_type: str, source: str = "Website"
):
    table = get_table("Leads")
    record = table.create(
        {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Case Type": case_type,
            "Status": "New",
            "Source": source,
            "Date Added": str(date.today()),
        }
    )
    print(f"✅ Lead created: {name}")
    return record


def get_all_leads():
    table = get_table("Leads")
    return table.all()


def get_leads_by_status(status: str):
    table = get_table("Leads")
    return table.all(formula=f"{{status}} = '{status}'")


def update_lead_status(record_id: str, status: str):
    table = get_table("Leads")
    table.update(record_id, {"Status": status})
    print(f"✅ Lead {record_id} status updated to: {status}")


# Schedule Consultation


def schedule_consultation(record_id: str, consultation_date: str):
    """Set Consultation date for a lead."""
    table = get_table("Leads")
    table.update(
        record_id,
        {"Status": "Consultation Booked", "Consultation Date": consultation_date},
    )
    print(f"Consultation scheduled for record: {record_id}")


def get_leads_for_reminder():
    """ "Get leads with consultation date date within the next 24 hours."""
    table = get_table("Leads")
    all_leads = table.all()

    leads_for_reminder = []
    now = datetime.now()

    for lead in all_leads:
        fields = lead["fields"]
        consultation_date_str = fields.get("Consultation Date", "")

        if consultation_date_str:
            try:
                consultation_date = datetime.fromisoformat(
                    consultation_date_str.replace("Z", "")
                )
                hours_until = (consultation_date - now).total_seconds() / 3600

                # Within the next 24 hours and hasn't happened yet
                if 0 < hours_until <= 24:
                    get_leads_for_reminder.append(lead)
            except:
                pass
    return leads_for_reminder


def get_leads_for_followup():
    """ "Get leads with consultation date in the past that haven't been followed up."""
    table = get_table("Leads")
    all_leads = table.all()

    leads_to_followup = []
    now = datetime.now()

    for lead in all_leads:
        fields = lead["fields"]
        consultation_date_str = fields.get("Consultation Date", "")
        follow_up_sent = fields.get("Follow Up Sent", False)

        if consultation_date_str and not follow_up_sent:
            try:
                consultation_date = datetime.fromisoformat(
                    consultation_date_str.replace("Z", "")
                )
                if consultation_date <= now:
                    leads_to_followup.append(lead)
            except:
                pass
    return leads_to_followup


def mark_follow_up_sent(record_id: str):
    """ "Mark a lead as having received a follow-up email."""
    table = get_table("Leads")
    table.update(
        record_id, {"Follow Up Sent": True, "Last Contacted": str(date.today())}
    )
    print("Follow-up marked for record: {record_id}")


def mark_reactivation_sent(record_id: str):
    """Mark a lead as having received a reactivation email."""
    table = get_table("Leads")
    table.update(
        record_id, {"Reactivation Sent": True, "Last Contacted": str(date.today())}
    )

    print("Reactivation marked for record: {record_id}")


# ---- CONVERSATIONS TABLE ---
def log_conversation(
    client_name: str, message: str, ai_response: str, channel: str = "Website"
):
    table = get_table("Conversations Log")
    record = table.create(
        {
            "Client Name": client_name,
            "Message": message,
            "AI Response": ai_response,
            "Channel": channel,
            "Timestamp": str(datetime.now()),
        }
    )
    print(f"✅ Conversation logged for: {client_name}")
    return record


# ---- DOCUMENTS CHECKLIST TABLE ---


def create_document_checklist(client_name: str, case_type: str, required_docs: str):
    table = get_table("Documents Checklist")
    record = table.create(
        {
            "Client Name": client_name,
            "Case Type": case_type,
            "Required Document": required_docs,
            "Document Received": False,
        }
    )
    print(f"✅ Document checklist created for: {client_name}")
    return record


def get_leads_pending_checklist():
    """Get leads with a case type but no checklist sent yet."""
    table = get_table("Leads")
    all_leads = table.all()

    pending = []
    for lead in all_leads:
        fields = lead["fields"]
        case_type = fields.get("Case Type", "")
        checklist_sent = fields.get("Checklist Sent", False)
        status = fields.get("Status", "")

        # Only send to active leads with a case type

        if case_type and not checklist_sent and status != "Cold":
            pending.append(lead)

    return pending


def get_docs_not_received():
    """Get leads whose documents haven't been received after 7 days."""
    table = get_table("Documents Checklist")
    all_records = table.all()

    overdue = []
    now = datetime.now()

    for record in all_records:
        fields = record["fields"]
        docs_received = fields.get("Document Received", False)
        due_date_str = fields.get("Due Date", "")

        if not docs_received and due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str)
                if now > due_date:
                    overdue.append(record)
            except:
                pass
    return overdue


def mark_checklist_sent(record_id: str):
    """Mark that a checklist has been sent to this lead."""
    table = get_table("Leads")
    table.update(
        record_id, {"Checklist Sent": True, "Last Contacted": str(date.today())}
    )
    print(f"Checklist marked as sent for: {record_id}")
