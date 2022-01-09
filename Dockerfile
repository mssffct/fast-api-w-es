FROM python:3.9

WORKDIR .

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app ./app

RUN isort

RUN flake8

RUN pytest

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]