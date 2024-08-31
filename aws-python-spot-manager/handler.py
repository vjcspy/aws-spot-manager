import os
import boto3
import logging

# Thiết lập logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    spot_fleet_request_id = os.getenv('SPOT_FLEET_REQUEST_ID')
    new_target_capacity = int(os.getenv('NEW_TARGET_CAPACITY'))

    try:
        response = ec2_client.modify_spot_fleet_request(
            SpotFleetRequestId=spot_fleet_request_id,
            TargetCapacity=new_target_capacity
        )
        
        logger.info(f"Response from modify_spot_fleet_request: {response}")
        
        return {
            'statusCode': 200,
            'body': f'Successfully modified target capacity to {new_target_capacity}.'
        }
    except Exception as e:
        # Log lỗi nếu có
        logger.error(f"Error modifying target capacity: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': f'Error modifying target capacity: {str(e)}'
        }
