import streamlit as st
import os
from dotenv import load_dotenv
from collections import defaultdict

from fetch_confluence import fetch_confluence_page
from parse_table import parse_confluence_table
from ai_transform import generate_release_notes
from email_formatter import format_email_body, convert_to_html_table
from send_email import send_email
from google_sheets import get_latest_release

load_dotenv()

st.set_page_config(page_title="Release Notes Tool", layout="wide")

st.title("📦 Release Notes Automation")

# -------------------------------
# LOAD CONFIG FROM GOOGLE SHEET
# -------------------------------
try:
    release_config  = get_latest_release()
    version         = release_config["version"]
    release_date    = release_config["release_date"]
    confluence_url  = release_config["confluence_url"]
    recipients      = release_config["recipients"]
    approval_status = release_config["approval_status"]

    st.info(f"📋 Loaded from Google Sheet — v{version} | {release_date} | Approval: **{approval_status}**")

except Exception as e:
    st.error(f"❌ Could not load from Google Sheet: {e}")
    st.stop()

# -------------------------------
# STEP 1: GENERATE
# -------------------------------
if st.button("🚀 Generate Release Notes"):

    # Set Confluence URL from sheet
    page_url = os.getenv("CONFLUENCE_PAGE_URL", "")
    if confluence_url and confluence_url.strip():
        page_url = confluence_url.strip()
        if "?expand" not in page_url:
            page_url += "?expand=body.storage"
        os.environ["CONFLUENCE_PAGE_URL"] = page_url

    with st.spinner("Fetching Confluence page..."):
        html = fetch_confluence_page()

    with st.spinner("Parsing table..."):
        parsed_data = parse_confluence_table(html)
        cleaned_data = [item for item in parsed_data if item.get("Module") != "N/A"]

    table_html = convert_to_html_table(cleaned_data)

    # Store directly in session state
    st.session_state["edited_notes"] = ""
    st.session_state["table"] = table_html

    st.success("✅ Release notes generated!")
    st.rerun()

# -------------------------------
# STEP 2: EDIT
# -------------------------------
if "edited_notes" in st.session_state:

    st.subheader("✏️ Review & Edit")

    updated_notes = st.text_area(
        "Edit Release Notes",
        value=st.session_state["edited_notes"],
        height=250,
        key="notes_editor"
    )

# -------------------------------
# STEP 3: PREVIEW
# -------------------------------
if "edited_notes" in st.session_state:

    notes_to_preview = st.session_state.get("notes_editor", st.session_state["edited_notes"])

    st.subheader("👀 Email Preview")

    logo_url = os.getenv("LOGO_URL", "")

    preview_html = format_email_body(
        notes_to_preview,
        st.session_state["table"],
        version,
        release_date,
        confluence_url,
        logo_url
    )

    st.session_state["preview_html"] = preview_html

    st.components.v1.html(preview_html, height=600, scrolling=True)

# -------------------------------
# STEP 4: SEND EMAIL (with approval check)
# -------------------------------
if "preview_html" in st.session_state:

    if approval_status.lower() == "approved":
        if st.button("✅ Approve & Send Email"):
            send_email(
                f"[POD][Planned Prod Release]|| FV {version} – {release_date}",
                st.session_state["preview_html"],
                recipients
            )
            st.success("🎉 Emails sent successfully!")
    else:
        st.warning(f"⏳ Approval Status is **'{approval_status}'**. Ask your approver to update it to **'Approved'** in the Google Sheet before sending.")
