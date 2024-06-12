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
