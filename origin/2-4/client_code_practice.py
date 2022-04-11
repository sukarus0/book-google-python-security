from flask import Flask, render_template, request, make_response, jsonify

# flask 웹서버를 실행함
app = Flask(__name__)


def save_cookie(response, customer_id):
    if customer_id in ["tom", "jerry", "secret"]:
        response.set_cookie("your_id", customer_id)
    return response


def process_money(money):
    return money


@app.route("/get_money", methods=["GET", "POST"])
def get_money():
    customer_id = ""
    get_cookie = ""
    withdraw_money = ""
    request_money = ""
    
    if request.method == "POST":
        customer_id = request.form["myID"]
        request_money = request.form["requestMoney"]
        get_cookie = request.cookies.get("your_id")
        withdraw_money = process_money(request_money)

        if not get_cookie:
            get_cookie = "서버로 전송된 쿠키 없음"

    response = make_response(
        render_template("client_code_practice.html", customer_id=customer_id,
                        get_cookie=get_cookie, withdraw_money=withdraw_money))
    response = save_cookie(response, customer_id)
    
    return response


@app.route("/get_balance", methods=['POST'])
def get_balance():
    content = request.json
    customer_id = content["customer_id"]

    if customer_id == "tom":
        balance = "100000"
    elif customer_id == "jerry":
        balance = "200000"
    elif customer_id == "secret":
        balance = "infinite"
    else:
        balance = "blocked"

    return jsonify({"balance": balance})


# 이 웹서버는 127.0.0.1 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)