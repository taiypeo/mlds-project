FROM python:3.12.2-slim-bookworm

WORKDIR /app
COPY clustered_orig.csv requirements.txt main.py ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
