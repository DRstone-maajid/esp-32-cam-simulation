import os
from flask import Flask, request, send_from_directory, jsonify, abort
from flask_cors import CORS
from flask_compress import Compress
from datetime import datetime

# create app; static files served from project root
app = Flask(__name__, static_folder='.', static_url_path='')

# enable CORS to allow the front‑end or external clients to hit the upload endpoint
CORS(app)
# compress responses to reduce bandwidth for public usage
Compress(app)

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

@app.route('/health')
def health():
    """Simple health check used by uptime monitors or railway.
    """
    return jsonify(status="ok")

if __name__ == '__main__':
    # use the port provided by Railway or default to 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    # disable debug mode in production
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
