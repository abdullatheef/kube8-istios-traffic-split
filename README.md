This codebase allows 3 types of running services
1. Straight forward running each application
2. docker compose
3. kubernetes

1. Straight forward running each application

./run.sh

verify : http://localhost:8010

2. docker compose

docker-compose up --build

verify : http://localhost


3. Kubernetes

cd kube
kubectl apply -f .


kubectl port-forward pod/<nginx> -n todo-app  8010:80
kubectl port-forward pod/<django> -n todo-app  8000:8000

verify : http://localhost:8010










