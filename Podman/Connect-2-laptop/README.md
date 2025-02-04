\#podman \#localnetwork \#powsgres \#postgresql

# An issue: configure access from 1st laptop (developer) to 2nd laptop (containers)
- I use in this example Podman on Windows OS - is a 2nd laptop;
- Developer laptop is Windows as well;
- Both laptops are in the same local network 192.168.22.0/24;

# compose.yaml 

    services:
      pg-okx-service:
        image: 'postgres:15.7'
        container_name: pg-okx-service
        environment:
          - 'POSTGRES_DB=db_bot_okx'
          - 'POSTGRES_USER=dbpwd'
          - 'POSTGRES_PASSWORD=dbpwd'
        volumes:
          - pg_data_okx:/var/lib/postgresql/data
        networks:
          podman-okx-net:
            ipv4_address: 192.168.144.2  # Assign static IP within the subnet
        ports:
          - '11234:5432'
    
    volumes: 
      pg_data_okx:
    
    networks:
      podman-okx-net:
        #external: true  # Use the manually created network
        driver: bridge
        ipam:
          config:
            - subnet: 192.168.144.0/30
    
            
