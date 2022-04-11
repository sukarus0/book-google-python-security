import pyodbc
import pandas as pd
import re
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class DetectedPayload:
    detected_type: str = ""
    detected_values: list[str] = field(default_factory=list)


@dataclass
class Column:
    column_name: str = ""
    detected_payloads: list[DetectedPayload] = field(default_factory=list)


@dataclass
class Table:
    table_name: str = ""
    columns: list[Column] = field(default_factory=list)


@dataclass
class Tables:
    tables: list[Table] = field(default_factory=list)


def get_cursor_and_connection():
    server = 'localhost'
    database = 'mytest'
    username = 'pyuser'
    password = 'Test1234%^&'

    mssql_conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=" + server + "; PORT=1433;DATABASE=" + database + "; \
        UID=" + username + "; PWD=" + password)

    cursor = mssql_conn.cursor()
    return cursor, mssql_conn

cursor, mssql_conn = get_cursor_and_connection()


# sysobjects 를 이용해 모든 테이블 이름들을 가져와 tables 객체에 넣음
def get_table_names():
    tables = Tables()
    sql_get_tables = "SELECT name FROM sysobjects WHERE xtype='U'"
    cursor.execute(sql_get_tables)
    rows = cursor.fetchall()

    for row in rows:
        table = Table()
        table.table_name = row[0]
        tables.tables.append(table)
    return tables


# 해당 테이블의 컬럼 이름을 얻어와 table 객체의 colunms 프로퍼티에 넣음
def get_column_names(table):
    column_names = []
    
    sql_get_columns = "SELECT column_name FROM " \
                      "INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?"
    cursor.execute(sql_get_columns, table.table_name)
    rows = cursor.fetchall()
    
    for row in rows:
        column = Column()
        column.column_name = row[0]
        table.columns.append(column)
    return table


# select 뒤에 넣을 컬럼 항목 만들기(a, b, c 이런 식으로 만들어진다)
def make_column_query(columns):
    column_query = ''

    for column in columns:
        column_query = column_query + column.column_name + ','
    column_query = column_query[:-1]
    return column_query


# 테이블에서 10 row를 가져와 Panda Dataframe에 담는다
def make_dataframe(table):
    column_query = make_column_query(table.columns)
    
    query1 = "SELECT top 10 " + column_query + " FROM " \
             + table.table_name + "(nolock)"
    df = pd.read_sql(query1, mssql_conn)
    return df


# 핸드폰 패턴을 찾아서 Column 객체의 detected_payloads 속성에 넣는다.
def check_personal_pattern(data_cells, column):
    mobile_tel_pattern = "(01[016789][-~.\s]?[0-9]{3,4}[-~.\s]?[0-9]{4})"

    detected_payload = DetectedPayload()

    for data_cell in data_cells:
        data_cell = str(data_cell)
        match_mobile_tel = re.search(mobile_tel_pattern, data_cell)

        if match_mobile_tel:
            detected_payload.detected_values.append(match_mobile_tel.group(1))

    if len(detected_payload.detected_values) > 0:
        detected_payload.detected_type = "mobile"
        column.detected_payloads.append(detected_payload)


if __name__ == "__main__":
    tables = get_table_names()

    # 구조 파악 및 검사 하기
    print("-"*30 + "체크 테이블" + "-"*30)
    for table in tables.tables:
        print("[" + table.table_name + "]")

        table = get_column_names(table)
        my_dataframe = make_dataframe(table)

        # 컬럼 이름을 가져와서
        for column in table.columns:
            # 컬럼 이름에 해당하는 수직 row 데이터를 가져온다.
            data_cells = my_dataframe[column.column_name].tolist()
            check_personal_pattern(data_cells, column)

    # 검출 결과 출력
    print("-"*30 + "검출 결과" + "-"*30)
    for table in tables.tables:
        for column in table.columns:
            if len(column.detected_payloads) > 0:
                for detected_payload in column.detected_payloads:
                    print("테이블:컬렴 - " + table.table_name
                          + ":" + column.column_name)
                    print("타입:검출 값 - " + detected_payload.detected_type
                          + ":" + str(detected_payload.detected_values))