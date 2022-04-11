from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
import pyodbc
from datetime import datetime, timedelta


def get_connection_and_cursor():
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
    return mssql_conn, cursor


mssql_conn, cursor = get_connection_and_cursor()

# flask 웹, API 서버를 실행함
app = Flask(__name__)
api = Api(app)


# 검증용 SMS 키 발급(원래는 데이터베이스 같은데서 가져올 것이다)
def get_sms_key():
    sms_key = "7777"
    return sms_key


# 토큰에서 ID 가져오기(원래는 암호화된 쿠키에서 가져와야 함)
def get_member_id_from_cookie():
    id = "tom"
    return id


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
            now_time = datetime.now()
            member_id = get_member_id_from_cookie()

            # SMS 인증이 성공하면 sms_cert 테이블에 인증 성공 결과를 넣는다.
            if sms_number == certify_number:
                cert_sql = "insert into sms_cert values (?,?,?)"
                cursor.execute(cert_sql, member_id, "Y", now_time)

                # auto increment 숫자 얻어오기
                cursor.execute("SELECT @@IDENTITY AS ID;")
                seqno = str(cursor.fetchone()[0])
                mssql_conn.commit()

                result = "Y"
            else:
                result = "N"
                seqno = "0"

            return {"certify_yn": result, "seqno": seqno}
        except Exception as e:
            return {"certify_yn": "N", "seqno": seqno}


class DoPayment(Resource):
    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("item_price", type=str, default="")
        parser.add_argument("seqno", type=str, default="")
        return parser

    def post(self):
        try:
            parser = DoPayment.get_parser()
            args = parser.parse_args()
            item_price = int(args["item_price"])
            seqno = int(args["seqno"])

            member_id = get_member_id_from_cookie()
            due_date = datetime.now() - timedelta(minutes=15)

            # 해당 seqno, member_id, 15분 이내의 인증 성공 건을 가져온다.
            check_sql = "select top 1 cert_yn from sms_cert(nolock) " \
                        "where seqno = ? and member_id = ? and cert_date >= ?"
            cursor.execute(check_sql, seqno, member_id, due_date)

            cert_yn = cursor.fetchone()

            # 인증된 건이 있다면, 결제를 진행 한다.
            if cert_yn:
                if cert_yn[0] == "Y":
                    payment_result = do_payment(item_price)
                else:
                    payment_result = "N"
            else:
                payment_result = "N"

            return {"payment_result":payment_result}
        except Exception as e:
            print(e)
            return {"payment_result": "N"}


# API 경로 등록
api.add_resource(CheckSMS, "/check_sms")
api.add_resource(DoPayment, "/do_payment")


# 최초 요청 웹 페이지
@app.route("/secure_design", methods=['GET'])
def design():
    return render_template('secure_design_patch.html')


# 웹서버는 호스트 127.0.0.1, 포트 5000번에 동작하며, 디버그 모드이다.
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)