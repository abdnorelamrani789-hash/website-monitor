import os
import requests
import smtplib
from email.mime.text import MIMEText
import csv
from datetime import datetime, timedelta

# =========================
# Environment Variables
# =========================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

URLS_TO_MONITOR = [
    "https://example.com",
    "https://github.com",
    "https://stackoverflow.com"
]

CSV_FILE = "uptime_report.csv"

# =========================
# إرسال إيميل بصياغة احترافية
# =========================
def send_email(subject, message, url=None, status=None):
    header = f"Bonjour,\n\n"
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
# تحديث CSV
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
# فحص المواقع
# =========================
def check_sites():
    for url in URLS_TO_MONITOR:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                send_email(
                    subject=f"⚠️ Site Down: {url}",
                    message="Un problème a été détecté sur le site.",
                    url=url,
                    status=f"DOWN ({res.status_code})"
                )
                update_csv(url, f"DOWN ({res.status_code})")
            else:
                print(f"{url} is up ✅")
                update_csv(url, "UP")
        except Exception as e:
            send_email(
                subject=f"⚠️ Site Down: {url}",
                message="Le site ne répond pas à la requête HTTP.",
                url=url,
                status="DOWN (Exception)"
            )
            update_csv(url, f"DOWN (Exception)")

# =========================
# تقرير يومي
# =========================
def send_daily_report():
    if not os.path.isfile(CSV_FILE):
        print("No CSV file found for daily report.")
        return

    now = datetime.now()
    yesterday = now - timedelta(days=1)
    uptime_summary = {}

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ts = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
            if ts.date() != yesterday.date():
                continue
            url = row['url']
            status = row['status']
            uptime_summary.setdefault(url, {"up":0, "total":0})
            uptime_summary[url]["total"] +=1
            if status.startswith("UP"):
                uptime_summary[url]["up"] +=1

    message_lines = [f"Rapport uptime du {yesterday.date()}:"]
    for url, data in uptime_summary.items():
        percent = (data["up"]/data["total"]*100) if data["total"]>0 else 0
        message_lines.append(f"{url}: {percent:.1f}% uptime")

    send_email(f"📊 Daily Uptime Report: {yesterday.date()}", "\n".join(message_lines))

# =========================
# Main
# =========================
if __name__ == "__main__":
    check_sites()
    # التقرير اليومي يتم تشغيله من workflow
