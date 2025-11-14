# Set UP

```bash

ARGO_WORKFLOWS_VERSION="v3.7.3"  # or whatever version you choose
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/quick-start-minimal.yaml"

# Check status
kubectl -n argo get pods -l app=argo-server
kubectl -n argo get pods -w

# Install argo CLI
# https://github.com/argoproj/argo-workflows/releases/?utm_source=chatgpt.com
```

This creates:

- Namespace: argo
- Controller SA: argo
- Argo Server SA: argo-server
- Minimal RBAC (missing permissions for new CRDs)
You will run all workflows inside namespace argo, which is recommended for the minimal install.

Submit example
```bash
argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo-workflows/main/examples/hello-world.yaml
```

# Accessing UI

Simplest way now (since you’re using Minikube with none driver) — just expose the Argo UI via NodePort so it’s reachable from your Mac:

Set a fixed NodePort
```bash
kubectl -n argo patch svc argo-server -p '{
  "spec": {
    "type": "NodePort",
    "ports": [{
      "port": 2746,
      "targetPort": 2746,
      "nodePort": 32045
    }]
  }
}'
kubectl -n argo get svc argo-server
```

Then access `https://192.168.0.112:32045/` in Mac

Try to ping from Mac The Workflows UI
```bash
curl -vk https://192.168.0.112:32045/healthz
```

# RBAC

# Fix RBAC so the wait container can write WorkflowTaskResults

Required because `quick-start-minimal.yaml` does NOT include RBAC for Argo v3.7.x CRDs.

```yaml
# argo-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-workflowtaskresults-role
  namespace: argo
rules:
  - apiGroups: ["argoproj.io"]
    resources:
      - workflowtaskresults
    verbs: ["create", "get", "list", "watch", "patch", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: argo-workflowtaskresults-binding
  namespace: argo
subjects:
  - kind: ServiceAccount
    name: argo
    namespace: argo
roleRef:
  kind: Role
  name: argo-workflowtaskresults-role
  apiGroup: rbac.authorization.k8s.io
```

Apply it `kubectl apply -f argo-rbac.yaml`

```bash
kubectl create clusterrolebinding argo-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=argo:argo
```