## [3] Using AWS ECR (Elastic Container Registry)
AWS ECR is a managed container image registry service. You can integrate it with your AWS account and use it to store your Docker images.

Steps:
1. Create a repository in AWS ECR.
2. Configure your Docker CLI to authenticate with ECR:
sh
```
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
```
3. Tag and push your image:
```
docker tag your-image:latest your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository:tag
docker push your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository:tag
```
