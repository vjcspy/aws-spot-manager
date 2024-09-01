import boto3
import os

ec2 = boto3.client('ec2')

def check_spot_instance(event, context):
    spot_request_id = os.environ['SPOT_FLEET_REQUEST_ID']
    allocation_id = os.environ.get('ALLOCATION_ID', None)

    # Kiểm tra Spot Request
    spot_requests = ec2.describe_spot_instance_requests(SpotInstanceRequestIds=[spot_request_id])
    spot_instance_id = spot_requests['SpotInstanceRequests'][0].get('InstanceId', None)

    if spot_instance_id:
        # Kiểm tra xem Instance đã có Elastic IP chưa
        instance = ec2.describe_instances(InstanceIds=[spot_instance_id])
        network_interfaces = instance['Reservations'][0]['Instances'][0]['NetworkInterfaces']

        for ni in network_interfaces:
            if ni.get('Association', {}).get('PublicIp', None):
                print(f"Instance {spot_instance_id} đã có Elastic IP.")
                return

        # Gán Elastic IP nếu chưa có
        if not allocation_id:
            eip = ec2.allocate_address(Domain='vpc')
            allocation_id = eip['AllocationId']
            print(f"Allocated new Elastic IP {eip['PublicIp']} with Allocation ID {allocation_id}")

        ec2.associate_address(InstanceId=spot_instance_id, AllocationId=allocation_id)
        print(f"Elastic IP {allocation_id} đã được gán cho instance {spot_instance_id}.")
    else:
        print(f"Spot Request {spot_request_id} chưa có instance.")
