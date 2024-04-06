FROM python:3.12.2-slim-bookworm

WORKDIR /app
COPY requirements.txt bot.py ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "bot.py"]
