from flask import Flask, render_template, request
from email.message import EmailMessage
import os
import smtplib

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    name = request.form["name"]
    email = request.form["email"]
    company = request.form["company"]
    files = request.files.getlist("files")

    saved_files = []
    for f in files:
        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(file_path)
        saved_files.append(file_path)

    send_email_to_owner(name, email, company, saved_files)
    send_confirmation_email(name, email)

    return "<h2>Thank you! Your files have been submitted successfully.</h2>"

def send_email_to_owner(name, email, company, attachments):
    msg = EmailMessage()
    msg["Subject"] = f"New Quote Submission from {name} ({company})"
    msg["From"] = "ClearView Insurance <willbaumert@clearviewinsurance.com>"
    msg["To"] = "willbaumert@clearviewinsurance.com"
    msg.set_content(f"""
New Quote Submission from {name} ({company})
Email: {email}

Files attached below.
""")

    for file_path in attachments:
        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file_path)
            )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("willbaumert@clearviewinsurance.com", "YOUR_APP_PASSWORD")
        smtp.send_message(msg)

def send_confirmation_email(name, recipient_email):
    msg = EmailMessage()
    msg["Subject"] = "Thank you for submitting your documents to ClearView Insurance"
    msg["From"] = "ClearView Insurance <willbaumert@clearviewinsurance.com>"
    msg["To"] = recipient_email
    msg.set_content(f"""
Thank you for submitting your documents to ClearView Insurance.
Our team will review them and reach out shortly.

If you need immediate assistance, please feel free to contact me directly:
📞 (214) 389-2353
✉️ willbaumert@clearviewinsurance.com

— ClearView Insurance
""")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("willbaumert@clearviewinsurance.com", "YOUR_APP_PASSWORD")
        smtp.send_message(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
