# fully automated script for setting up Minikube on WSL with error handling

Here's a fully automated Bash script to install and configure Minikube on WSL (Ubuntu/Debian) with all necessary dependencies, including kubectl, Docker, and Helm. This script handles errors and ensures you have a working Kubernetes cluster.

📌 Steps Covered by This Script:
✅ Installs kubectl (fixes 302 redirect issue)
✅ Installs Minikube
✅ Installs Docker (for Minikube driver)
✅ Adds user to the Docker group (avoids permission issues)
✅ Starts Minikube
✅ Verifies the installation with kubectl get nodes

---

📌 How to Use This Script
  - 1️⃣ Open WSL (Ubuntu/Debian)
  - 2️⃣ Copy and paste the script into a file:

bash:

      nano install_minikube.sh
      
  - 3️⃣ Save the file (CTRL+X, then Y, then ENTER)
  - 4️⃣ Make the script executable:

bash: 

    chmod +x install_minikube.sh
    
  - 5️⃣ Run the script:

bash:

    ./install_minikube.sh

    
## ✅ What Happens After Running This Script?

* Minikube and dependencies are installed.
* Minikube is started automatically using Docker.
* Kubernetes is ready to use.
* You can now deploy applications using kubectl.

## 💡 Next Steps

Run minikube dashboard to open the Kubernetes UI.
Deploy a test Nginx app:
bash:

    kubectl create deployment nginx --image=nginx
    kubectl expose deployment nginx --type=NodePort --port=80
    minikube service nginx --url

Install Helm for managing Kubernetes applications.

