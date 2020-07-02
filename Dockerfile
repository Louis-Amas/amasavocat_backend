FROM python:3.7.8-stretch


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "/usr/src/app/manage.py", "runserver"]
