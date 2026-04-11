from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "admin": "123456",
    "testuser": "password123",
    "test01":"test01",
    "test02":"test01",
    "test03":"test01"
}

# Thêm một biến để lưu danh sách các tài khoản đang online và mã máy của họ
# Cấu trúc: {"tài_khoản": "mã_máy_tính"}
ACTIVE_USERS = {}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Thiếu thông tin JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    device_id = data.get('device_id') # Lấy mã máy tính từ app gửi lên

    if username in USERS and USERS[username] == password:
        # Kiểm tra xem tài khoản có đang được dùng ở máy khác không
        if username in ACTIVE_USERS and ACTIVE_USERS[username] != device_id:
            return jsonify({"success": False, "message": "Tài khoản đang được sử dụng ở thiết bị khác!"}), 403

        # Nếu hợp lệ, lưu lại trạng thái đang online cho máy này
        ACTIVE_USERS[username] = device_id
        return jsonify({"success": True, "status": "ok", "message": "Đăng nhập thành công"}), 200
    else:
        return jsonify({"success": False, "message": "Sai tài khoản hoặc mật khẩu"}), 401

# Thêm API để đăng xuất (giải phóng tài khoản)
@app.route('/api/logout', methods=['POST'])
def logout():
    data = request.get_json()
    username = data.get('username')
    
    # Xóa tài khoản khỏi danh sách đang online
    if username in ACTIVE_USERS:
        del ACTIVE_USERS[username]
        
    return jsonify({"success": True, "message": "Đã đăng xuất"}), 200

@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
