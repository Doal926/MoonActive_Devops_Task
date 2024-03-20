import boto3


# function that runs through all sqs queues in all regions and get thier rescource policy
def get_sqs_policy():
    # get all regions
    client = boto3.client("ec2")
    regions = [region["RegionName"] for region in client.describe_regions()["Regions"]]
    # get all sqs queues in all regions
    for region in regions:
        client = boto3.client("sqs", region_name=region)
        response = client.list_queues()
        for queue in response["QueueUrls"]:
            client = boto3.client("sqs", region_name=region)
            response = client.get_queue_attributes(
                QueueUrl=queue, AttributeNames=["QueueArn", "Policy"]
            )
            print(response["Attributes"]["QueueArn"], response["Attributes"]["Policy"])
