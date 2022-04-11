from flask import Flask, make_response
import pandas as pd
import numpy as np
import io

# flask 웹서버를 실행 합니다.
app = Flask(__name__)


@app.route("/excel_down", methods=['GET'])
def excel_down():
    # pandas 객체를 하나 만든다.
    data_frame = pd.DataFrame({'A': 'fruit drink cookie fruit'.split(),
                               'B': 'orange soda pie mango'.split(),
                               'C': np.arange(4)})

    # 메모리에 pandas 객체를 이용해 엑셀을 만들고 저장한다.
    output = io.BytesIO()
    writer = pd.ExcelWriter(output)
    data_frame.to_excel(writer, 'food')
    writer.save()

    # 엑셀 형태로 HTTP 응답을 주어 브라우저가 파일로 저장하게 유도한다.
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=download.xlsx'
    response.headers["Content-type"] = "text/csv"
    return response


# 이 웹서버는 127.0.0.1 주소를 가지면 포트 5000번에 동작하며, 에러를 자세히 표시한다.
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
