from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import jwt
from datetime import datetime, timedelta

# flask 웹, API 서버를 실행함
app = Flask(__name__)
api = Api(app)


# JWT 에 사용할 암호화 키 생성
def get_secret_key():
    secret_key = "secret"
    return secret_key


class MakeToken(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("my_name", type=str, default="")
        return parser


    def post(self):
        try:
            parser = MakeToken.get_parser()
            args = parser.parse_args()
            my_name = args["my_name"]

            secret_key = get_secret_key()

            # 기본 페이로드 생성(만료일, 생성일, 주제)
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=10),
                'iat': datetime.utcnow(),
                'sub': my_name
            }

            # 토큰 만들어 내기
            secret = jwt.encode(
                payload,
                secret_key,
                algorithm="HS256"
            )

            return {"token":secret}
        except Exception as e:
            return {"token": str(e)}


class SendToken(Resource):
    def post(self):
        try:
            secret_key = get_secret_key()

            # 요청된 Authorization 헤더로 부터 토큰 값 추출
            auth_header = request.headers.get('Authorization')
            if auth_header:
                my_token = auth_header.split(" ")[1]

            # 토큰 값 복호화
            payload = jwt.decode(my_token, secret_key, algorithms=["HS256"])
            user_name = payload["sub"]

            return {"my_name":user_name}
        except jwt.ExpiredSignatureError:
            return {"my_name":"토큰이 만료됨!"}
        except Exception as e:
            return {"my_name": str(e)}


# API 경로 등록
api.add_resource(MakeToken, "/make_token")
api.add_resource(SendToken, "/send_token")


# 최초 요청 웹 페이지
@app.route("/call_api", methods=['GET'])
def call_api():
    return render_template('api_with_token.html')


# 웹서버는 호스트 127.0.0.1, 포트 5000번에 동작하며, 디버그 모드이다.
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)