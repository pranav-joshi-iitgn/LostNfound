import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
message = Mail(
    from_email="pranav.joshi@iitgn.ac.in",
    to_emails="oranav.joshi@iitgn.ac.in",
    subject="Yay",
    html_content="<strong>Some content</strong>"
    )
try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)
except Exception as e:
    print(e.message)
