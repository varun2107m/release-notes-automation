def convert_notes_to_html(notes):
    if not notes:
        return ""
    html = "<ul style='margin:0 0 8px; padding-left:20px;'>"
    for line in notes.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        elif line.startswith("•") or line.startswith("-"):
            bullet_text = line.lstrip("•-").strip()
            html += f"<li style='margin-bottom:4px;'>{bullet_text}</li>"
        else:
            html += f"</ul><p style='margin:10px 0 4px; font-weight:600; color:#1F4E79;'>{line}</p><ul style='margin:0 0 8px; padding-left:20px;'>"
    html += "</ul>"
    return html


def convert_to_html_table(data):
    if not data:
        return ""

    from collections import defaultdict

    headers = [h for h in data[0].keys() if h not in ("Category", "Section")]
    col_count = len(headers)

    html = """
    <table style='border-collapse: collapse; width:100%; font-family: Arial, sans-serif; font-size:13px;'>
    """

    # Column headers
    html += "<tr>"
    for h in headers:
        html += f"<th style='padding:8px 12px; background:#1F4E79; color:#ffffff; text-align:left; font-weight:600; border:1px solid #ccc;'>{h}</th>"
    html += "</tr>"

    # Group rows by Category
    grouped = defaultdict(list)
    order = []
    for row in data:
        cat = row.get("Category", "Other")
        if cat not in grouped:
            order.append(cat)
        grouped[cat].append(row)

    category_labels = {
        "Enhancement": "Enhancements",
        "Feature": "New Features",
        "Bug Fix": "Bug Fixes",
    }

    for i, cat in enumerate(order):
        display_cat = category_labels.get(cat, cat)
        html += f"<tr><td colspan='{col_count}' style='padding:7px 12px; background:#D6E4F0; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; border:1px solid #ccc; color:#1F4E79;'>{display_cat}</td></tr>"
        for j, row in enumerate(grouped[cat]):
            bg = "#ffffff" if j % 2 == 0 else "#F7FAFD"
            html += f"<tr style='background:{bg};'>"
            for h in headers:
                html += f"<td style='padding:7px 12px; border:1px solid #ddd; vertical-align:top;'>{row.get(h, '')}</td>"
            html += "</tr>"

    html += "</table>"
    return html


def format_email_body(notes, table_html, version, release_date, confluence_url, logo_url=""):

    logo_tag = ""
    if logo_url and logo_url.strip() and logo_url.strip().startswith("http"):
        logo_tag = f"<img src='{logo_url.strip()}' style='height:40px; display:block; margin-bottom:16px;'/>"

    html = f"""
    <html>
    <body style='margin:0; padding:0; background:#ffffff; font-family:Arial, sans-serif;'>

    <div style='width:100%; background:#ffffff;'>

        <!-- Header -->
        <div style='background:#1F4E79; padding:20px 28px;'>
            {logo_tag}
            <h2 style='margin:0; color:#ffffff; font-size:18px; font-weight:600;'>
                Planned Production Release — v{version}
            </h2>
            <p style='margin:4px 0 0; color:#BDD7EE; font-size:13px;'>Scheduled: {release_date}</p>
        </div>

        <!-- Body -->
        <div style='padding:24px 28px; color:#333333; font-size:14px; line-height:1.6;'>

            <p style='margin:0 0 16px;'>Hi All,</p>

            <p style='margin:0 0 20px;'>
                This is to inform you that the upcoming planned release of version <b>v{version}</b>
                is scheduled for <b>{release_date}</b>. Please find the key highlights and release data below.
            </p>

            <!-- Release Data Table -->
            <div style='margin:0 0 20px; overflow-x:auto;'>
                {table_html}
            </div>

            <!-- Notes -->
            <h3 style='margin:0 0 8px; font-size:14px; color:#1F4E79; border-bottom:2px solid #1F4E79; padding-bottom:4px;'>Notes</h3>
            <ul style='margin:0 0 20px; padding-left:20px; font-size:13px; color:#444;'>
                <li style='margin-bottom:4px;'>Zero downtime expected. Deployment starts at 10:00 PM.</li>
                <li style='margin-bottom:4px;'>Feature flags enabled on request.</li>
            </ul>

            <!-- Confluence Button -->
            <a href="{confluence_url}"
               style="display:inline-block; padding:9px 18px; background-color:#0052CC; color:#ffffff;
                      text-decoration:none; border-radius:4px; font-size:13px; font-weight:600;">
                View Confluence Page &rarr;
            </a>

        </div>

        <!-- Footer -->
        <div style='background:#f9f9f9; border-top:1px solid #e0e0e0; padding:16px 28px;'>
            <p style='margin:0; font-size:13px; color:#555;'>Thanks &amp; Regards,</p>
            <p style='margin:2px 0 0; font-size:13px; font-weight:700; color:#1F4E79;'>POD Team</p>
        </div>

    </div>

    </body>
    </html>
    """

    return html


















