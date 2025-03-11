#!/bin/bash

set -e  # Exit immediately if a command fails

echo "📌 Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required dependencies
echo "📌 Step 2: Installing required dependencies..."
sudo apt install -y curl wget apt-transport-https ca-certificates conntrack

# Install kubectl manually (fix for 302 redirect issue)
echo "📌 Step 3: Installing kubectl..."
K8S_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt || echo "v1.29.0")
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client

# Install Docker (for Minikube driver)
echo "📌 Step 4: Installing Docker..."
if ! command -v docker &> /dev/null; then
    sudo apt install -y docker.io
    sudo usermod -aG docker $USER
    echo "🚀 Docker installed! Please restart your WSL session for group changes to apply."
else
    echo "✅ Docker is already installed!"
fi

# Install Minikube
echo "📌 Step 5: Installing Minikube..."
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version

# Start Minikube using Docker as the driver
echo "📌 Step 6: Starting Minikube..."
minikube start --driver=docker

# Verify the installation
echo "📌 Step 7: Checking Kubernetes Cluster..."
kubectl get nodes

echo "🎉 Minikube installation completed successfully!"
echo "👉 Run 'minikube dashboard' to open the Kubernetes dashboard."
