import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email: str, subject: str, html_content: str):
    """ "Core email sender via Gmail SMTP."""
    try:
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Immigration Law Firm <{gmail_user}"
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, msg.as_string())

        print(f"✅ Email sent to: {to_email}")
        return True
    except Exception as e:
        import traceback

        print(f"❌ Email failed: {e}")
        traceback.print_exc()
        return None


def send_welcome_email(name: str, email: str, case_type: str):
    """Send welcome email to new client."""
    subject = "We received your inquiry - Immigration Law Firm"
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c3e50;">Thank you for contacting us!</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>We have received your inquiry about your <strong>{case_type}</strong> case.</p>
            <p>One of our experienced immigration attorneys will contact you within 
            <strong>24 hours</strong> to schedule your consultation.</p>
            <p>In the meantime, feel free to reply to this email if you have any questions.</p>
            <br>
            <p>Best regards,</p>
            <p><strong>Immigration Law Firm Team</strong></p>
            <hr style="border: 1px solid #ecf0f1;">
            <p style="font-size: 12px; color: #7f8c8d;">This is an automated message.</p>
        </div>
    """
    return send_email(to_email=email, subject=subject, html_content=html)


def send_reminder_email(name: str, email: str, consultation_date: str):
    """Send consultation reminder email 24 hours before."""
    subject = "Reminder: Your Consultation is coming up Tomorrow."
    html = f"""
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
    """
    return send_email(to_email=email, subject=subject, html_content=html)


def send_followup_email(name: str, email: str, case_type: str):
    """Send follow-up email after consultation."""
    subject = "Next Steps After Your Consultation."
    html = f"""
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
            <p>Don't hesitate to reach out if you have any questions.</p>
            <br>
            <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
        </div>
    """
    return send_email(to_email=email, subject=subject, html_content=html)


def send_reactivation_email(name: str, email: str, case_type: str):
    """Send reactivation email to cold leads."""
    subject = "We're Still Here to Help With Your Immigration Case."
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c5282;">We Haven't Forgotten About You</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>We noticed it's been a while since we last spoke about
            your <strong>{case_type}</strong> case.</p>
            <p>Immigration processes can feel overwhelming, but you don't
            have to navigate them alone. Our attorneys are ready to help.</p>
            <p><strong>Reply to this email</strong> or call us at
            +1 (555) 123-4567 to reconnect.</p>
            <br>
            <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
        </div>
    """
    return send_email(to_email=email, subject=subject, html_content=html)


def send_checklist_email(name: str, email: str, case_type: str, checklist_html: str):
    """Send document checklist email to client."""
    subject = f"Your Document Checklist - {case_type} Application"
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c5282;">Your Document Checklist</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>Thank you for choosing our firm for your
            <strong>{case_type}</strong> case.</p>
            <p>Please gather the following documents:</p>
            {checklist_html}
            <p>Please submit all documents within <strong>7 days</strong>
            to avoid delays.</p>
            <br>
            <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
            <hr style="border: 1px solid #ecf0f1;">
            <p style="font-size: 12px; color: #7f8c8d;">
            Need help? Call us at +1 (555) 123-4567</p>
        </div>
    """
    return send_email(to_email=email, subject=subject, html_content=html)


def send_document_reminder_email(name: str, email: str, case_type: str):
    """Send reminder email if documents not received after 7 days."""
    subject = f"Reminder: Documents Needed for Your {case_type} Case."
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #e53e3e;">Action Required: Documents Pending</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>We noticed we haven't received your documents yet for
            your <strong>{case_type}</strong> case.</p>
            <p>Please submit them as soon as possible to keep your case on track.</p>
            <p><strong>Reply to this email</strong> or call us at
            +1 (555) 123-4567 for assistance.</p>
            <br>
            <p>Best regards,<br><strong>Immigration Law Firm Team</strong></p>
        </div>
    """
    return send_email(to_email=email, subject=subject, html_content=html)
