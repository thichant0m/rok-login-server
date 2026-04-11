from flask import Flask, request, jsonify

app = Flask(__name__)

# Danh sách tài khoản mẫu (Trong thực tế bạn nên dùng Database như MySQL, MongoDB, SQLite...)
USERS = {
    "admin": "123456",
    "testuser": "password123"
}

@app.route('/api/login', methods=['POST'])
def login():
    # Lấy dữ liệu JSON từ request của app Tkinter
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Thiếu thông tin JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    # Kiểm tra tài khoản và mật khẩu
    if username in USERS and USERS[username] == password:
        # Trả về success = True đúng với yêu cầu của app Tkinter của bạn
        return jsonify({"success": True, "status": "ok", "message": "Đăng nhập thành công"}), 200
    else:
        return jsonify({"success": False, "message": "Sai tài khoản hoặc mật khẩu"}), 401

# Route mặc định để test xem server có chạy không
@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
