FROM python:3.9-slim-bullseye
ENV QUIZ_HOST=0.0.0.0
ENV QUIZ_PORT=80
ADD . /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
CMD ["python", "main.py"]
#
# SOME HELPFUL DOCKER COMMANDS
# ============================
# docker build -t quizzology:latest .
# docker rmi quizzology
# docker system prune
# docker images
# docker run -p 4000:80 --name qz quizzology
# docker run -p 4000:80 -v $(pwd):/app --name qz quizzology
# docker ps
# docker rm qz
# docker stop qz
# docker restart qz
# docker inspect qz
