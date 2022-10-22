FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/lms_core
COPY requirements.txt /usr/src/lms_core/
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
#
#RUN python manage.py migrate

COPY . /usr/src/lms_core

CMD python manage.py runserver 0.0.0.0:8000