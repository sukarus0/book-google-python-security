from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import pandas as pd
from datetime import datetime


class TestJob:
    @staticmethod
    def run_job():
        s = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                          '10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': '127.0.0.1',
            'Referer': 'http://127.0.0.1:5000/item_search/'
        }

        # tom을 파라매터로 페이지를 호출하자
        page_url = "http://127.0.0.1:5000/item_search"
        payload = {"searchText": "tom"}
        response = s.post(page_url, headers=headers, data=payload)

        # 호출 결과를 pandas 로 파싱(소스 내 table들을 dataframe으로 만들어 줌)
        df_table_list = pd.read_html(response.text)
        # 첫번째 테이블을 가져와 화면에 현재 시간과 함께 출력한다.
        df = df_table_list[0]
        print("크롤링 시간: " + str(datetime.now()))
        print("*"*50)
        print(df)
        print("*"*50)


if __name__ == "__main__":
    # 포그라운드 스케줄러 실행 모드
    schedule = BlockingScheduler(timezone="MST", standalone=True)
    test_job = TestJob()

    # 스캐줄링 잡 등록
    schedule.add_job(test_job.run_job, "interval", seconds=5)
    try:
        schedule.start()
    except (KeyboardInterrupt):
        print("종료 처리")