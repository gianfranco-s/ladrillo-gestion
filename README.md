# Ladrillo Gestión
PoC for construction management


Run locally (no Docker)
```sh
uv venv
DATA_DIR=./ uv run streamlit run src/streamlit_main.py
```

Steps to complete the prototype:
- [x] Add table and visualization for building materials spending
- [x] Input data form
- [x] Input data with empty dates
- [x] Edit data
- [ ] Show progress bar for project status
- [ ] Add table for materials description
- [ ] Add table and visualization for workers spending
- [ ] Add table and visualization for project info
 
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

