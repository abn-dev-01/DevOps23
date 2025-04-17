#!/usr/bin/env bash
# Script to obtain temporary AWS credentials and configure profile
# Usage: ./aws-sts.sh <MFA_CODE>
#
# Add code below into ~/.bashrc
#
# # AWS Session Token
# if [ -f ~/.aws_temp_creds.sh ]; then
#    . ~/.aws_temp_creds.sh
# fi


set -euo pipefail

# Check that MFA token is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <MFA_CODE>"
  exit 1
fi

MFA_CODE="$1"
# Profile with permanent credentials
PERMANENT_PROFILE="permanent-profile"
# Profile for temporary credentials
TEMP_PROFILE="temp-profile"
# MFA device ARN
MFA_ARN="arn:aws:iam::<account-id>:mfa/<mfa-id>"
echo "!!! replace this in code $MFA_ARN "; exit 1;

# Temporary file to store JSON response
CREDS_FILE=$(mktemp)
trap 'rm -f "$CREDS_FILE"' EXIT

# Print STS command before execution
# Prepare STS command, echo and execute it
STS_CMD=(aws sts get-session-token --serial-number "$MFA_ARN" --token-code "$MFA_CODE" --profile "$PERMANENT_PROFILE")
echo "Executing STS command: ${STS_CMD[*]}"
"${STS_CMD[@]}" > "$CREDS_FILE"

# Parse credentials from JSON
ACCESS_KEY=$(jq -r .Credentials.AccessKeyId "$CREDS_FILE")
SECRET_KEY=$(jq -r .Credentials.SecretAccessKey "$CREDS_FILE")
SESSION_TOKEN=$(jq -r .Credentials.SessionToken "$CREDS_FILE")

# Update AWS CLI profile with temporary credentials
aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$TEMP_PROFILE"
aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$TEMP_PROFILE"
aws configure set aws_session_token "$SESSION_TOKEN" --profile "$TEMP_PROFILE"

# Update default AWS CLI profile with temporary credentials
aws configure set aws_access_key_id "$ACCESS_KEY"
aws configure set aws_secret_access_key "$SECRET_KEY"
aws configure set aws_session_token "$SESSION_TOKEN"

# Create a shell script with exports for temporary credentials
ENV_FILE="$HOME/.aws_temp_creds.sh"
touch $ENV_FILE
cat > "$ENV_FILE" <<EOF
export AWS_ACCESS_KEY_ID="$ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$SECRET_KEY"
export AWS_SESSION_TOKEN="$SESSION_TOKEN"
export AWS_SESSION_EXPIRE=$(jq -r .Credentials.Expiration "$CREDS_FILE")
EOF

chmod +x "$ENV_FILE"
echo "Temporary credentials exported to $ENV_FILE"

# Example usage of the temp profile
#echo "Listing S3 buckets with profile '$TEMP_PROFILE':"
#aws s3 ls --profile "$TEMP_PROFILE"
