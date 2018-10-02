FROM python:2.7

ADD ./requirements.txt /
RUN pip install -r /requirements.txt

ADD ./advisor_client/requirements.txt /
RUN pip install -r /requirements.txt

# Install server
ADD . /tmp/
RUN /tmp/advisor_server/manage.py migrate

# Install client
WORKDIR /tmp/advisor_client/
RUN python ./setup.py develop

EXPOSE 8000

CMD ["/tmp/advisor_server/manage.py", "runserver", "0.0.0.0:8000"]
