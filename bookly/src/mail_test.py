import httpx
from src.config import Config

# Make sure MAILTRAP_INBOX_ID and MAILTRAP_API_TOKEN are defined in src/config.py
URL = f"https://mailtrap.io{Config.MAILTRAP_INBOX_ID}"

async def send_mailtrap_api(recipients: list[str], subject: str, html_content: str):
    """Sends an email via Mailtrap Sandbox REST API to bypass Render port blocks"""
    
    headers = {
        "Authorization": f"Bearer {Config.MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Mailtrap Sandbox handles single user testing objects. 
    # We grab the first index of your recipient list.
    target_email = recipients[0] if recipients else "test@example.com"
    
    payload = {
        "from": {"email": Config.MAIL_FROM, "name": "FastAPI Sandbox Auth"}, 
        "to": [{"email": target_email}],
        "subject": subject,
        "html": html_content
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, headers=headers, json=payload)
            response.raise_for_status() 
        except httpx.HTTPStatusError as exc:
            print(f"Mailtrap Sandbox API Error: {exc.response.status_code} - {exc.response.text}")
        except Exception as e:
            print(f"Unexpected sandbox email delivery failure: {e}")
