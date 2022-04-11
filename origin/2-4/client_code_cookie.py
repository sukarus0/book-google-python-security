from flask import Flask, render_template, request, make_response

# flask 웹서버를 실행함
app = Flask(__name__)


@app.route("/set_cookie", methods=["GET", "POST"])
def set_cookie():
    cookie_text = ""
    get_cookie = ""
    
    if request.method == "POST":
        cookie_text = request.form["inputText"]
        get_cookie = request.cookies.get('your_id')

        if not get_cookie:
            get_cookie = "서버로 전송된 쿠키 없음"

    response = make_response(render_template(
        'client_code_cookie.html', cookie_text=cookie_text,
        get_cookie=get_cookie))

    if cookie_text:
        response.set_cookie("your_id", cookie_text)

    return response


# 이 웹서버는 127.0.0.1 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)