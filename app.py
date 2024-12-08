from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    """
    홈 페이지 라우트: templates/login.html을 렌더링합니다.
    """
    return render_template("login.html")  # templates/login.html 파일 렌더링

@app.route("/login", methods=["POST"])
def login():
    """
    로그인 처리 라우트: POST 요청으로 받은 JSON 데이터를 확인하여
    유효한 사용자(admin/1234)인지 검증하고, 성공 시 painter.py 실행.
    """
    try:
        # 요청 데이터 가져오기
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # 로그인 검증
        if username == "admin" and password == "1234":
            # painter.py 실행
            painter_path = os.path.join(os.getcwd(), "painter.py")
            if not os.path.exists(painter_path):
                return f"painter.py 파일이 존재하지 않습니다: {painter_path}", 500

            try:
                subprocess.Popen(["python", painter_path])
                return "로그인 성공! Tkinter 창이 열립니다.", 200
            except Exception as e:
                return f"Tkinter 실행 오류: {str(e)}", 500
        else:
            return "아이디 또는 비밀번호가 잘못되었습니다.", 401

    except Exception as e:
        return f"요청 처리 중 오류가 발생했습니다: {str(e)}", 500


if __name__ == "__main__":
    # Flask 애플리케이션 실행
    app.run(debug=True)
