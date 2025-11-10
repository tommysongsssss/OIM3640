import time
import pandas as pd
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# ================== CONFIG ==================
QUERY = "Eli Lilly"
MAX_RECORDS = 500
OUTPUT_XLSX = Path("/Users/thomassong0604/Desktop/QTM Final Project/eli_lilly_500 (1).xlsx")
URL = "https://ppubs.uspto.gov/pubwebapp/"
# ============================================

# start browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def wait_xpath(xp, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xp))
    )

def click_xpath(xp, timeout=20):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xp))
    )
    driver.execute_script("arguments[0].click();", el)
    return el

try:
    # 1. open site
    driver.get(URL)

    # 2. wait for the search box on the LEFT
    # in your screenshot it's a textarea with "Enter query text"
    search_box = wait_xpath("//textarea[contains(.,'') or @aria-label='Enter query text' or @title='Enter query text']")
    search_box.clear()
    search_box.send_keys(QUERY)

    # 3. click the Search button at bottom of left panel
    # it literally says 'Search'
    # sometimes it’s off-screen inside the panel, so scroll first
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", search_box.find_element(By.XPATH, "./ancestor::div[1]"))
    click_xpath("//button[normalize-space()='Search']")

    # 4. wait for the Search Results table to appear at the bottom
    time.sleep(2)  # let it render
    # grab ANY table in the results area
    def get_results_table():
        tables = driver.find_elements(By.XPATH, "//div[contains(@class,'search')]//table | //table")
        return tables[0] if tables else None

    table = get_results_table()
    if table is None:
        raise RuntimeError("Didn't find the Search Results table — make sure the bottom panel is open.")

    data_rows = []
    seen = set()

    while len(data_rows) < MAX_RECORDS:
        table = get_results_table()
        if not table:
            break

        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header
        if not rows:
            break

        for idx, row in enumerate(rows):
            if len(data_rows) >= MAX_RECORDS:
                break

            # click the row so the right “Document Viewer” shows the doc
            try:
                driver.execute_script("arguments[0].click();", row)
            except StaleElementReferenceException:
                table = get_results_table()
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]
                driver.execute_script("arguments[0].click();", rows[idx])

            # wait a bit for viewer to update
            time.sleep(1.3)

            # read columns from the row itself
            tds = row.find_elements(By.TAG_NAME, "td")
            pub_no = tds[4].text.strip() if len(tds) > 4 else ""
            date_pub = tds[5].text.strip() if len(tds) > 5 else ""
            title = tds[7].text.strip() if len(tds) > 7 else ""

            if pub_no and pub_no in seen:
                continue
            seen.add(pub_no)

            # grab the document viewer text (the green panel on the right)
            doc_text = ""
            try:
                doc_viewer = driver.find_element(By.XPATH, "//div[contains(@class,'document') or contains(@id,'doc')]")
                doc_text = doc_viewer.text
            except NoSuchElementException:
                pass

            # pull abstract
            abstract = ""
            if "Abstract" in doc_text:
                abstract = doc_text.split("Abstract", 1)[1].split("BACKGROUND", 1)[0].strip()

            # pull CPC CURRENT block
            cpc = ""
            if "CPC CURRENT" in doc_text:
                cpc_block = doc_text.split("CPC CURRENT", 1)[1]
                cpc_lines = cpc_block.splitlines()[0:10]
                cpc = "; ".join([l.strip() for l in cpc_lines if l.strip()])

            data_rows.append({
                "Publication Number": pub_no,
                "Date Published": date_pub,
                "Title": title,
                "Abstract / Description": abstract,
                "CPC Codes": cpc,
                "Document ID": tds[3].text.strip() if len(tds) > 3 else "",
                "Family ID": tds[6].text.strip() if len(tds) > 6 else "",
                "URL (USPTO)": URL,
            })
            print(f"Got {len(data_rows)} / {MAX_RECORDS}")

        # if the USPTO UI has pagination, we could click "Next" here.
        # your screenshot shows 1–500 already, so break.
        break

    # 5. save to Excel
    df = pd.DataFrame(data_rows)
    df.to_excel(OUTPUT_XLSX, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_XLSX}")

finally:
    driver.quit()
