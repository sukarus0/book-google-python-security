from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# flask 웹서버를 실행 한다
app = Flask(__name__)


# 업로드 창을 보여준다
@app.route('/upload')
def upload():
    return render_template('updown_upload.html')


# 업로드 처리를 한다
@app.route('/upload_process', methods=['GET', 'POST'])
def upload_process():
    if request.method == 'POST':
        file_object = request.files['uploaded_file']
        file_object.save(secure_filename(file_object.filename))
        return '파일 업로드 완료'


# 이 웹서버는 127.0.0.1 주소를 가지면 포트 5000번에 동작하며, 에러를 자세히 표시한다
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
