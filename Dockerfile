FROM python:2.7

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /tests
WORKDIR /tests
COPY tests/test_one.py /tests
CMD ["pytest", "test_one.py"]