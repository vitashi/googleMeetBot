FROM python:3.9.15-alpine

WORKDIR /usr/src/automator

COPY . /usr/src/automator

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
