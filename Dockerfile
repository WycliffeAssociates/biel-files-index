FROM python:3.6-slim

RUN pip3 install \
    PyGithub \
    pylint \
    coverage

WORKDIR /app

# Add data files
COPY ["languages.json", "/app/"]

# Add scripts
COPY ["lint.sh", "/app/"]
COPY ["test.sh", "/app/"]
RUN chmod +x /app/*.sh

# Add Python files last since they're most likely to change
COPY ["*.pylintrc", "/app/"]
COPY ["*.py", "/app/"]
RUN chmod +x /app/*.py

ENTRYPOINT ["/app/main.py"]
