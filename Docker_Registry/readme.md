# Docker Registry

There are several ways to set up a Docker registry. Here are the most common methods:

### [1] `Docker Hub`.
Using a public DockerRegistry, like `Docker Hub`. It is a hosted registry service provided by Docker, and it's the easiest way to start using a Docker registry. You just need to create an account on Docker Hub and start pushing your images.

## [2] Running a Private Docker Registry
Docker provides an official image for setting up your own registry. You can run a private Docker registry on your own server or cloud provider.

Using Docker CLI

    docker run -d -p 5000:5000 --name registry registry:2

This command will pull the official registry image and run it as a container on port 5000.

Using Docker Compose
Create a `docker-compose.yml` file:

```version: '3'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - ./data:/var/lib/registry
```

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

## [4] Using Google Container Registry (GCR)
GCR is a fully managed Docker registry service by Google Cloud Platform.

Steps:
1. Authenticate Docker with GCR:
sh
```
gcloud auth configure-docker
```
2. Tag and push your image:
sh
```
docker tag your-image gcr.io/your-project-id/your-image
docker push gcr.io/your-project-id/your-image
```

## [5] Using Azure Container Registry (ACR)
ACR is a managed Docker registry service by Microsoft Azure.

Steps:
1. Create a registry in Azure.
2. Log in to the registry:
sh
```
az acr login --name yourRegistryName
```
3. Tag and push your image:
sh
```
docker tag your-image yourRegistryName.azurecr.io/your-image
docker push yourRegistryName.azurecr.io/your-image
```

## [6] Using Harbor
Harbor is an open-source container image registry that secures images with role-based access control, scans images for vulnerabilities, and signs images as trusted.

Using Docker Compose
Create a `harbor.yml` file with your configuration. 
[See at the 06.Harbor for details >>>](./06.Harbor/readme.md)

## [7] Using GitLab Container Registry
[See the details here >>>](./07.GitLab_Container_Registry/readme.md)

## [8] Using Self-Hosted Solutions
[See the details here >>>](./08.Self_hosting/readme.md)


