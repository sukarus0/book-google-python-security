from flask import Flask, render_template, request
import pyodbc


def get_cursor():
    # 연결 문자열을 세팅함
    server = "localhost"
    database = "mytest"
    username = "pyuser"
    password = "Test1234%^&"

    # 데이터베이스에 연결함
    mssql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER='+server+'; PORT=1433;DATABASE='+database+'; \
        UID='+username+'; PWD='+ password)

    # 커서를 생성함
    cursor = mssql_conn.cursor()    
    return cursor


cursor = get_cursor() 

# flask 웹서버를 실행함
app = Flask(__name__)

@app.route("/item_search", methods=["GET", "POST"])
def item_search():
    search_text = ""
    
    if request.method == "POST":
        search_text = request.form["searchText"]
    
    search_sql = "{CALL Select_Buy_Items (?)}"

    cursor.execute(search_sql, search_text)  
    result_rows = cursor.fetchall()

    return render_template("sql_injection.html", rows = result_rows,
        search_text = search_text, sql_query = search_sql)


# 이 웹서버는 127.0.0.1 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)