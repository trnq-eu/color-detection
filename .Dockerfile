FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install -e .

COPY . .

CMD ["uv", "run", "fastapi", "run", "main.py"]