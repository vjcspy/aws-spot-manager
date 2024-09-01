import boto3
import os

ec2 = boto3.client('ec2')


def check_spot_instance(event, context):
    spot_fleet_request_id = os.environ['SPOT_FLEET_REQUEST_ID']
    allocation_id = os.environ.get('ALLOCATION_ID', None)

    try:
        # Kiểm tra Spot Fleet Request
        spot_fleet_requests = ec2.describe_spot_fleet_requests(SpotFleetRequestIds=[spot_fleet_request_id])

        # Lấy thông tin các Spot Instances liên kết với Spot Fleet Request
        spot_fleet_instances = ec2.describe_spot_fleet_instances(SpotFleetRequestId=spot_fleet_request_id)
        spot_instance_ids = [instance['InstanceId'] for instance in spot_fleet_instances['ActiveInstances']]

        if spot_instance_ids and len(spot_instance_ids) == 1:
            for spot_instance_id in spot_instance_ids:
                # Kiểm tra xem Instance đã có Elastic IP chưa
                instance = ec2.describe_instances(InstanceIds=[spot_instance_id])
                network_interfaces = instance['Reservations'][0]['Instances'][0]['NetworkInterfaces']

                for ni in network_interfaces:
                    if ni.get('Association', {}).get('PublicIp', None):
                        print(f"Instance {spot_instance_id} đã có Elastic IP.")
                        return

                # Gán Elastic IP nếu chưa có
                # if not allocation_id:
                #     eip = ec2.allocate_address(Domain='vpc')
                #     allocation_id = eip['AllocationId']
                #     print(f"Allocated new Elastic IP {eip['PublicIp']} with Allocation ID {allocation_id}")

                if allocation_id:
                    ec2.associate_address(InstanceId=spot_instance_id, AllocationId=allocation_id)
                    print(f"Elastic IP {allocation_id} đã được gán cho instance {spot_instance_id}.")
        else:
            print(f"Spot Fleet Request {spot_fleet_request_id} chưa có instance nào.")

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        # raise e
