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
