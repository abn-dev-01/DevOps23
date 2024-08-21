Here’s a minimal `docker-compose.yml` script to set up Apache Kafka with Zookeeper. This setup is simple and should work well on your notebook.

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

  kafka:
    image: confluentinc/cp-kafka:7.3.1
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper

networks:
  default:
    name: kafka_network
```

### Instructions:

1. **Create a directory** for your Kafka setup:

   ```bash
   mkdir kafka-docker && cd kafka-docker
   ```

2. **Create the `docker-compose.yml` file**:

   ```bash
   touch docker-compose.yml
   ```

3. **Paste the above content** into your `docker-compose.yml`.

4. **Start the services**:

   ```bash
   docker-compose up -d
   ```

5. **Verify Kafka is running**:

   - Kafka should be accessible on `localhost:9092`.
   - Zookeeper should be accessible on `localhost:2181`.

This setup uses a single broker and is configured for minimal resource usage, making it suitable for running on a notebook.
