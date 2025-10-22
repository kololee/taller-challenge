FROM python:3.11-slim

WORKDIR /code

COPY ./src/app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]