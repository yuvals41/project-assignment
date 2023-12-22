# project-assignment
For this project i used kind cluster because its lightweight and flexible

I used it on my linux machine

## prerequisites
[docker](https://docs.docker.com/engine/install/)

[helm](https://helm.sh/docs/intro/install/)

[kubectl](https://kubernetes.io/docs/tasks/tools/)

## To download 

Mac:

```
brew install kind
```

Linux
```
sudo port selfupdate && sudo port install kind
```

Windows
```
choco install kind
```

## Create a kind cluster with the following configuration in order for us to reach the cluster from the localhost(make sure port 80 is available)
```
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
EOF
```


## Than make sure to use the cluster
```
kubectl config use-context kind-kind
```


## Install nginx with the following configuration
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm upgrade --install -n kube-system ingress-nginx ingress-nginx/ingress-nginx \
    --set controller.hostPort.enabled=true \
    --set controller.admissionWebhooks.enabled=false
```


## Install both services
```
helm upgrade --install -f useless-values.yaml useless Kubernetes/
helm upgrade --install -f funny-values.yaml funny Kubernetes/
```

After one minute because the nginx controller takes a few seconds to be ready you can try to access the endpoints

```
curl http://localhost/funnyfact
curl http://localhost/uselessfact
```


## NOTES

- In the assignment it was written to use two domains, because its a local development its not possible(unless you change the hosts file) so i used localhost for this i hope its okay

- In the assignment, in the github actions part it was written to deploy the helm chart with github actions workflow, because its a local cluster its not possible to a github machine to deploy it on my local cluster so i wrote the commands to deploy my chart but i ignored the error, you can see it on .github/workflows/ci-cd.yml file.
  basically i assume the the pipeline will deploy to a cluster where the applictions are exposed in domain-1 and domain-2 to the world, but i my local cluster chart i exposed the ingress only to localhoat with the two routes


Enjoy and Thank you!