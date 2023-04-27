# asunny2-project-2
Minikube is started first.

```
minikube start --driver=docker
```
After this, kafka deployment is created. For that zookeeper-setup.yaml and kafka-setup.yaml is completed.

Then the deployments and services are created using the following commands.

```
kubectl apply -f .\zookeeper-setup.yaml
kubectl apply -f .\kafka-setup.yaml
```
After this, created another python pod using python-setup.yaml

```
kubectl apply -f .\python-setup.yaml
```

Copied the custom_data_producer.py into the python pod using

```
kubectl cp custom_data_producer.py python-pod:custom_data_producer.py
```

Tested the kafka service from within the deployment using the script.