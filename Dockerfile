FROM python:3
RUN pip3 install PyGithub
ADD ["*.py", "/"]
RUN chmod +x /main.py
ENTRYPOINT ["/main.py"]
