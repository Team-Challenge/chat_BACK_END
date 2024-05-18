FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

EXPOSE 8000

CMD [ "python", "main.py" , "--host", "0.0.0.0", "--port", "8000"]