from flask import Flask, render_template, request
from urllib import parse

# flask 웹서버를 실행함
app = Flask(__name__)


@app.route("/encoding", methods=["GET", "POST"])
def encoding():
    convert_text = ""
    convert_result = ""
    method_type = "encode"
    
    if request.method == "POST":
        convert_text = request.form["inputText"]
        method_type = request.form["convert_select"]

    if convert_text:
        if method_type == "encode":
            convert_result = parse.quote(convert_text)
        elif method_type == "decode":
            convert_result = parse.unquote(convert_text)
    
    return render_template("encoding.html", convert_text=convert_text,
                           method_type=method_type, convert_result=convert_result)


# 이 웹서버는 127.0.0.1 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)