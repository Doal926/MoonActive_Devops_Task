# MoonActive DevSecOps Home Exercise

## Table of Contents
- [Description](#description)
  - [Assignment A](#assingment-a)
  - [Assignment B](#assignment-b)
- [Getting Started](#getting-started)
  - [Assignment A](#assignment-a)
  - [Assignment B](#assignment-b-1)

## Description
Dor Alon's DevSecOps Home Exercise.

### Assingment A:
The code will scan an AWS account for externally exposed SQS queues and will alter their IAM policy to internal.
This assignment includes two workflows:
- A workflow that builds the code into a container and pushes it to DockerHub
- A workflow that scans the account once a day. This workflow can be triggered manually
  
Assignment A files:
- [sqs_policy_handler.py](./sqs_policy_handler.py)
- [Dockerfile](./Dockerfile)
- [.github/workflows/build_and_push.yaml](./.github/workflows/build_and_push.yaml)
- [.github/workflows/daily_sqs_external_policy_check.yaml](./.github/workflows/daily_sqs_external_policy_check.yaml)

### Assignment B:
The code will run on your AWS instance. This app will receive a GET request and return your instance metadata.
[Assignment B files.](Assignment_B/)

## Getting Started
### Assignment A:
#### Setup:
- Clone this repo.
- Configure the following repository secrets:
  - DOCKERHUB_USERNAME - your docker hub username
  - DOCKERHUB_TOKEN - your docker hub token
  - AWS_ACCESS_KEY_ID - your AWS account access key id
  - AWS_SECRET_ACCESS_KEY -  your AWS account secret access key
  - BUCKET_NAME - your s3 bucket name

#### Testing
There are two ways to run the code and check for external policy in all SQS queues in your account:
- Daily scan: This scan will trigger every day at 10 am UTC. This workflow will scan and upload the externally exposed SQS queue names to a S3 bucket and also alter the IAM policies of those queues
- Manual scan: For this scan to work, you need to go to your GitHub Actions -> Daily SQS External Policy Check -> Run Workflow
  ![image](https://github.com/Doal926/MoonActive_Devops_Task/assets/134269134/eb7ed7fd-4177-4c60-ae66-ac0d1f6f9651)
  When you trigger the manual scan, you can put a different bucket than the one you put in the secret, and you can specify to run in Log Mode(will not change the IAM policies) with one of these flags: `-l` or `--log`


### Assignment B:
#### Setup
```bash
cd 'Assignment_B/'
pip install -r requirements.txt
python3 instance_metadata.py
```

#### Testing
For this code to work, you need to send a GET request with the VM's IP and the correct Port with the suffix - `/metadata`. For example:
```bash
curl -X GET http://[vm-ip]:5000/metadata
```

