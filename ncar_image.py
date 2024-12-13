from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# 브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# 엑셀 파일 생성
xlsx = Workbook()
list_sheet = xlsx.active
list_sheet.title = "output"
list_sheet.append(['Title', 'Image URL'])

def click_more_button(driver):
    """더보기 버튼을 클릭하여 모든 데이터를 로드하는 함수"""
    try:
        while True:
            # 더보기 버튼이 나타나면 클릭
            more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btnInfoMore"))
            )
            more_button.click()
            print("더보기 버튼 클릭")
            time.sleep(3)  

    except Exception:
        print("더보기 버튼 없음 또는 모든 데이터 로드 완료")

def crawl_car_list(driver):
    """자동차 목록에서 제목과 이미지 URL을 크롤링하는 함수"""
    try:
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 자동차 목록 가져오기
        car_items = soup.find("ul", {"id": "list_mocha"}).find_all("li")
        for car in car_items:
            # 제목 추출
            title_tag = car.find("strong", {"class": "tit_car"})
            title = title_tag.get_text(strip=True) if title_tag else "제목 없음"

            # 이미지 URL 추출
            img_tag = car.find("img", {"class": "thumb_g"})
            img_url = img_tag["src"] if img_tag else "이미지 없음"

            # 출력 및 엑셀 저장
            print(f"Title: {title}, Image URL: {img_url}")
            list_sheet.append([title, img_url])

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

# 크롤링 실행
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL 이동
    url = 'http://www.encar.com/mocha.do?mnfccd=001&mdlgroupcd=&mdlcd=&year=&mochaYn=&method='
    driver.get(url)

    # 더보기 버튼 클릭하여 모든 데이터 로드
    click_more_button(driver)

    # 크롤링 수행
    crawl_car_list(driver)

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 브라우저 종료
    driver.quit()

    # 엑셀 저장
    file_name = "image_url.xlsx"
    xlsx.save(file_name)
    print(f"엑셀 파일 저장 완료: {file_name}")
