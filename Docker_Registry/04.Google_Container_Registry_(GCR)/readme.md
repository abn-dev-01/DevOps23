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
