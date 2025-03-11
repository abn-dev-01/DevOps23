# fully automated script for setting up Minikube on WSL with error handling

Here's a fully automated Bash script to install and configure Minikube on WSL (Ubuntu/Debian) with all necessary dependencies, including kubectl, Docker, and Helm. This script handles errors and ensures you have a working Kubernetes cluster.

📌 Steps Covered by This Script:
✅ Installs kubectl (fixes 302 redirect issue)
✅ Installs Minikube
✅ Installs Docker (for Minikube driver)
✅ Adds user to the Docker group (avoids permission issues)
✅ Starts Minikube
✅ Verifies the installation with kubectl get nodes
