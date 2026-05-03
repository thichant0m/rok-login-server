from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "admin": "123456",
    "testuser": "password123",
    "user01": "thichfarmgem"
}

# Biến lưu danh sách tài khoản đang online và thông tin thiết bị đang chiếm quyền
# Cấu trúc: {"tài_khoản": "mã_máy_tính_đang_dùng"}
ACTIVE_USERS = {}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Thiếu thông tin JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    device_id = data.get('device_id')  # Lấy mã máy tính từ App gửi lên

    if username in USERS and USERS[username] == password:
        # Quan trọng: GHI ĐÈ device_id mới dể đăng nhập.
        # Lúc này, thông tin device_id của máy cũ trong ACTIVE_USERS sẽ bị xóa và thay bằng mã mạng của máy mới.
        ACTIVE_USERS[username] = device_id
        return jsonify({"success": True, "status": "ok", "message": "Đăng nhập thành công"}), 200
    else:
        return jsonify({"success": False, "message": "Sai tài khoản hoặc mật khẩu"}), 401

# API kiểm tra phiên làm việc liên tục (Heartbeat API cho Bot)
@app.route('/api/verify_session', methods=['POST'])
def verify_session():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "valid": False}), 400

    username = data.get('username')
    device_id = data.get('device_id')

    # Nếu máy cũ gửi lên để hỏi, mà server đang lưu device_id bị máy khác ghi đè lên rồi
    if username in ACTIVE_USERS and ACTIVE_USERS[username] == device_id:
        # Nếu khớp, cho phép Bot duy trì chạy
        return jsonify({"success": True, "valid": True}), 200
    else:
        # Nếu đã bị máy khác đăng nhập đè lên -> đá máy này ra!
        return jsonify({"success": False, "valid": False}), 200

# API để đăng xuất (giải phóng tài khoản nếu cần)
@app.route('/api/logout', methods=['POST'])
def logout():
    data = request.get_json()
    if not data:
        return jsonify({"success": False}), 400
        
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
