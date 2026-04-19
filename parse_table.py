from bs4 import BeautifulSoup

def parse_confluence_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return []

    rows = table.find_all("tr")
    parsed_data = []

    for i, row in enumerate(rows):
        cols = row.find_all(["td", "th"])
        col_text = [c.get_text(strip=True) for c in cols]

        if not col_text:
            continue

        if i == 0 or (len(col_text) > 1 and "module" in col_text[1].lower()):
            continue

        if len(col_text) < 5:
            continue

        category = col_text[0]
        module = col_text[1]
        submodule = col_text[2]
        users = col_text[3]
        description = col_text[4]

        parsed_data.append({
            "Category": category,
            "Section": category,  # backward compatibility
            "Module": module,
            "SubModule": submodule,
            "Users": users,
            "Description": description
        })

    return parsed_data





