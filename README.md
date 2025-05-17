# Ladrillo Gestión
PoC for construction management


Run locally (no Docker)
```sh
uv run streamlit run src/streamlit_main.py
```


## Docker
Build
```sh
docker buildx build -f docker/Dockerfile -t ladrillo-gestion .
```

Run
```sh
docker run -v ./src:/app/src -p 8501:8501 ladrillo-gestion
```
