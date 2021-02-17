FROM python:3.8-slim

WORKDIR /app

# Install libraries
COPY ["requirements.txt", "/app/"]
RUN python -m pip install -r requirements.txt

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
