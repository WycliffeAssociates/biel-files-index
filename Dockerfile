FROM python:3
ADD main.py /
RUN pip3 install PyGithub
CMD [ "python3", "./main.py" ]
