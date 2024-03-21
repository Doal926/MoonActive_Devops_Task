# MoonActive DevSecOps Home Exercise

## Table of Contents
- [Description](#description)
- [Getting Started](#getting-started)
- [Usage](#usage)

## Description
Dor Alon's DevSecOps Home Exercise

### Assingment A:
In this assignment, the code will scan your AWS account for external SQS policies and change them to internal policies instead. This assignment also includes two workflows: one that builds the code into a container and pushes this container to a DockerHub repository and the other workflow that scans the account once every day and also can be triggered manually
Assignment A files:
- sqs_policy_handler.py
- Dockerfile
- .github/workflows/build_and_push.yaml
- .github/workflows/daily_sqs_external_policy_check.yaml

### Assignment B:
In this assignment, the code will run on your AWS instance. This app will receive a GET request and return your instance metadata
Assignment B file:
- Assignment_B/instance_metadata.py

## Getting Started
### Assignment A:
For this assignment to work, you need to configure the following repository secrets in your cloned repo:
- DOCKERHUB_USERNAME - your docker hub username
- DOCKERHUB_TOKEN - your docker hub token
- AWS_ACCESS_KEY_ID - your AWS account access key id
- AWS_SECRET_ACCESS_KEY -  your AWS account secret access key
- BUCKET_NAME - your s3 bucket name

### Assignment B:
For this assignment to work, you need to run the code on your VM

## Usage
# Assignment A:
There are two ways to run the code and check for external policy in all SQS queues in your account:
- Daily scan: This scan will trigger every day at 10 am. This workflow will scan and upload but will not change the policy
- Manual scan: For this scan to work, you need to go to your GitHub Actions -> Daily SQS External Policy Check -> Run Workflow
  ![image](https://github.com/Doal926/MoonActive_Devops_Task/assets/134269134/eb7ed7fd-4177-4c60-ae66-ac0d1f6f9651)
  When you trigger the manual scan, you can put a different bucket than the one you put in the secret, and you can specify to change policy with one of these flags: `-cp` or `--change-    policy`

# Assignment B:
For this code to work, you need to send a GET request with the VM's IP and the correct Port with the suffix - `/metadata`. For example: `curl -X GET http://127.0.0.0:5000/metadata`

