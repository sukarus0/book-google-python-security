from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import pyodbc
import json


def get_cursor():
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
    return cursor


def line_plot():
    # 최근 5개의 데이터를 가져온다
    search_sql = "select top 5 name, previous_score, " \
                 "current_score, pass_yn " \
                 "from test_result (nolock) order by seqno desc"

    cursor.execute(search_sql)
    result_rows = cursor.fetchall()

    name = []
    previous_score = []
    current_score = []
    color = []

    for result_row in result_rows:
        name.append(result_row[0])
        previous_score.append(result_row[1])
        current_score.append(result_row[2])
        if result_row[3] == "Y":
            color.append("LightSkyBlue")
        else:
            color.append("red")

    # 과거 건 부터 보여주기 위해서 순서를 바꿈
    name.reverse()
    previous_score.reverse()
    current_score.reverse()
    color.reverse()

    # pyplot 그래프용 데이터 만듬
    data = [
        go.Scatter(
            x=name,
            y=current_score,
            type='scatter',
            mode='markers',
            marker=dict(
                color=color,
                size=20,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            name='현재 점수'
        ),
        go.Scatter(
            x=name,
            y=previous_score,
            opacity=0.8,
            type="scatter",
            mode='markers',
            marker=dict(
                color=color,
                size=15,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            name='지난 점수'
        )

    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


cursor = get_cursor()
app = Flask(__name__)


@app.route('/show_exam_result')
def index():
    line = line_plot()
    return render_template('monitoring_graph.html', plot=line)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)