# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# gds plugin installation
RUN wget -O neo4j-graph-data-science-2.3.1.zip https://graphdatascience.ninja/neo4j-graph-data-science-2.3.1.zip && \
    unzip neo4j-graph-data-science-2.3.1.zip && \
    mv neo4j-graph-data-science-2.3.1.jar /var/lib/neo4j/plugins/ && \
    rm neo4j-graph-data-science-2.3.1.zip && \
    sed -i 's/#dbms.security.procedures.unrestricted=.*/dbms.security.procedures.unrestricted=gds\.\*/' /etc/neo4j/neo4j.conf

# Change password
RUN neo4j-admin dbms set-initial-password project2phase1

# Enable remote access
RUN sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/' /etc/neo4j/neo4j.conf

# Install git
RUN apt-get update && \
    apt-get install -y git

# Setting the Github Token as environment variable
ENV GITHUB_TOKEN=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

WORKDIR /cse511

# Download python script from git repo
RUN git clone https://CSE511-SPRING-2023:${GITHUB_TOKEN}@github.com/CSE511-SPRING-2023/asunny2-project-2.git /cse511/

# Download dataset
RUN wget -O yellow_tripdata_2022-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet

# Install required python packages
RUN pip install --upgrade pip && \
    pip install neo4j pandas pyarrow

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
