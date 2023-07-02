# syntax=docker/dockerfile:1

FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/
CMD ["uvicorn","app","--host","0.0.0.0", "--port","15400"]


