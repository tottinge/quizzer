FROM python:3.9-alpine
ENV QUIZ_HOST=0.0.0.0
ENV QUIZ_PORT=80
ADD . /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 4000
CMD ["python", "main.py"]