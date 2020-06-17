FROM python:3.6-slim

RUN pip3 install \
    PyGithub \
    pylint \
    coverage

WORKDIR /app
ADD ["*.sh", "/app/"]
ADD ["books.json", "/app/"]
RUN chmod +x /app/*.sh

# Add Python files last since they're most likely to change
ADD ["*.pylintrc", "/app/"]
ADD ["*.py", "/app/"]
RUN chmod +x /app/*.py

ENTRYPOINT ["/app/main.py"]
