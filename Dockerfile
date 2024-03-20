FROM python:3.11.7

WORKDIR /usr/app

RUN pip install boto3

COPY sqs_policy_handler.py /usr/app/

CMD python sqs_policy_handler.py