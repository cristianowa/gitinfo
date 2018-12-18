 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
 RUN python manage.py migrate
 RUN ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""