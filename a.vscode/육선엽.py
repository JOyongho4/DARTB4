from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# 크롬 드라이버 옵션 설정
options = Options()
options.add_argument("--headless")  # 창 안 띄움
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--lang=ko-KR")  # 한글 페이지 대응

# ChromeDriver 경로: 본인 환경에 맞게 수정
driver = webdriver.Chrome(options=options)

# URL 열기
url = "https://statiz.sporki.com/player/?m=playlog&p_no=15864&pos=pitching&year=2024&si=1"
driver.get(url)

# 페이지 로딩 대기
time.sleep(5)

# 페이지 소스 추출
soup = BeautifulSoup(driver.page_source, "html.parser")

# 테이블 찾기
table = soup.find("table", {"class": "table table-striped"})

# 데이터 수집
if table:
    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        rows.append([td.get_text(strip=True) for td in tr.find_all("td")])
    
    df = pd.DataFrame(rows, columns=headers)
    
    # 저장
    df.to_csv("/Users/joyongho/Desktop/크롤링/s.csv", index=False, encoding='utf-8-sig')
    print("✅ CSV 저장 완료")
else:
    print("❌ 테이블을 찾을 수 없습니다.")

driver.quit()
