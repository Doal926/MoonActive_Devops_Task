import argparse
import json
import os
from typing import Any

import boto3


# function that uploads log.txt to s3 bucket
def upload_to_s3(bucket_name: str):
    s3 = boto3.client("s3")
    s3.upload_file("log.txt", bucket_name, "log.txt")


# function that runs through all sqs queues in all regions and get their resource policy
def get_sqs_policy(region: str) -> dict[str, dict[str, Any]]:
    client = boto3.client("sqs", region_name=region)
    sqs_policies = {}

    # if we have more than 1000 queues we need to use paginator
    for page in client.get_paginator("list_queues").paginate():
        for queue in page["QueueUrls"]:
            client = boto3.client("sqs", region_name=region)
            response = client.get_queue_attributes(
                QueueUrl=queue, AttributeNames=["QueueArn", "Policy"]
            )

            queue_policy = response["Attributes"]["Policy"]
            sqs_policies[queue] = json.loads(queue_policy)

    return sqs_policies


def fix_sqs_policy(aws_account_id: str, queue_policy: dict[str, Any]):
    for statement in queue_policy.get("Statement", []):
        if is_principal_external(aws_account_id, statement["Principal"]):
            statement["Principal"]["AWS"] = f"arn:aws:iam::{aws_account_id}:root"


# Function that changes the policy of a queue from external to internal
def change_sqs_policy(region, queue, queue_policy):
    queue_url = queue
    client = boto3.client("sqs", region_name=region)

    fix_sqs_policy(get_current_aws_account_id(), queue_policy)

    queue_policy = json.dumps(queue_policy)
    response = client.set_queue_attributes(
        QueueUrl=queue_url, Attributes={"Policy": queue_policy}
    )
    print(response)
    # return response


def get_current_aws_account_id():
    client = boto3.client("sts")
    response = client.get_caller_identity()
    return response["Account"]


def parse_arn(arn: str) -> dict[str, str]:
    arn = arn.split(":")
    return {
        "partition": arn[1],
        "service": arn[2],
        "region": arn[3],
        "account_id": arn[4],
        "resource": arn[5],
    }


def is_principal_external(current_account_id: str, principal: dict[str, Any] | str) -> bool:
    # check if the principal is an external account
    # according to: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html
    # according to the documentation above principal can be written as follows: "Principal": { "AWS": "123456789012" }
    # when it is done aws changes it to "Principal": { "AWS": "arn:aws:iam::123456789012:root" }
    if isinstance(principal, str):
        if principal == "*" or parse_arn(principal)["account_id"] != current_account_id:
            return True

    if isinstance(principal, dict):
        if "AWS" in principal:
            aws_principal = principal["AWS"]
            if isinstance(aws_principal, str):
                if aws_principal == "*" or parse_arn(aws_principal)["account_id"] != current_account_id:
                    return True
            elif isinstance(aws_principal, list):
                for p in aws_principal:
                    if p == "*" or parse_arn(p)["account_id"] != current_account_id:
                        return True
    return False


def is_policy_allow_external(
    current_aws_account_id: str, queue_policy: dict[str, Any]
) -> bool:
    # for each statement in the policy
    # check if the principal is an external account
    for statement in queue_policy.get("Statement", []):
        if is_principal_external(current_aws_account_id, statement["Principal"]):
            return True

    return False


def sqs_handler():
    args = parse_args()
    current_aws_account_id = get_current_aws_account_id()

    # get all regions
    client = boto3.client("ec2")
    regions = [region["RegionName"] for region in client.describe_regions()["Regions"]]

    # get all sqs queues in all regions
    for region in regions:
        if region != "eu-central-1":
            continue
        sqs_policies = get_sqs_policy(region)
        for queue, sqs_policy in sqs_policies.items():
            is_external_accessible_queue = is_policy_allow_external(
                current_aws_account_id, sqs_policy
            )
            if is_external_accessible_queue:
                with open("log.txt", "a") as f:
                    f.write(f"{queue.split('/')[-1]}\n")

                if args.change_policy:
                    change_sqs_policy(region, queue, sqs_policy)
    upload_to_s3(args.bucket)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", help="Bucket Name", required=True)
    parser.add_argument(
        "-cp", "--change-policy", action="store_true", help="Change Policy"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sqs_handler()
    # print log.txt
    if os.path.exists("log.txt"):
        with open("log.txt", "r") as f:
            print(f.read())
    # delete log.txt
    if os.path.exists("log.txt"):
        os.remove("log.txt")
