# Document checklists per case type
CHECKLISTS = {
    "Work Visa": [
        "Valid passport (minimum 6 months validity)",
        "Job offer letter from U.S. employer",
        "Signed employment contract",
        "Educational certificates and transcripts",
        "Proof of work experience (reference letters)",
        "Resume / CV",
        "Labor Condition Application (LCA)",
        "Passport-sized photographs",
        "Proof of language proficiency (if required)",
        "Police clearance certificate",
        "Medical certificate",
    ],
    "Green Card": [
        "Valid passport",
        "Form I-485 (Application to Register Permanent Residence)",
        "Birth certificate (with certified translation if needed)",
        "Marriage certificate (if applicable)",
        "Police clearance certificate",
        "Medical examination results (Form I-693)",
        "Proof of financial support (Form I-864)",
        "Two passport-sized photographs",
        "Tax returns for past 3 years",
        "Proof of continuous residence",
        "Employment authorization (if applicable)",
    ],
    "Citizenship": [
        "Permanent Resident Card (Green Card)",
        "Form N-400 (Application for Naturalization)",
        "Valid passport or travel document",
        "Passport-sized photographs",
        "Tax returns for past 5 years",
        "Proof of continuous residence",
        "Proof of physical presence in the U.S.",
        "Marriage certificate (if married to U.S. citizen)",
        "Any court records (if applicable)",
        "Selective Service registration (if applicable)",
    ],
    "DACA": [
        "Proof of identity (passport, birth certificate, or school ID)",
        "Proof of immigration status",
        "Proof of arrival in U.S. before age 16",
        "Proof of continuous residence since June 15, 2007",
        "Proof of current school enrollment or graduation",
        "Proof of employment (if applicable)",
        "Form I-821D (DACA Request)",
        "Form I-765 (Work Permit Application)",
        "Form I-765WS (Worksheet)",
        "Two passport-sized photographs",
        "Filing fee payment receipt",
    ],
}


def get_checklist(case_type: str) -> list:
    """ "Get document checklist for a given case type."""
    return CHECKLISTS.get(case_type, [])


def format_checklist_html(case_type: str) -> str:
    """Format checklist as HTML for email."""
    checklist = get_checklist(case_type)

    if not checklist:
        return "<p> Please contact us for a customized document list.</p>"

    items = "".join([f"<li>{item}</li>" for item in checklist])
    return f"<ol>{items}</ol>"


def format_checklist_text(case_type: str) -> str:
    """Format checklist as plain text for Airtable."""
    checklist = get_checklist(case_type)

    if not checklist:
        return "Please contact us for a customized document list."
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(checklist)])
