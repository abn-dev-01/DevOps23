# what I can use on windows instead of Docker Desktop app?

If you're looking for alternatives to Docker Desktop on Windows, there are several options you can consider depending on your specific needs, such as running containers directly, leveraging a lightweight VM setup, or using other Docker-compatible tools. Here are a few alternatives:

### 1. **Podman**
Podman is a daemonless container engine for developing, managing, and running OCI Containers on your system. Podman is a drop-in replacement for Docker but doesn't require a running daemon. It can be a good choice for those looking to use containers without Docker Desktop.

- **Installation:** Podman can be installed on Windows using the Windows Subsystem for Linux (WSL). After setting up WSL, you can install Podman in your Linux distribution using the package manager.

### 2. **Rancher Desktop**
Rancher Desktop is an application for Mac, Windows, and Linux that provides Kubernetes and container management at the desktop level. It uses containerd and k3s under the hood instead of Docker.

- **Features:** Rancher Desktop allows you to run Kubernetes using the same version that ships with Docker Desktop, and it uses a straightforward interface to manage Kubernetes contexts and container images.

### 3. **Multipass**
Multipass is a lightweight VM manager that allows you to quickly and easily launch and manage VMs. It provides a command-line interface to launch, manage, and generally interact with VM instances for Linux.

- **Usage:** While primarily used for launching Linux VMs, you can use it to run any containerized applications inside those VMs. This can be a simpler alternative for those who need a quick setup for development environments.

### 4. **Minikube**
Minikube is a tool that lets you run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.

- **Purpose:** You can use Minikube to run Docker containers within a Kubernetes environment. It's useful for learning and development purposes.

### 5. **CRI-O**
CRI-O is a lightweight container engine for running containers according to the Open Container Initiative (OCI) specification. It’s designed to provide an integration path between OCI conformant runtimes and the Kubelet. 

- **Details:** While not a direct replacement for Docker Desktop, it can be used in environments where Kubernetes is being used to manage containers.

### 6. **Mirantis Container Runtime (formerly Docker Enterprise)**
After acquiring Docker Enterprise, Mirantis continues to offer a robust container platform. This can be used as a more enterprise-focused alternative to Docker Desktop, especially in professional environments.

### 7. **Use Windows Subsystem for Linux (WSL) with Docker CLI**
With WSL 2, you can install Docker CLI on your Linux distribution running on WSL and use it to manage Docker containers. This setup uses the underlying Linux kernel, which can be a more integrated and native-like experience for those comfortable with Linux.

- **Setup:** Install WSL 2, select a Linux distribution via the Microsoft Store (such as Ubuntu), and then install Docker within that Linux environment.

### Conclusion
Each of these alternatives has its own set of features and limitations. Your choice will depend on whether you need a full Docker-compatible experience, something lighter, or if you are looking for Kubernetes integration. For most users transitioning from Docker Desktop, Rancher Desktop and Podman provide the closest functionality and ease of use.
