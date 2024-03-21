# MoonActive DevSecOps Home Exercise

## Table of Contents
- [Description](#description)
- [Getting Started](#getting started)
- [Usage](#usage)

## Description
This is Dor Alon DevSecOps Home Exercise.
Assignment A files: 
> - sqs_policy_handler.py
> - Dockerfile
> - .github/workflows/build_and_push.yaml
> - .github/workflows/daily_sqs_external_policy_check.yaml
Assignment B file:
> - Assignment_B/instance_metadata.py

## Getting Started
# Assignment A
In order for this assignmet to work you need to configure the following repository secrets in your cloned repo:
> - DOCKERHUB_USERNAME - your docker hub username
> - DOCKERHUB_TOKEN - your docker hub token
> - AWS_ACCESS_KEY_ID - your AWS account access key id
> - AWS_SECRET_ACCESS_KEY -  your AWS account secret access key
> - BUCKET_NAME - your s3 bucket name

# Assignment B
In for this assignment to work you need to run the code on your VM and send a GET request with the VM's IP and the right Port with the suffix /metadata. For example: `curl -X GET http://127.0.0.0:5000/metadata`

## Usage
[Explain how to use your project and provide examples if applicable.]

## Contributing
[Specify how others can contribute to your project, including guidelines for pull requests and code reviews.]

## License
[Choose an appropriate license for your project and include it here.]
