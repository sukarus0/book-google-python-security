from flask import Flask, render_template, request

# flask 웹서버를 실행함
app = Flask(__name__)


@app.route("/xss_ajax", methods=["GET", "POST"])
def xss():
    reflected_xss_string = ""
    
    if request.method == "GET":
        if "inputText" in request.args:
            reflected_xss_string = request.args.get("inputText",
                                                    default="", type=str)
    
    return render_template("xss_ajax.html",
                           reflected_xss_string = reflected_xss_string)


@app.route("/get_data", methods=['GET'])
def get_data():
    your_id = request.args.get('id')
    return "hello, " + str(your_id)


# 이 웹서버는 127.0.0.1 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)