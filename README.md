# Ladrillo Gestión
PoC for construction management
![image](https://github.com/user-attachments/assets/81552324-8033-44fa-b890-490734398756)


Run locally (no Docker)
```sh
# uv sync  # to install packages
DATA_DIR=./ uv run streamlit run src/streamlit_main.py
```

Steps to complete the prototype:
- [x] Add table and visualization for building materials spending
- [x] Input data form
- [x] Input data with empty dates
- [x] Edit data
- [x] Show progress bar for project status
- [x] Add upload button
- [x] Add reset system button 
 
## Docker
Build
```sh
docker buildx build -f docker/Dockerfile -t ladrillo-gestion .
```

Run
```sh
docker run -v ./src:/app/src -v ./test_data:/tmp/test_data -p 8501:8501 ladrillo-gestion
```

https://docs.google.com/spreadsheets/d/1nRl7ScM3iabbjMBcDVaRo--JDzSjE3nwaFpYzTUgl80/edit?usp=sharing

