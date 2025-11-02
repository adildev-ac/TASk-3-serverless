# -*- coding: utf-8 -*-
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- IMPORTANT ---
# 1. Replace with your actual Gmail address.
# 2. Use a Gmail "App Password", not your regular password.
#    Get one here: https://myaccount.google.com/apppasswords
sender_email = "batch2023mca@gmail.com"
sender_password = "xjkw pubm dlox bqng"

def send_email(event, context):
    """
    Handles the API request to send an email.
    """
    try:
        # Parse the incoming request body
        body = json.loads(event.get('body', '{}'))
        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')

        # Validate that all required fields are present
        if not all([receiver_email, subject, body_text]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields: receiver_email, subject, and body_text are required."})
            }

        # Create the email message object
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))

        # Connect to Gmail's SMTP server and send the email
        # The 'with' statement ensures the connection is automatically closed
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        # Return a success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format in request body."})
        }
    except Exception as e:
        # In a real app, you would log this error for debugging
        print(f"An unexpected error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)})
        }
