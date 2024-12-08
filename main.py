"""""<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <style>
        body {
            background-color: #90ee90; /* 연두색 배경 */
            display: flex;
            justify-content: center;
            align-items: flex-end; /* 화면 아래쪽으로 정렬 */
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .logo {
            position: absolute; /* 로고를 독립적으로 배치 */
            top: 20px; /* 화면 상단에서 여백 */
            text-align: center;
            width: 100%;
        }
        .logo img {
            max-width: 300px; /* 로고 크기를 3배 확대 */
            max-height: 300px;
            width: auto;
            height: auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 20px;
        }
        .container {
            text-align: center;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 500px; /* 가로로 길게 조정 */
            margin-bottom: 50px; /* 아래로 내려오도록 간격 조정 */
            margin-top: 100px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        input, button {
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #message {
            color: red;
            margin-bottom: 10px;
            font-size: 16px;
        }
    </style>
    <script>
        async function handleLogin(event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const message = document.getElementById("message");

            // 서버에 POST 요청 보내기
            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                const result = await response.text();

                // 메시지 업데이트
                if (response.ok) {
                    message.style.color = "green";
                    message.textContent = result;
                } else {
                    message.style.color = "red";
                    message.textContent = result;
                }
            } catch (error) {
                message.style.color = "red";
                message.textContent = "서버 오류가 발생했습니다.";
            }
        }
    </script>
</head>
<body>
    <div class="logo">
    <img src="/static/images/main_frog.png" alt="Logo">
    </div>
    <div class="container">
        <form onsubmit="handleLogin(event)">
            <!-- 메시지가 표시될 영역 -->
            <div id="message"></div>
            <label for="username">아이디:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">비밀번호:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">로그인</button>
        </form>
    </div>
</body>
</html>
"""