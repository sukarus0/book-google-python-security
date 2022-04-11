from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse

# flask 웹, API 서버를 실행함
app = Flask(__name__)
api = Api(app)


class GetSecret(Resource):
    @staticmethod
    # 인자 파싱
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("my_name", type=str, default="")
        return parser

    # API 호출 처리
    def post(self):
        try:
            parser = GetSecret.get_parser()
            args = parser.parse_args()
            my_name = args["my_name"]

            secret = my_name + "' secret number is 123"

            return {"secret":secret}
        except Exception as e:
            return {"secret": str(e)}

# API 경로 등록
api.add_resource(GetSecret, "/get_secret")


# 최초 요청 웹 페이지
@app.route("/call_api", methods=['GET'])
def call_api():
    return render_template('api_default.html')


# 웹서버는 호스트 127.0.0.1, 포트 5000번에 동작하며, 디버그 모드이다.
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)