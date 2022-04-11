from json_logic import jsonLogic
from dataclasses import dataclass, field, asdict
from threading import Thread
from statistics import mean
from enum import Enum
import queue
import pyodbc


class Const(str, Enum):
    END_MARK = "END"
    PASS = "Y"
    FAIL = "N"


@dataclass
class ExamScore:
    name: str = ""
    previous_score: int = 0
    current_score: int = 0
    mean: float = 0.0


@dataclass
class ExamScores:
    exam_scores: list[ExamScore] = field(default_factory=list)


def get_cursor_and_connection():
    # 연결 문자열을 세팅함
    server = 'localhost'
    database = 'mytest'
    username = 'pyuser'
    password = 'Test1234%^&'

    # 데이터베이스에 연결함
    mssql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + server + '; PORT=1433;DATABASE=' + database + '; \
        UID=' + username + '; PWD=' + password)

    # 커서를 생성함
    cursor = mssql_conn.cursor()
    return mssql_conn, cursor


mssql_conn, cursor = get_cursor_and_connection()


# 시험 성적 데이터를 만들어 낸다.
def make_exam_data():
    sample_exams = [
        ["tom", 90, 80],
        ["jane", 40, 50],
        ["lucy", 100, 20],
        ["bread", 100, 100],
        ["sam", 90, 80],
    ]

    exam_scores = ExamScores()

    for sample_exam in sample_exams:
        exam_score = ExamScore()
        exam_score.name = sample_exam[0]
        exam_score.previous_score = sample_exam[1]
        exam_score.current_score = sample_exam[2]
        exam_score.mean = mean([sample_exam[1], sample_exam[2]])
        exam_scores.exam_scores.append(exam_score)

    return exam_scores


# 룰을 이용해서 결과를 판단한다
# (현재 성적이 80 이상이고, 전 시험을 포함한 평균이 50 이상)
def check_exam(exam_score):
    rule = {"and": [
        {">=": [{"var": "current_score"}, 80]},
        {">=": [{"var": "mean"}, 50]},
    ]}

    exam_dict = asdict(exam_score)
    rule_result = jsonLogic(rule, exam_dict)

    if rule_result:
        return Const.PASS.value
    else:
        return Const.FAIL.value


q = queue.Queue()

# 시험 성적을 큐에 넣는다.
def producer(queue):
    exam_scores = make_exam_data()

    for exam_score in exam_scores.exam_scores:
        queue.put(exam_score)

    queue.put(Const.END_MARK.value)


# 시험 성적과 합격 결과를 테이블에 넣는다.
def insert_data(sample_exam, pass_yn):
    sql = "insert into test_result(name, previous_score, " \
          "current_score, pass_yn) " \
          "values (?, ?, ?, ?)"
    parameters = [sample_exam.name, sample_exam.previous_score,
                  sample_exam.current_score, pass_yn]
    cursor.execute(sql, parameters)
    mssql_conn.commit()


# 큐에서 시험 성적을 가져와 합격 여부를 판단 후 테이블에 결과를 넣는다.
def consumer(queue):
    while True:
        sample_exam = queue.get()
        if sample_exam != Const.END_MARK:
            queue.task_done()
            print(asdict(sample_exam))

            # 룰 엔진에 데이터를 전달하여 결과를 받는다.
            pass_yn = check_exam(sample_exam)
            print(f"롤 체크결과: {pass_yn}")

            # 결과와 함께 데이터를 테이블에 넣는다.
            insert_data(sample_exam, pass_yn)
        else:
            print("큐가 다 처리되었습니다")
            queue.task_done()
            break


if __name__ == '__main__':
    # 큐에 데이터를 넣는 producer 와 cusumer 를 각각 쓰레드로 띄운다.
    threads = [Thread(target=producer, args=(q,)),
               Thread(target=consumer, args=(q,)),]

    for thread in threads:
        thread.start()

    # 큐가 완료될 때까지 기다린다.
    q.join()
