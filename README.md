
# Color Recognition API

A FastAPI-based service that analyzes uploaded images and returns the **dominant colors** in RGB, HEX, and human-readable names (e.g., "Crimson", "SkyBlue").

Perfect for design tools, accessibility apps, fashion tech, or image analysis pipelines.

![FastAPI](https://img.shields.io/badge/FastAPI-109988?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue)


---

## 🚀 Features

- 🔍 Extract dominant colors using **K-Means clustering**
- 🖌️ Get colors in **RGB**, **HEX**, and **CSS3 human-readable names**
- 📤 Accepts image uploads (JPEG, PNG, etc.)
- 📊 Adjustable number of colors (1–10)
- 📄 Auto-generated API docs with **Swagger UI**
- 🐍 Built with modern Python & [`uv`](https://docs.astral.sh/uv/) for fast dependency management

---

## 📦 Prerequisites

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

---

## 🛠️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/color-detection.git
cd color-detection
```

### 2. Install dependencies using `uv` (recommended)

```bash
uv venv  # Create a virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

> 💡 `uv` is faster than `pip` and fully compatible with `pyproject.toml`.

---

## ▶️ Run the API

```bash
uv run fastapi dev
```

The server will start at:

- **API**: `http://127.0.0.1:8000`
- **Interactive Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`

---

## 🧪 Usage Example

### Upload an image via `curl`

```bash
curl -X POST "http://127.0.0.1:8000/api/color-recognition" \
  -F "image=@sample.jpg" \
  -F "num_colors=5" | python -m json.tool
```

### Example Response

```json
{
  "success": true,
  "filename": "sunset.jpg",
  "num_colors": 5,
  "colors": [
    {
      "rgb": [255, 69, 0],
      "hex": "#ff4500",
      "name": "Orange Red"
    },
    {
      "rgb": [255, 165, 0],
      "hex": "#ffa500",
      "name": "Orange"
    },
    ...
  ]
}
```

---

## 🌐 API Endpoints

| Method | Path | Description |
|-------|------|-------------|
| POST | `/api/color-recognition` | Upload an image and get dominant colors |
| GET  | `/health` | Health check — returns status |

> Supports `num_colors` (1–10) via form data.

---

## 🧩 How It Works

1. Image is uploaded and converted to RGB.
2. Pixels are flattened and clustered using **K-Means**.
3. Dominant colors are extracted and sorted by frequency.
4. Each color is matched to the closest **CSS3 named color** (e.g., "SteelBlue").
5. Results returned as JSON with RGB, HEX, and name.

Uses:
- `FastAPI` – for the REST API
- `scikit-learn` – K-Means clustering
- `Pillow` & `numpy` – image processing
- `webcolors` – color naming (v24.8.0+ compatible)

---

## 🧹 Development Tips

- Auto-reload enabled via `fastapi dev`
- Logs are visible in the terminal
- Test directly in Swagger UI

---

## 📦 Deployment (Optional)

Deploy using:

- Docker (see below)

### Dockerfile (optional)

```Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install -e .

COPY . .

CMD ["uv", "run", "fastapi", "run", "main.py"]
```

Then:
```bash
docker build -t color-api .
docker run -p 8000:8000 color-api
```






