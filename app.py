from flask import Flask, request, render_template, jsonify
import subprocess
import os
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"message": "아이디와 비밀번호를 입력하세요."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # painter.py 실행
            painter_path = os.path.join(os.getcwd(), "painter.py")
            if not os.path.exists(painter_path):
                return jsonify({"message": f"painter.py 파일이 존재하지 않습니다: {painter_path}"}), 500

            try:
                subprocess.Popen([r"C:\Users\Gram13\AppData\Local\Programs\Python\Python312\python.exe", painter_path])
                return jsonify({"message": "로그인 성공! Tkinter 창이 열립니다."}), 200
            except Exception as e:
                return jsonify({"message": f"Tkinter 실행 오류: {str(e)}"}), 500
        else:
            return jsonify({"message": "아이디 또는 비밀번호가 잘못되었습니다."}), 401

    except Exception as e:
        return jsonify({"message": f"요청 처리 중 오류가 발생했습니다: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
