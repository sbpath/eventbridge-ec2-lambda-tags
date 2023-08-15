import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    sns = boto3.client("sns")
    sns_topic_arn = "arn:aws:sns:us-east-1:692050956348:Default_CloudWatch_Alarms_Topic"  # Replace with your SNS topic ARN

    event_detail = event["detail"]
    instance_id = event_detail["instance-id"]
    state = event_detail["state"]

    # Retrieve instance tags
    response = ec2.describe_instances(InstanceIds=[instance_id])
    tags = response["Reservations"][0]["Instances"][0].get("Tags", [])

    # Define the desired tag key and value
    desired_tag_key = "ENV"
    desired_tag_value = "PROD"

    # Check if the instance has the desired tag
    has_desired_tag = any(tag["Key"] == desired_tag_key and tag["Value"] == desired_tag_value for tag in tags)

    if has_desired_tag and state in ["stopped", "terminated"]:
        # Send notification to SNS topic
        message = f"Instance {instance_id} has the desired tag and is in state: {state}"
        sns.publish(TopicArn=sns_topic_arn, Message=message)
    else:
        print(f"Instance {instance_id} does not match the filtering criteria")

