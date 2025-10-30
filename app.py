{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww29740\viewh16320\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, render_template, request\
from email.message import EmailMessage\
import os\
import smtplib\
\
app = Flask(__name__)\
UPLOAD_FOLDER = "uploads"\
os.makedirs(UPLOAD_FOLDER, exist_ok=True)\
\
# Home page\
@app.route("/")\
def home():\
    return render_template("index.html")\
\
# Upload route\
@app.route("/upload", methods=["POST"])\
def upload():\
    name = request.form["name"]\
    email = request.form["email"]\
    company = request.form["company"]\
    files = request.files.getlist("files")\
\
    saved_files = []\
    for f in files:\
        path = os.path.join(UPLOAD_FOLDER, f.filename)\
        f.save(path)\
        saved_files.append(path)\
\
    # Send notification email to you\
    send_email_to_owner(name, email, company, saved_files)\
\
    # Send thank-you email to loan officer\
    send_confirmation_email(name, email)\
\
    return "<h2>Thank you! Your files have been submitted successfully.</h2>"\
\
# Function to email you with attachments\
def send_email_to_owner(name, email, company, attachments):\
    msg = EmailMessage()\
    msg["Subject"] = f"New Quote Submission from \{name\} (\{company\})"\
    msg["From"] = "ClearView Insurance <willbaumert@clearviewinsurance.com>"\
    msg["To"] = "willbaumert@clearviewinsurance.com"\
    msg.set_content(f"""\
New Quote Submission from \{name\} (\{company\})\
Email: \{email\}\
\
Files attached below.\
""")\
\
    for path in attachments:\
        with open(path, "rb") as f:\
            msg.add_attachment(\
                f.read(),\
                maintype="application",\
                subtype="octet-stream",\
                filename=os.path.basename(path)\
            )\
\
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:\
        smtp.starttls()\
        smtp.login("willbaumert@clearviewinsurance.com", "YOUR_APP_PASSWORD")\
        smtp.send_message(msg)\
\
# Function to email the loan officer a confirmation\
def send_confirmation_email(name, recipient_email):\
    msg = EmailMessage()\
    msg["Subject"] = "Thank you for submitting your documents to ClearView Insurance"\
    msg["From"] = "ClearView Insurance <willbaumert@clearviewinsurance.com>"\
    msg["To"] = recipient_email\
    msg.set_content(f"""\
Thank you for submitting your documents to ClearView Insurance.\
Our team will review them and reach out shortly.\
\
If you need immediate assistance, please feel free to contact me directly:\
\uc0\u55357 \u56542  (214) 389-2353\
\uc0\u9993 \u65039  willbaumert@clearviewinsurance.com\
\
\'97 ClearView Insurance\
""")\
\
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:\
        smtp.starttls()\
        smtp.login("willbaumert@clearviewinsurance.com", "YOUR_APP_PASSWORD")\
        smtp.send_message(msg)\
\
if __name__ == "__main__":\
    app.run(host="0.0.0.0", port=10000)\
}
