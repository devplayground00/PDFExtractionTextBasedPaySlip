import imaplib
import email
from email.header import decode_header
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailHelper:

    def __init__(self, email_user, email_pass):
        self.email_user = email_user
        self.email_pass = email_pass

    def read_emails_from_inbox(self):
        email_details = {}

        try:
            # Connect to Gmail IMAP server
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_user, self.email_pass)
            mail.select("inbox")

            # Search for all emails
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()

            for email_id in email_ids:
                _, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Extract email details (sender, subject, etc.)
                        sender_email = msg["From"].split()[-1].strip("<>")
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()

                        # Extract email body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                                    body = part.get_payload(decode=True).decode()
                        else:
                            body = msg.get_payload(decode=True).decode()

                        # Store email details in a dictionary
                        email_details[email_id] = {
                            "sender": sender_email,
                            "subject": subject,
                            "body": body
                        }

                        # For debugging
                        # print(f"From: {sender_email}\nSubject: {subject}\nBody: {body}\n")

            mail.logout()

        except Exception as e:
            print(f"Error reading emails: {e}")

        return email_details

    def download_pdfs_from_email(self, working_folder):
        files_with_senders = {}

        try:
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_user, self.email_pass)
            mail.select("inbox")

            # Search for all emails and get the first one
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()


            if not email_ids:
                print("No emails found in the inbox.")
                return files_with_senders  # Return empty dictionary

            first_email_id = email_ids[0]  # Get the first email

            # Fetch and process only the first email
            _, msg_data = mail.fetch(first_email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender_email = msg["From"]
                    sender_email = sender_email.split()[-1].strip("<>") if sender_email else "Unknown Sender"

                    for part in msg.walk():
                        # Check for attachments
                        if part.get_content_disposition() and "attachment" in part.get_content_disposition():
                            filename = part.get_filename()
                            if filename:
                                filename = decode_header(filename)[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode()

                                # Make filename unique
                                unique_filename = f"{first_email_id.decode()}_{filename}"
                                filepath = os.path.join(working_folder, unique_filename)

                                # Save the file
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                files_with_senders[filepath] = (sender_email, first_email_id)

            mail.logout()
        except Exception as e:
            print(f"Error downloading attachments: {e}")

        return files_with_senders

    def send_email_with_attachments(self, recipient_email, pdf_filepath, csv_filepath, customer_name , customer_ref_no):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient_email
            msg['Subject'] = f" {customer_name} {customer_ref_no} Processed PDF and CSV Files"

            msg.attach(MIMEText("Attached are the processed PDF and CSV files.", "plain"))

            for file in [pdf_filepath, csv_filepath]:
                if os.path.exists(file):
                    attachment = open(file, "rb")
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
                    msg.attach(part)
                    attachment.close()

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.send_message(msg)
            server.quit()

            # print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def delete_email(self, email_id):
        try:
            # Connect to Gmail IMAP server
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_user, self.email_pass)
            mail.select("inbox")

            # Mark the email as deleted
            mail.store(email_id, "+FLAGS", "\\Deleted")

            # Permanently remove deleted emails
            mail.expunge()

            # Logout
            mail.logout()

        except Exception as e:
            print(f"Error deleting email {email_id.decode()}: {e}")

