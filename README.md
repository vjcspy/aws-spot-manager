# Auto Schedule AWS Spot request

## Infra

Sử dụng Terraform để tạo IAM Role cho lambda sử dụng

## AWS Python serverless

Sửa `serverless.yaml` để config cho đúng:
- SPOT_FLEET_REQUEST_ID
- NEW_TARGET_CAPACITY

### Deploy
```shell
serverless deploy
```
