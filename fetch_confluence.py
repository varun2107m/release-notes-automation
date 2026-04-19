import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

def fetch_confluence_page():

    url = os.getenv("CONFLUENCE_PAGE_URL")
    token = os.getenv("CONFLUENCE_API_TOKEN")
    email = os.getenv("CONFLUENCE_EMAIL")

    if not url or url.strip() == "":
        raise ValueError("❌ Missing CONFLUENCE_PAGE_URL in .env file.")

    if not token or token.strip() == "":
        raise ValueError("❌ Missing CONFLUENCE_API_TOKEN in .env file.")

    if not email or email.strip() == "":
        raise ValueError("❌ Missing CONFLUENCE_EMAIL in .env file.")

    try:
        response = requests.get(url, auth=HTTPBasicAuth(email, token))

        if response.status_code != 200:
            raise Exception(
                f"❌ Failed to fetch Confluence page. "
                f"Status Code: {response.status_code}, Response: {response.text}"
            )

        return response.text

    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ Error while calling Confluence API: {str(e)}")
    
    



    




