FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt
# --no-cache-dir reduces the image size

COPY . .

EXPOSE 8501
#By default Streamlit runs on port no. 8501

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0"]