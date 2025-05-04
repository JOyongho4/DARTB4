import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL 설정 (예: 류현진 선수의 일별 기록 페이지)
url = 'https://statiz.sporki.com/player/?m=day&p_no=15535'

# User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# 요청
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

# 테이블 찾기
table = soup.find('table')

# pandas DataFrame으로 변환
df = pd.read_html(str(table))[0]

# 확인
print(df.head())

# 저장 (선택)

df.to_csv('/Users/joyongho/Desktop/크롤링/s.csv', index=False)
