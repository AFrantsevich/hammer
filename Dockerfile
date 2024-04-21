FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY referal / /app
RUN chmod +x start.sh
CMD ["./start.sh"]