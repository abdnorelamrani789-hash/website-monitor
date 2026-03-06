import requests
import yagmail
from datetime import datetime

# --- لائحة المواقع المراد مراقبتها ---
websites = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://example.com"
]

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

print("Monitoring done. Emails sent if needed.")
