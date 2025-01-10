
# Setting Up Local Kafka Container for Spring Boot Application

* For registering the containers with Docker Desktop, we will use the following command:

       docker-compose up -d

*  Create the required topics using Docker Desktop console using the following command:

       kafka-topics --create --topic user-notification --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092


Now that the container is up and the required prerequisites have been performed, we can launch the Spring Boot application.  

For the Spring Boot application, configure the Kafka bootstrap address as below:

    kafka.bootstrapAddress=localhost:9092

\#application
\#Docker (software)
\#kafka
\#Spring Boot
