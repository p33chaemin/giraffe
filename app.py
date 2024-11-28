from flask import Flask, render_template, request, redirect, url_for
import subprocess  # Tkinter 실행에 사용

app = Flask(__name__)

# 로그인 페이지
@app.route('/')
def home():
    return render_template('login.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # 간단한 로그인 검증 예제 (실제에서는 데이터베이스 사용)
    if username == "admin" and password == "1234":
        # 로그인 성공 시 Tkinter 실행
        subprocess.Popen(["python", "painter.py"])
        return "로그인 성공! Tkinter 창이 열립니다."
    else:
        return "로그인 실패. 다시 시도하세요."

if __name__ == '__main__':
    app.run(debug=True)
