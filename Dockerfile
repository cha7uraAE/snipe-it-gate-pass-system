FROM python:3.12-slim

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

EXPOSE 8501


CMD ["sh", "-c", "streamlit run --browser.serverAddress 0.0.0.0 --server.enableCORS False --server.port 8501 /usr/app/src/app.py" ]

