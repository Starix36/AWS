import boto3

# Initialize AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
s3_client = boto3.client('s3')
eks_client = boto3.client('eks')
sts_client = boto3.client('sts')

def get_account_id():
    try:
        account_id = sts_client.get_caller_identity()['Account']
        return account_id
    except Exception as e:
        print(f"Error fetching Account ID instances: {e}")
        return None


def get_ec2_instances():
    try:
        ec2_instances = ec2_client.describe_instances()
        return ec2_instances
    except Exception as e:
        print(f"Error fetching EC2 instances: {e}")
        return None

def get_rds_instances():
    try:
        rds_instances = rds_client.describe_db_instances()
        return rds_instances
    except Exception as e:
        print(f"Error fetching RDS instances: {e}")
        return None

def get_s3_buckets():
    try:
        s3_buckets = s3_client.list_buckets()
        return s3_buckets
    except Exception as e:
        print(f"Error fetching S3 buckets: {e}")
        return None

def get_eks_clusters():
    try:
        eks_clusters = eks_client.list_clusters()
        return eks_clusters
    except Exception as e:
        print(f"Error fetching EKS clusters: {e}")
        return None

# Get EC2 instances
ec2_info = get_ec2_instances()
if ec2_info:
    for reservation in ec2_info.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            print(f"EC2 Instance: {instance.get('InstanceId')}, Region: {instance.get('Placement', {}).get('AvailabilityZone')}, Type: {instance.get('InstanceType')}, State: {instance.get('State', {}).get('Name')}, Tags: {instance.get('Tags')}")

# Get RDS instances
rds_info = get_rds_instances()
if rds_info:
    for rds_instance in rds_info.get('DBInstances', []):
        print(f"RDS Instance: {rds_instance.get('DBInstanceIdentifier')}, Region: {rds_instance.get('AvailabilityZone')}, Type: {rds_instance.get('DBInstanceClass')}, State: {rds_instance.get('DBInstanceStatus')}, Tags: {rds_instance.get('TagList')}")

# Get S3 buckets
s3_info = get_s3_buckets()
if s3_info:
    for bucket in s3_info.get('Buckets', []):
        try:
            tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
            print(f"S3 Bucket: {bucket['Name']}, Region: {s3_client.meta.region_name}, Tags: {tags['TagSet']}")
        except Exception as e:
            print(f"Error fetching tags for bucket {bucket['Name']}: {e}")

# Get EKS clusters
account_id = get_account_id()
eks_info = get_eks_clusters()

if eks_info:
    for cluster in eks_info.get('clusters', []):
        try:
            tags = eks_client.list_tags_for_resource(resourceArn=f"arn:aws:eks:{eks_client.meta.region_name}:{account_id}:cluster/{cluster}")
            print(f"EKS Cluster: {cluster}, Region: {eks_client.meta.region_name}, Tags: {tags['tags']}")
        except Exception as e:
            print(f"Error fetching tags for cluster {cluster}: {e}")