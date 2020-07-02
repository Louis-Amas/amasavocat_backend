FROM python


RUN mkdir /code

COPY requirements.txt /code/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/

RUN python /code/manage.py collectstatic
RUN python /code/manage.py makemigrations
RUN python /code/manage.py migrate

CMD ["python", "code/manage.py", "runserver", "0.0.0.0:8000"]
