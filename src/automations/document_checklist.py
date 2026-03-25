import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.airtable_client import (
    get_leads_pending_checklist,
    get_docs_not_received,
    mark_checklist_sent,
    create_document_checklist,
    get_table,
)

from src.email_service.mailer import send_checklist_email, send_document_reminder_email

from src.automations.checklists import format_checklist_html, format_checklist_text


def run_checklist_automation():
    """Send document checklist to leads who haven't received one yet."""
    print("\n Running checklist automation...")

    leads = get_leads_pending_checklist()

    if not leads:
        print(" No leads pending checklist.")
        return

    for lead in leads:
        fields = lead["fields"]
        record_id = lead["id"]
        name = fields.get("Name", "")
        email = fields.get("Email", "")
        case_type = fields.get("Case Type", "")

        if not email or not case_type:
            continue

        # Format checklist
        checklist_html = format_checklist_html(case_type)
        checklist_text = format_checklist_text(case_type)

        # Save checklist to Airtable Documents Checklist table
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        create_document_checklist(
            client_name=name, case_type=case_type, required_docs=checklist_text
        )

        # Update due date in Documents Checklist
        checklist_table = get_table("Documents Checklist")
        all_records = checklist_table.all()
        for record in reversed(all_records):
            if record["fields"].get("Client Name") == name:
                checklist_table.update(record["id"], {"Due Date": due_date})
                break

        # Mark checklist as sent in Leads table
        mark_checklist_sent(record_id)

        print(f"Checklist processed for: {name} ({case_type})")


def run_document_reminder():
    """Send reminders for overdue document."""
    print("\n Running document reminder automation...")

    overdue_records = get_docs_not_received()

    if not overdue_records:
        print("  No overdue documents.")
        return

    for record in overdue_records:
        fields = record["fields"]
        client_name = fields.get("Client Name", "")
        case_type = fields.get("Case Type", "")

        # Find email from Leads table
        leads_table = get_table("Leads")
        matching_leads = leads_table.all(formula=f"{{Name}} = '{client_name}'")

        if matching_leads:
            email = matching_leads[0]["fields"].get("Email", "")
            if email:
                send_document_reminder_email(
                    name=client_name, email=email, case_type=case_type
                )
                print(f"Document reminder sent for: {client_name}")


def run_all_checklist_automations():
    """Run all checklist automations."""
    print("\n Running all checklist automations...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    run_checklist_automation()
    run_document_reminder()

    print("\n All checklist automations complete.")
