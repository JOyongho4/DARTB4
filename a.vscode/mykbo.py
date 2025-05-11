from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# 크롬 설정
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://mykbostats.com/players/158")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.sortable tbody tr"))
)

rows = driver.find_elements(By.CSS_SELECTOR, "table.sortable tbody tr")

# 디버깅 + 필터링
data = []
for i, row in enumerate(rows):
    cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
    if len(cols) != 16:
        print(f"⚠️ Skipping row {i}: has {len(cols)} columns → {cols}")
    else:
        data.append(cols)

columns = ["Date", "Opp", "Role", "Dec", "ERA", "WHIP", "IP", "NP", "R", "ER", "H", "HR", "SO", "BB", "HB", "GS"]
df = pd.DataFrame(data, columns=columns)

print(df)
driver.quit()

df.to_csv("/Users/joyongho/Desktop/mykbo_game_stats_2024.csv", index=False, encoding="utf-8-sig")
print(df)

