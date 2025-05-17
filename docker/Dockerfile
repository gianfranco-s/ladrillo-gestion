FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install .

# Streamlit’s default port
EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit_main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
