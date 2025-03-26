FROM python:3.12.3-alpine3.19

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 5001
ENV DEBUG true



WORKDIR /usr/share/src 

COPY  /requirements.txt ./
#COPY /requirements.dev.txt ./  

RUN  pip install -r ./requirements.txt 
#     \ && pip install  -r ./requirements.dev.txt

COPY /src/  ./

COPY /dev_examples/exampleHTML1.html ../dev_examples/
COPY /dev_examples/exampleHTML2.html ../dev_examples/

EXPOSE 5001
RUN pip install uvicorn

# run the app server   with gunicorn
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5001", "--workers", "3", "app:app"]