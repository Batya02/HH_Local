FROM python:3.8.3

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir bot 
COPY bot ./bot
WORKDIR /bot

CMD ["python", "main.py"]