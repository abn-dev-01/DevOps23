# AWS DevOps

This script converts attached to EC2 instances `EBS not-encrypted` to `EBS-encrypted`: 
- Stop the EC2 instance.
- Find EC2 instance given in arguments of the script. 
- Load all EBS in this instance.
- Find snapshots for given EC2 instance with a creation time leass 30minutes and use it OR
    - Make a snapshot of EBS, then detach it from EC2-instance. 
- Create a new Encrypted EBS with the same options (return drive back at the instance)
- Start EC2 instance.

## Check out before starting

1. A path to the python - in the beging of the script.
2. `aws configure` your credentials - make sure you have enougth access to perform each command (EC2, EBS, etc)

This can help you: 

if you use MFA 

```
aws sts get-session-token \
  --profile permanent-profile \
  --serial-number arn:aws:iam::<aws-id-account>:mfa/<your-device> \
  --token-code 123456
```
and 
```
aws configure set aws_access_key_id YOUR_ACCESS_KEY
aws configure set aws_secret_access_key YOUR_SECRET_KEY
aws configure set aws_session_token YOUR_SESSION_TOKEN

aws configure set region us-west-2
aws configure set output json
```
  
