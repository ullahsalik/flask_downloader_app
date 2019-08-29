FROM python:3.6.9-alpine3.10
ADD . /app
WORKDIR /app
RUN pip install gunicorn
EXPOSE 8000
RUN pip install -r /app/requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]
