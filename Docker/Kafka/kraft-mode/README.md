Yes, you can run Kafka without Zookeeper by using **KRaft mode** (Kafka Raft). KRaft is a feature introduced in Apache Kafka that allows Kafka to operate without the need for Zookeeper by integrating the metadata management within Kafka brokers themselves. Below is a `docker-compose.yml` file for running Kafka in KRaft mode.

### [`docker-compose.yml`](./docker-compose.yml) for Kafka in KRaft Mode

```yaml
version: '3.8'
##########################################################################################
#
#  docker-compose.yml for Kafka in KRaft Mode
#
##########################################################################################

services:
  kafka:
    image: bitnami/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
      - "9093:9093"  # Internal communication
    environment:
      - KAFKA_CFG_NODE_ID=1
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@localhost:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
      - KAFKA_CFG_LOG_DIRS=/bitnami/kafka/data
      - KAFKA_ENABLE_KRAFT=yes
    volumes:
      - ./docker/kafka_data:/bitnami/kafka/data

  # kafka-ui:
  #   image: provectuslabs/kafka-ui:latest
  #   container_name: kafka-ui
  #   ports:
  #     - "8080:8080"
  #   environment:
  #     - KAFKA_CLUSTERS_0_NAME=kraft-cluster
  #     - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092
  #   depends_on:
  #     - kafka

volumes:
  kafka_data:
    driver: local

networks:
  default:
    name: kafka_network
```

### Explanation and Usage

1. **KRaft Mode Setup**:
   - `KAFKA_PROCESS_ROLES: broker,controller`: Specifies that this node will act as both a broker and a controller.
   - `KAFKA_CONTROLLER_QUORUM_VOTERS: "1@localhost:9093"`: Sets up the controller quorum voters; since this is a single-node setup, only one controller is defined.
   - `KAFKA_LISTENERS` and `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`: Define listeners and their protocols for client communication and inter-broker communication.
   - `KAFKA_ADVERTISED_LISTENERS`: The listener advertised to clients; typically set to the public address or hostname.

2. **Kafka UI**:
   - A Kafka UI tool is included, making it easier to manage topics, partitions, and other Kafka resources.

3. **Volumes**:
   - The `kafka_data` volume ensures that Kafka’s data is persisted across container restarts.

4. **Starting the Services**:
   - Use `docker-compose up -d` to start Kafka and the UI.

5. **Access Kafka UI**:
   - Access the Kafka UI at `http://localhost:8080`.

### Starting Kafka in KRaft Mode

This setup allows you to start Kafka without Zookeeper, using the newer KRaft mode. It's more lightweight and should run efficiently on a notebook, making it suitable for development and testing purposes.
