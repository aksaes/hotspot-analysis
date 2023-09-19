Hotspot Analysis
Minikube is started first and dashboard launched for viewing the cluster.

```
minikube start --driver=docker --cpus=7 --memory=7g 
minikube dashboard
```
After this, kafka service and deployment is created using zookeeper-setup.yaml and kafka-setup.yaml.

```
kubectl apply -f .\zookeeper-setup.yaml
kubectl apply -f .\kafka-setup.yaml
```
After this, helm is installed and executed to create the Kafka Connect Neo4j Connector, neo4j service created and service deployment for Kafka and Neo4j connection is created.

```
helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml
kubectl apply -f neo4j-service.yaml
kubectl apply -f kakfa-neo4j-connector.yaml
```

Port-forwarding is done to allow the services and database to be accessible from outside the minikube cluster.
```
kubectl port-forward svc/neo4j-service 7474:7474 7687:7687
kubectl port-forward svc/kafka-service 9092:9092
```

Now the database is loaded with the data from the dataset using 

```
python3 data_producer.py
```

PageRank and BFS is implemented in interface.py and tested using 

```
python3 tester.py
```
