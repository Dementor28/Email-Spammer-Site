import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import schedule
import time
import os
import sys

# Counter
email_counter = 0

def send_email(sender_email, password, receiver_email, subject, body, image_paths, pdf_paths):
    global email_counter
    smtp_server = "smtp.office365.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach images
    for image_path in image_paths:
        if image_path:  # Check if path is not empty
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                image = MIMEImage(image_data)
                image.add_header("Content-Disposition", "attachment", filename=os.path.basename(image_path))
                msg.attach(image)

    # Attach PDFs
    for pdf_path in pdf_paths:
        if pdf_path:  # Check if path is not empty
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                pdf_attachment = MIMEApplication(pdf_data)
                pdf_attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(pdf_path))
                msg.attach(pdf_attachment)

    server = None  # Initialize the server variable

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, [receiver_email], text)
        email_counter += 1
        print(f"Email sent successfully, total emails sent: {email_counter}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        if server:
            server.quit()

def main():
    if len(sys.argv) < 8:
        print("Usage: python email_spammer.py <sender_email> <password> <receiver_email> <subject> <body> <schedule_option> <image_paths> <pdf_paths>")
        return

    sender_email = sys.argv[1]
    password = sys.argv[2]
    receiver_email = sys.argv[3]
    subject = sys.argv[4]
    body = sys.argv[5]
    schedule_option = sys.argv[6]
    image_paths = sys.argv[7:10]  # Up to 3 image paths
    pdf_paths = sys.argv[10:13]  # Up to 3 PDF paths

    # Send the first email immediately
    send_email(sender_email, password, receiver_email, subject, body, image_paths, pdf_paths)

    # Schedule to send email based on user input
    if schedule_option == "everyMinute":
        schedule.every(1).minute.do(send_email, sender_email, password, receiver_email, subject, body, image_paths, pdf_paths)
    elif schedule_option == "everyHour":
        schedule.every(1).hour.do(send_email, sender_email, password, receiver_email, subject, body, image_paths, pdf_paths)
    elif schedule_option == "everyDay":
        schedule.every(1).day.do(send_email, sender_email, password, receiver_email, subject, body, image_paths, pdf_paths)
    else:
        print("Invalid schedule option. Use 'everyMinute', 'everyHour', or 'everyDay'.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
