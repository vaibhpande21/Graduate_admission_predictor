
FROM python:3.9.6-slim-bullseye
WORKDIR /docker

COPY requirements.txt ./

RUN  pip install --upgrade pip
RUN  pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "--app", "graduate", "run", "--host=0.0.0.0" ]