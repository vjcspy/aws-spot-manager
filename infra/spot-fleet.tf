resource "aws_spot_fleet_request" "example" {
  iam_fleet_role  = "aws-ec2-spot-fleet-tagging-role"
  target_capacity = 1
}