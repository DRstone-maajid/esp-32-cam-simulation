# ESP32-CAM Simulator Web App

This repository contains a simple Flask-based backend and HTML/JS frontend that simulate an ESP32-CAM device streaming images to a server. The project is designed to be deployed on [Railway](https://railway.app) but can run anywhere with Python support.

## Features

- Front-end interface for webcam or manual image upload
- ``/upload`` endpoint that accepts image data and saves files
- Configurable secret key for authentication
- Compatible with Railway hosting

## Getting Started

### Prerequisites

- Python 3.10+ (3.11 recommended)
- ``pip`` for installing dependencies
- Git (optional but recommended)

### Local Development

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd "esp 32 cam simulation"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Copy ``.env`` and set a secret:
   ```bash
   cp .env .env.local
   # edit .env.local and change UPLOAD_SECRET
   ```

5. **Run the server**
   ```bash
   set FLASK_ENV=development
   set UPLOAD_SECRET=your_secret_here
   python app.py
   ```
   Open http://localhost:5000 in your browser.

6. **Simulate ESP32**
   Make sure you have OpenCV installed with access to a webcam. Then run:
   ```bash
   python esp32_simulator.py --server http://localhost:5000 --key your_secret_here
   ```

### Deploying to Railway

1. **Push your repository** (ensure it’s on GitHub or GitLab). Railway connects to your Git provider.
2. **Create a new Railway project** and link the repo; it will automatically read `runtime.txt`,
   `requirements.txt`, and the `Procfile` to build your Python service.
3. **Set environment variables** under the project’s Variables tab:
   - `UPLOAD_SECRET` – a strong key used to authenticate uploads.
   - (optional) `FLASK_ENV` – `production` by default; use `development` for local debugging.

4. **Deploy and watch the logs**. Railway provides a dynamic port in the `PORT` variable,
   which the app already respects.

5. **Access the service** via the provided URL (e.g. `https://thieft-detection.up.railway.app`):
   - Front‑end UI at `/`
   - Upload endpoint at `/upload` (accepts JPEGs with the secret header)
   - Health check at `/health` (returns `{"status":"ok"}`)

6. **Public hosting considerations:**
   - CORS is enabled so clients on other origins can POST to `/upload`.
   - Responses are gzip‑compressed to save bandwidth.
   - Uploaded files live in an ephemeral `uploads/` folder; they vanish when the
     container restarts. For persistence, plug in external storage (S3, etc.).
   - The front-end defaults to the same-origin server URL; you rarely need to
     update it in production.

### Using the Simulator Script

```bash
python esp32_simulator.py --server https://<your-service>.railway.app --key <UPLOAD_SECRET>
```

### Notes

- Uploaded images are stored locally in the ``uploads/`` directory. Railway's ephemeral filesystem means files will disappear on restart. For persistence, integrate with external storage (S3, etc.).
- Adjust ``camera index`` in ``esp32_simulator.py`` if you have multiple webcams.
- UI defaults to the current origin so you don't need to set the server URL when using the same host.

## License

MIT
