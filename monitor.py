# monitor.py
import requests
import pandas as pd
import yagmail
from datetime import datetime
import os

# --- إعداد مجلد البيانات ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_FILE = os.path.join(DATA_DIR, "uptime_report.csv")

# --- لائحة المواقع المراد مراقبتها ---
websites = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://example.com"
]

# --- قراءة التقرير السابق أو إنشاء DataFrame جديد ---
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "url", "status"])

# --- إعداد الإيميل ---
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = os.environ["EMAIL_TO"]
yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASS)

# --- مراقبة المواقع ---
for site in websites:
    try:
        r = requests.get(site, timeout=10)
        if r.status_code == 200:
            status = "Up ✅"
        else:
            status = f"Down ⚠️ (HTTP {r.status_code})"
    except Exception as e:
        status = f"Down ⚠️ ({e})"
    
    # --- إرسال إيميل احترافي إذا الموقع طاح ---
    if "Down" in status:
        subject = f"[ALERT] Site Down: {site}"
        body = f"""
🔹 Website: {site}
🔹 Status: {status}
🔹 Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Action Suggestions:
1. Verify your server is online and responding.
2. Check DNS and hosting configuration.
3. Inspect server logs for errors.
4. Notify your technical team if downtime persists.

This is an automated monitoring alert. Please do not reply to this email.
"""
        yag.send(to=EMAIL_TO, subject=subject, contents=body)
    
    # --- تحديث التقرير ---
    df = pd.concat([df, pd.DataFrame([{
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "url": site,
        "status": status
    }])], ignore_index=True)

# --- حفظ CSV ---
df.to_csv(CSV_FILE, index=False)
print("Monitoring done. CSV updated and emails sent if needed.")
