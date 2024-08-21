Below is a more detailed setup for Apache Kafka using Docker Compose. This version includes Kafka, Zookeeper, and a Kafka UI tool for easier management. Additionally, I'll include installation instructions for Docker and Docker Compose, as well as the `docker-compose.yml` script.

### Installation Instructions

#### 1. **Install Docker**

- **For Ubuntu/Debian**:
  ```bash
  sudo apt-get update
  sudo apt-get install -y \
      ca-certificates \
      curl \
      gnupg \
      lsb-release

  sudo mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```

- **For Windows/Mac**: Download Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop) and follow the installation instructions.

#### 2. **Install Docker Compose**

If Docker Compose is not bundled with Docker (as it is on some Linux distributions):

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:

```bash
docker-compose --version
```

### Docker Compose Setup for Kafka

Here’s the `docker-compose.yml` file with more details:

```yaml
version: '3.8'

services:
  zookeeper:
    image: zookeeper:3.8
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper

  kafka:
    image: confluentinc/cp-kafka:7.3.1
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_LOG_DIRS: /var/lib/kafka
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - kafka_data:/var/lib/kafka
    depends_on:
      - zookeeper

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
      KAFKA_CLUSTERS_0_METRICS_PORT: 8081
    depends_on:
      - kafka
    restart: always

volumes:
  zookeeper_data:
    driver: local
  kafka_data:
    driver: local

networks:
  default:
    name: kafka_network
```

### Setup and Usage Instructions

1. **Create a Directory for Kafka Setup**:
   ```bash
   mkdir kafka-docker && cd kafka-docker
   ```

2. **Create the `docker-compose.yml` File**:
   ```bash
   touch docker-compose.yml
   ```

3. **Paste the Above Content** into `docker-compose.yml`.

4. **Start the Docker Compose Stack**:
   ```bash
   docker-compose up -d
   ```

5. **Access the Kafka UI**:

   - Open your browser and go to `http://localhost:8080`.
   - This UI allows you to manage Kafka topics, consumers, and more.

6. **Verify Kafka and Zookeeper**:

   - Kafka should be running on `localhost:9092`.
   - Zookeeper should be running on `localhost:2181`.

### Additional Details

- **Volumes**:
  - `zookeeper_data` and `kafka_data` are defined to persist the data between container restarts.

- **Kafka UI**:
  - The `kafka-ui` service provides a user interface to interact with your Kafka cluster, making it easier to manage topics, partitions, and view consumer details.

- **Networks**:
  - The `kafka_network` is defined to ensure services can communicate within the same Docker network.

This setup is a bit more comprehensive and suitable for development or testing environments, even on a notebook.
