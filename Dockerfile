FROM python:3.6-slim
RUN pip3 install PyGithub

WORKDIR /app
ADD ["*.py", "/app/"]
ADD ["books.json", "/app/"]
RUN chmod +x /app/*.py

ENTRYPOINT ["/app/main.py"]
