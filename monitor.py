import os
import csv
from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText

# =========================
# المتغيرات
# =========================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Gmail ديالك
EMAIL_PASS = os.getenv("EMAIL_PASS")        # App Password
EMAIL_TO = os.getenv("EMAIL_TO")            # البريد المرسل ليه

URLS_TO_MONITOR = [
    "https://example.com",
    "https://github.com",
    "https://stackoverflow.com"
]

DATA_FOLDER = "data"
CSV_FILE = os.path.join(DATA_FOLDER, "uptime_report.csv")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# =========================
# دالة إرسال الإيميل
# =========================
def send_email(subject, message, url=None, status=None):
    header = "Bonjour,\n\n"
    body = f"{message}\n"
    if url and status:
        body += f"\nDétails:\nSite: {url}\nStatut: {status}\n"
    footer = "\nCordialement,\nService de Monitoring de Sites Web"
    full_message = header + body + footer

    msg = MIMEText(full_message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_TO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASS)
        server.send_message(msg)

    print(f"Email sent: {subject}")

# =========================
# دالة تحديث CSV
# =========================
def update_csv(url, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "url", "status"])
        writer.writerow([now, url, status])

# =========================
# مراقبة المواقع
# =========================
def check_sites():
    for url in URLS_TO_MONITOR:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                send_email(f"⚠️ Site Down: {url}", "Un problème détecté.", url, f"DOWN ({res.status_code})")
                update_csv(url, f"DOWN ({res.status_code})")
            else:
                print(f"{url} is up ✅")
                update_csv(url, "UP")
        except Exception as e:
            send_email(f"⚠️ Site Down: {url}", "Le site ne répond pas.", url, "DOWN (Exception)")
            update_csv(url, "DOWN (Exception)")

# =========================
# Main
# =========================
if __name__ == "__main__":
    check_sites()
