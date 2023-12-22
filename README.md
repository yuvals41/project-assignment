# Project-assignment
For this project i used kind cluster because its lightweight and flexible

I used it on my linux and windows machines it should work on Mac also

# For local Tests with docker only
```
docker buildx build -t yuvals41/webapp:v1 Application/
```

then run different containers with different environment variables

```
docker run -p 8080:8080 -d -e FUNNY_FACT_URL=https://api.chucknorris.io/jokes/random yuvals41/webapp:v1
docker run -p 8081:8080 -d -e USELESS_FACT_URL=https://uselessfacts.jsph.pl/api/v2/facts/random yuvals41/webapp:v1
```

test it
```
curl localhost:8080/funnyfact
curl localhost:8081/uselessfact
```

# For Local Kubernetes
## Prerequisites
[docker](https://docs.docker.com/engine/install/)

[helm](https://helm.sh/docs/intro/install/)

[kubectl](https://kubernetes.io/docs/tasks/tools/)

And git clone the repo

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

## Create a kind cluster with the following configuration in order for us to reach the cluster from the localhost(make sure port 80 is available), on windows use git bash
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


## Install nginx ingress controller with the following configuration
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm upgrade --install -n kube-system ingress-nginx ingress-nginx/ingress-nginx \
    --set controller.hostPort.enabled=true \
    --set controller.admissionWebhooks.enabled=false
```


## Install both services
```
helm upgrade --install -f Kubernetes/useless-values.yaml useless Kubernetes/
helm upgrade --install -f Kubernetes/funny-values.yaml funny Kubernetes/
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

If you have any questions or wonders feel free to ask me what and why i did

Enjoy and Thank you!
