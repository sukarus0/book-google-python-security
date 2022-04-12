from flask import Flask, render_template, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

key = RSA.generate(2048)
cipher_rsa_public = PKCS1_OAEP.new(key.publickey())
cipher_rsa_private = PKCS1_OAEP.new(key)

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
            convert_result = cipher_rsa_public.encrypt\
                (convert_text.encode('utf-8'))
            convert_result = base64.b64encode(convert_result).decode('utf-8')
        elif method_type == "decode":
            encypted_data = base64.b64decode(convert_text)
            convert_result = cipher_rsa_private.decrypt\
                (encypted_data).decode('utf-8')
    
    return render_template("encoding.html", 
        convert_text = convert_text, method_type = method_type,
                           convert_result = convert_result)


# 이 웹서버는 0.0.0.0 주소, 포트 5000번에서 동작하며, 에러를 자세히 표시한다 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)