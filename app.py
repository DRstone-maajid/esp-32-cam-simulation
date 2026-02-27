import os
from flask import Flask, request, send_from_directory, jsonify, abort
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# secret used to validate uploads from the simulator/ESP32
UPLOAD_SECRET = os.environ.get('UPLOAD_SECRET', '')

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    # serve the front-end file directly
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    key = request.headers.get('X-ESP32-KEY', '')
    if UPLOAD_SECRET and key != UPLOAD_SECRET:
        return abort(401, "Unauthorized")

    data = request.get_data()
    if not data:
        return abort(400, "No data received")

    filename = datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.jpg'
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as f:
        f.write(data)

    app.logger.info(f"received {len(data)} bytes -> {filename}")
    return jsonify(status="ok", filename=filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
