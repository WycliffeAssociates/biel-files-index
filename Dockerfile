FROM python:3
RUN pip3 install PyGithub
ADD ["main.py", "/"]
ADD ["books.json", "/"]
RUN chmod +x /main.py
ENTRYPOINT ["/main.py"]
