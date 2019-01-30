FROM python:3
RUN pip3 install PyGithub
ADD ["*.py", "/"]
ENTRYPOINT ["/main.py"]
