import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1) undetected-chromedriver로 드라이버 실행
driver = uc.Chrome()
wait = WebDriverWait(driver, 10)

# 2) 크롤링할 투수 선수명→페이지ID 매핑
players = {
    "박상원": 1548,
    "한승혁": 327
    # 필요한 선수명:ID 추가
}
years = ["2024", "2023", "2022"]
all_data = []

for name, pid in players.items():
    # 3) 해당 선수 페이지 열기
    driver.get(f"https://mykbostats.com/players/{pid}")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ui.dropdown")))

    for year in years:
        # 4) 사용자 입력: '없음' 입력 시 스킵
        resp = input(f"▶ [{name}] {year} 데이터가 없으면 '없음'을, 아니면 엔터를 눌러주세요… ")
        if resp.strip() == "없음":
            print(f"  - [{name}] {year} 스킵")
            continue

        time.sleep(0.5)  # 렌더 안정화

        # 5) "Show More" 버튼이 있으면 모두 클릭
        while True:
            btns = driver.find_elements(By.CSS_SELECTOR, 'a[phx-click="show_all"]')
            if not btns:
                break
            driver.execute_script("arguments[0].click();", btns[0])
            time.sleep(0.2)

        # 6) 테이블 스크래핑 (투수: 16컬럼)
        rows = driver.find_elements(By.CSS_SELECTOR, "table.sortable tbody tr")
        year_rows = []
        for row in rows:
            cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            if len(cols) == 16:
                year_rows.append(cols)

        # 7) 데이터가 없으면 "없음" 한 줄 추가, 있으면 모두 추가
        if not year_rows:
            all_data.append([name, year] + ["없음"] * 16)
        else:
            for cols in year_rows:
                all_data.append([name, year] + cols)

# 8) 드라이버 종료
driver.quit()

# 9) DataFrame 생성 및 저장
columns = [
    "PlayerName", "Year", "Date", "Opp", "Role", "Dec", "ERA", "WHIP",
    "IP", "NP", "R", "ER", "H", "HR", "SO", "BB", "HB", "GS"
]
df = pd.DataFrame(all_data, columns=columns)
df.to_csv("mykbo_pitchers_by_name.csv", index=False, encoding="utf-8-sig")

print("✅ Saved mykbo_pitchers_by_name.csv")