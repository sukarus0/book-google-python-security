from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse

# flask 웹, API 서버를 실행함
app = Flask(__name__)
api = Api(app)


# 검증용 SMS 키 발급(원래는 데이터베이스 같은데서 가져올 것이다)
def get_sms_key():
    sms_key = "7777"
    return sms_key


# 결제 진행(원래는 복잡한 체크 로직 후, 결제가 될 것이다)
def do_payment(item_price):
    if item_price > 0:
        payment_result = "Y"
    else:
        payment_result = "N"
    return payment_result


class CheckSMS(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("sms_number", type=str, default="")
        return parser

    def post(self):
        try:
            parser = CheckSMS.get_parser()
            args = parser.parse_args()
            sms_number = args["sms_number"]

            certify_number = get_sms_key()

            if sms_number == certify_number:
                result = "Y"
            else:
                result = "N"

            return {"certify_yn": result}
        except Exception as e:
            return {"certify_yn": "N"}


class DoPayment(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("item_price", type=str, default="")
        return parser

    def post(self):
        try:
            parser = DoPayment.get_parser()
            args = parser.parse_args()

            item_price = int(args["item_price"])
            payment_result = do_payment(item_price)

            return {"payment_result":payment_result}
        except Exception as e:
            return {"payment_result": "N"}


# API 경로 등록
api.add_resource(CheckSMS, "/check_sms")
api.add_resource(DoPayment, "/do_payment")


# 최초 요청 웹 페이지
@app.route("/secure_design", methods=['GET'])
def design():
    return render_template('secure_design_bad.html')


# 웹서버는 호스트 127.0.0.1, 포트 5000번에 동작하며, 디버그 모드이다.
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)