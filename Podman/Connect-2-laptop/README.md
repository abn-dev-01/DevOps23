\#podman \#localnetwork \#powsgres \#postgresql

# An issue: configure access from 1st laptop (developer) to 2nd laptop (containers)
- I use in this example Podman on Windows OS - is a 2nd laptop;
- Developer laptop is Windows as well;
- Both laptops are in the same local network 192.168.22.0/24;

# Instructions before starting `podman compose`

Open CDM as Administrator and run:

        netsh interface portproxy add v4tov4 listenaddress=192.168.22.248 listenport=11234 connectaddress=192.168.144.2 connectport=5432

Where are:
- `192.168.22.248` is your external IP address (Wifi or ETH) you are going to connect here;
- `11234` - is an external port for a connection from 1st laptop, for example from DBEaver app;
- `192.168.144.2` is an IP Address of Postgres in WSL of Podman (Virtual IP address)
- `5432` is a standard Postgres system port - is the port inside a container.

## Check forwarding:

        netsh interface portproxy show v4tov4
        
        Listen on ipv4:             Connect to ipv4:
        
        Address         Port        Address         Port
        --------------- ----------  --------------- ----------
        192.168.22.248  11234       192.168.144.2   5432


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

#


