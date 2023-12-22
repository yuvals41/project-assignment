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


## Then make sure to use the cluster
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

- In the assignment, it was written to use two domains, because it's a local development it's not possible(unless you change the hosts file) so I used localhost for this I hope it's okay

- In the assignment, in the GitHub actions part it was written to deploy the helm chart with GitHub actions workflow, because it's a local cluster it's not possible to a GitHub machine to deploy it on my local cluster so I wrote the commands to deploy my chart but I ignored the error, you can see it on .github/workflows/ci-cd.yml file.
  basically, I assume the the pipeline will deploy to a cluster where the applications are exposed in domain-1 and domain-2 to the world, but on my local cluster chart I exposed the ingress only to localhost with the two routes so you can see I exposed them properly
  Of course, if it was on a public Kubernetes cluster I would expose those domains on the ingress and route them to the right microservices

If you have any questions or wonders feel free to ask me what i did and why
Enjoy and Thank you!
