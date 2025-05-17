FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install .

# Streamlit’s default port
EXPOSE 8501

# # tell Streamlit where to look for the app
# ENV STREAMLIT_SERVER_HEADLESS=true \
#     STREAMLIT_SERVER_ENABLECORS=false \
#     STREAMLIT_SERVER_PORT=8501


CMD ["streamlit", "run", "src/streamlit_main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]