FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

ENV dockerHOME = '/democratiCPV'

RUN mkdir -p ${dockerHOME}

WORKDIR ${dockerHOME}

COPY requirements.txt ${dockerHOME}

RUN python -m pip install --upgrade pip

COPY . ${dockerHOME}

RUN python -m pip install -r requirements.txt


EXPOSE 8000

CMD python manage.py runserver 