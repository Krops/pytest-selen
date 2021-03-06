FROM python:3.7

COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir -p /tests
WORKDIR /tests
COPY tests/test_one.py /tests/
COPY tests/resources /tests/
RUN mkdir -p /report
CMD ["pytest", "--alluredir=report", "test_one.py"]
