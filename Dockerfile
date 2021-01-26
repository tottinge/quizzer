FROM python:3.9-alpine
ADD . /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 4000
CMD ["python", "main.py"]