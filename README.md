# Ladrillo Gestión
PoC for construction management


Run locally (no Docker)
```sh
uv venv
DATA_DIR=./ uv run streamlit run src/streamlit_main.py
```

To do:
* add plot to show workers salary
* show progress bar for project status
* Input data form
 
## Docker
Build
```sh
docker buildx build -f docker/Dockerfile -t ladrillo-gestion .
```

Run
```sh
docker run -v ./src:/app/src -v ./test_data.csv:/tmp/test_data.csv -p 8501:8501 ladrillo-gestion
```

https://docs.google.com/spreadsheets/d/1nRl7ScM3iabbjMBcDVaRo--JDzSjE3nwaFpYzTUgl80/edit?usp=sharing

