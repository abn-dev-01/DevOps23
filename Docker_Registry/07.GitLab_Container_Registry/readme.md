## [7] Using GitLab Container Registry
If you are using GitLab, it provides a built-in container registry that can be used to store Docker images.

Steps:
1. Enable the Container Registry in your GitLab project settings.
2. Authenticate, tag, and push your image:
sh
```
docker login registry.gitlab.com
docker tag your-image registry.gitlab.com/your-group/your-project/your-image
docker push registry.gitlab.com/your-group/your-project/your-image
```
