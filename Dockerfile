FROM python:3.6.3
MAINTAINER Matthew Berryhill "matthewberryhill@gmail.com"
COPY ./api /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]