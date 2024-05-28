import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def create_report():
    # Generate a sample report (You can customize this part)
    data = {
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Metric1': [100],
        'Metric2': [200]
    }
    df = pd.DataFrame(data)
    report_path = 'daily_report.csv'
    df.to_csv(report_path, index=False)
    return report_path

def send_email(subject, body, to, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to, text)

def job():
    report_path = create_report()
    send_email(
        subject='Daily Report',
        body='Please find attached the daily report.',
        to='recipient@example.com',
        attachment_path=report_path
    )
    print(f'Email sent: {datetime.now()}')

# Schedule the job every day at a specific time
schedule.every().day.at("09:00").do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
