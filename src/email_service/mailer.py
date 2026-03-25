import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_welcome_email(name: str, email: str, case_type: str):
    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": "We received your inquiry - Immigration Law Firm",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2c3e50;">Thank you for contacting us!</h2>
                <p>Hi <strong>{name}</strong>,</p>
                <p>We have received your inquiry about your <strong>{case_type}</strong> case.</p>
                <p>One of our experienced immigration attorneys will contact you within <strong>24 hours</strong> to schedule your consultation.</p>
                <p>In the meantime, feel free to reply to this email if you have any additional questions.</p>
                <br>
                <p>Best regards,</p>
                <p><strong>Immigration Law Firm Team</strong></p>
                <hr style="border: 1px solid #ecf0f1;">
                <p style="font-size: 12px; color: #7f8c8d;">This is an automated message. Please ignore this email.</p>
                </div>
            """,
            }
        )

        print(f"✅ Welcome email sent to: {email}")
        return response
    except Exception as e:
        print(f"❌ Email Failed: {e}")

        return None


def send_reminder_email(name: str, email: str, consultation_date: str):
    """Send consultation reminder email 24 hours before."""
    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": "Reminder: Your Consultation Tomorrow",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2c5282;">Your Consultation is Tomorrow</h2>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>This is a friendly reminder that your consultation is scheduled for
                    <strong>{consultation_date}</strong>.</p>
                    <p>To make the most of your consultation, please prepare:</p>
                    <ul>
                        <li>A list of questions you'd like to ask</li>
                        <li>Any relevant documents related to your case</li>
                        <li>Your immigration history if applicable</li>
                    </ul>
                    <p>If you need to reschedule, please contact us as soon as possible.</p>
                    <br>
                    <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
                </div>
            """,
            }
        )
        print(f"Reminder email sent to: {email}")
        return response
    except Exception as e:
        print(f"Reminder email failed: {e}")
        return None


def send_followup_email(name: str, email: str, case_type: str):
    """ "Send follow-up email after consultation."""

    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": "Next Steps After Your Consultation",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2c5282;">Thank You for Meeting With Us</h2>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for your consultation regarding your
                    <strong>{case_type}</strong> case.</p>
                    <p>Here are your next steps:</p>
                    <ol>
                        <li>Review the document checklist we discussed</li>
                        <li>Gather all required documents</li>
                        <li>Reply to this email when you're ready to proceed</li>
                    </ol>
                    <p>Our team is ready to guide you through every step of the process.
                    Don't hesitate to reach out if you have any questions.</p>
                    <br>
                    <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
                </div>""",
            }
        )
        print(f"Follow-up email sent to: {email}")
        return response
    except Exception as e:
        print(f"Follow-up email failed: {e}")
        return None


def send_reactivation_email(name: str, email: str, case_type: str):
    """Send reactivation email to cold leads."""
    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": "We're Still Here to Help With Your Immigration Case",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2c5282;">We Haven't Forgotten About You</h2>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>We noticed it's been a while since we last spoke about
                    your <strong>{case_type}</strong> case.</p>
                    <p>Immigration processes can feel overwhelming, but you don't
                    have to navigate them alone. Our experienced attorneys are
                    ready to help you move forward.</p>
                    <p>A lot can change in immigration law — let's make sure
                    you have the most current information for your case.</p>
                    <p><strong>Reply to this email</strong> or call us at
                    +1 (555) 123-4567 to reconnect with our team.</p>
                    <br>
                    <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
                </div>
            """,
            }
        )
        print(f"Reactivation email sent to: {email}")
        return response
    except Exception as e:
        print(f"Reactivation email failed: {e}")
        return None


def send_checklist_email(name: str, email: str, case_type: str, checklist_html: str):
    """Send document checklist email to client."""

    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": f"Your Document Checklist - {case_type} Application",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2c5282;">Your Document Checklist</h2>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for choosing our firm for your 
                    <strong>{case_type}</strong> case.</p>
                    <p>To move forward with your application, please gather 
                    the following documents:</p>
                    {checklist_html}
                    <p>Please submit all documents within <strong>7 days</strong> 
                    to avoid delays in your application.</p>
                    <p>If you have any questions about a specific document, 
                    reply to this email and our team will assist you.</p>
                    <br>
                    <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
                    <hr style="border: 1px solid #ecf0f1;">
                    <p style="font-size: 12px; color: #7f8c8d;">
                    Need help? Call us at +1 (555) 123-4567 or email 
                    info@immigrationlawfirm.com</p>
                </div>
            """,
            }
        )
        print(f"Checklist email sent to: {email}")
        return response
    except Exception as e:
        print(f"Checklist email failed: {e}")
        return None


def send_document_reminder_email(name: str, email: str, case_type: str):
    """Send reminder email if documents not received after 7 days."""
    try:
        response = resend.Emails.send(
            {
                "from": "Immigration Law Firm <onboarding@resend.dev>",
                "to": email,
                "subject": f"Reminder: Documents Needed for Your {case_type} Case",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #e53e3e;">Action Required: Documents Pending</h2>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>We noticed we haven't received your documents yet for 
                    your <strong>{case_type}</strong> case.</p>
                    <p>Missing documents can delay your application significantly. 
                    Please submit them as soon as possible to keep your case 
                    on track.</p>
                    <p>If you're having trouble gathering any of the required 
                    documents, please reply to this email and our team will 
                    guide you through the process.</p>
                    <p><strong>Reply to this email</strong> or call us at 
                    +1 (555) 123-4567 for assistance.</p>
                    <br>
                    <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
                </div>
            """,
            }
        )
        print(f"Document reminder sent to: {email}")
        return response
    except Exception as e:
        print(f"Document reminder failed: {e}")
        return None
