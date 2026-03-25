from datetime import datetime, timedelta, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.airtable_client import (
    get_leads_for_followup,
    get_leads_for_reminder,
    get_leads_by_status,
    mark_follow_up_sent,
    mark_reactivation_sent,
    update_lead_status,
    get_table,
)
from src.email_service.mailer import (
    send_reminder_email,
    send_followup_email,
    send_reactivation_email,
)


def run_reminder_sequence():
    """ "Send reminders to leads with consultation in next 24 hours."""
    print("\n Running reminder sequence...")
    leads = get_leads_for_reminder()

    if not leads:
        print("    No upcoming consultations in next 24 hours.")
        return

    for lead in leads:
        fields = lead["fields"]
        name = fields.get("Name", "")
        email = fields.get("Email", "")
        consultation_date = fields.get("Consultation Date", "")

        if email:
            send_reminder_email(
                name=name, email=email, consultation_date=consultation_date
            )


def run_followup_sequence():
    """ "Send follow-up emails to leads whose consultation has passed."""
    print("\n Running follow-up sequence...")
    leads = get_leads_for_followup()

    if not leads:
        print(" No leads pending follow-up.")
        return

    for lead in leads:
        fields = lead["fields"]
        record_id = lead["id"]
        name = fields.get("Name", "")
        email = fields.get("Email", "")
        case_type = fields.get("Case Type", "immigration")

        if email:
            send_followup_email(name=name, email=email, case_type=case_type)
            mark_follow_up_sent(record_id)
            update_lead_status(record_id, "Contacted")


def run_reactivation_sequence():
    """Send reactivation emails to cold leads."""
    print("\n Running reactivation sequence...")

    cold_leads = get_leads_by_status("Cold")

    if not cold_leads:
        print(" No cold leads to reactivate.")
        return

    for lead in cold_leads:
        fields = lead["fields"]
        record_id = lead["id"]
        name = fields.get("Name", "")
        email = fields.get("Email", "")
        case_type = fields.get("Case Type", "immigration")
        reactivation_sent = fields.get("Reactivation Sent", False)

        # Only send if not already reactivated
        if email and not reactivation_sent:
            send_reactivation_email(name=name, email=email, case_type=case_type)
            mark_reactivation_sent(record_id)


def run_all_sequences():
    """Run all automation sequences."""
    print("Running all follow-up automation...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    run_reminder_sequence()
    run_followup_sequence()
    run_reactivation_sequence()

    print("\n All sequences complete.")
