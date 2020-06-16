FROM python:3.6-slim

RUN pip3 install \
    PyGithub \
    pylint \
    coverage

WORKDIR /app
ADD ["*.sh", "/app/"]
ADD ["*.py", "/app/"]
ADD ["books.json", "/app/"]

RUN chmod +x /app/*.sh
RUN chmod +x /app/*.py

ENTRYPOINT ["/app/main.py"]
