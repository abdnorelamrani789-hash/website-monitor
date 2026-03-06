import os
import requests
import time
import smtplib
from email.mime.text import MIMEText

# =========================
# المتغيرات من GitHub Secrets
# =========================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # bellinotion@gmail.com
EMAIL_PASS = os.getenv("EMAIL_PASS")        # App Password 16 chars
EMAIL_TO = os.getenv("EMAIL_TO")            # abdnorelamrani789@gmail.com

# المواقع لي بغينا نراقبو
URLS_TO_MONITOR = [
    "https://example.com",
    "https://github.com",
    "https://stackoverflow.com"
]

# وقت الانتظار بين كل محاولة (بالثواني)
CHECK_INTERVAL = 10  # هنا غير للتجربة، workflow غادي يشغل كل 30 دقيقة

# =========================
# إرسال إيميل
# =========================
def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_TO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASS)
        server.send_message(msg)
    print(f"Email sent: {subject}")

# =========================
# فحص المواقع
# =========================
def check_sites():
    for url in URLS_TO_MONITOR:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                send_email(f"⚠️ Site Down: {url}", f"Le site {url} retourne le code {res.status_code}.")
            else:
                print(f"{url} is up ✅")
        except Exception as e:
            send_email(f"⚠️ Site Down: {url}", f"Le site {url} ne répond pas. Erreur: {e}")

# =========================
# تشغيل البوت
# =========================
if __name__ == "__main__":
    check_sites()
