This codebase consists kubernetes basic app and traffic split

* Install helm
* Install istios
   
```
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm install istio-base istio/base -n istio-system --set defaultRevision=default --create-namespace 
helm install istiod istio/istiod -n istio-system --wait




kubectl apply -f kube # (try 2 times)
kubectl port-forward pod/<nginx> -n todo-app  8010:80
kubectl port-forward pod/<django> -n todo-app  8000:8000

```
verify localhost:8010











