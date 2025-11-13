# Python setup

```bash
pyenv local 3.10.18
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Build Docker image

```bash
# Build
docker build \
  --platform linux/amd64 \
  -t 192.168.0.112:5000/auth:latest .

# Push
docker push 192.168.0.112:5000/auth:latest

curl http://ubuntu:5000/v2/_catalog
curl http://ubuntu:5000/v2/auth/tags/list
```

```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f auth-deploy.yaml
kubectl apply -f service.yaml

# Scale down to 1 to ensure it works
kubectl scale deployment auth --replicas=1

# See the services
kubectl get services
```

# Test the auth service

Since your auth service is of ClusterIP type, it's only reachable from within your Kubernetes cluster, which is why you're not seeing an external IP.

```bash
# kubectl port-forward service/auth <local_port>:<pod_port>
kubectl port-forward service/auth 5000:5000
```

## Test the login
```bash
# curl -X POST \
# -H "Content-Type: application/json" \
# -H "Authorization: Basic $(echo -n 'david@email.com:xxx' | base64)" \
# http://localhost:5000/login

JWT_TOKEN=$(curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'david@email.com:xxx' | base64)" \
  http://localhost:5000/login)
```

## Test the validate
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  http://localhost:5000/validate
```