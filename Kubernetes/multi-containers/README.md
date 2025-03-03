# How to create a Pod with 3 different containers? 

    To create a Pod with three different containers, you need to define 
    a multi-container Pod in a Kubernetes YAML manifest. 
    These containers will share the same network namespace, allowing them 
    to communicate via localhost, and they can share storage using emptyDir volumes.


## 1. YAML Definition for a Multi-Container Pod

```
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: trading-system
spec:
  containers:
    - name: app-container
      image: openjdk:17
      command: ["/bin/sh", "-c", "while true; do echo 'App is running'; sleep 10; done"]
      ports:
        - containerPort: 8080
      volumeMounts:
        - name: shared-data
          mountPath: /data

    - name: redis-cache
      image: redis:7
      command: ["redis-server"]
      ports:
        - containerPort: 6379
      volumeMounts:
        - name: shared-data
          mountPath: /cache

    - name: logging-agent
      image: busybox
      command: ["/bin/sh", "-c", "while true; do cat /data/logs.txt; sleep 5; done"]
      volumeMounts:
        - name: shared-data
          mountPath: /data

  volumes:
    - name: shared-data
      emptyDir: {}  # Shared storage between containers
```

---

## **2. Breakdown of This Configuration**
### **Containers:**
1. **`app-container` (Main Application)**
   - Runs a simple Java application (simulated with `openjdk:17`).
   - Listens on port **8080**.
   - Shares a volume `/data` with the other containers.

2. **`redis-cache` (In-Memory Database)**
   - Runs **Redis** for caching purposes.
   - Exposes port **6379**.
   - Uses the same **emptyDir** volume for potential shared data.

3. **`logging-agent` (Sidecar Container)**
   - Reads logs from `/data/logs.txt` every 5 seconds.

---

## **3. Deploy the Pod**
Apply the YAML configuration:
```bash
kubectl apply -f multi-container-pod.yaml
```

Check if the pod is running:
```bash
kubectl get pods
```

Check pod logs:
```bash
kubectl logs multi-container-pod -c app-container
kubectl logs multi-container-pod -c redis-cache
kubectl logs multi-container-pod -c logging-agent
```

---

## **4. Internal Communication**
- The three containers **share the same localhost network**.
- The **app-container** can communicate with Redis via `localhost:6379`:
  ```bash
  redis-cli -h localhost -p 6379
  ```
- Logs are shared in `/data/logs.txt` (via `emptyDir`).

---

## **5. When to Use a Multi-Container Pod?**
- **Tightly coupled components** (e.g., app + Redis cache + logger).
- **Sidecar containers** (logging, monitoring, or security agents).
- **Shared storage needs** using `emptyDir`, `PersistentVolumeClaim`, etc.

Would you like me to modify this to include **Liveness/Readiness Probes or Resource Limits**? 🚀
