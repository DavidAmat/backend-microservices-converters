# Create containerd registry config

Tell containerd that localhost:5000 is a trusted local registry:


```bash
sudo mkdir -p /etc/containerd/certs.d/localhost:5000
sudo tee /etc/containerd/certs.d/localhost:5000/hosts.toml <<EOF
server = "http://localhost:5000"

[host."http://localhost:5000"]
  capabilities = ["pull", "resolve"]
EOF

sudo systemctl restart containerd

```

In the YAML manifest for the deployment

```bash
image: localhost:5000/fastapi-demo:latest
imagePullPolicy: IfNotPresent
```

then apply it

# Cheatsheet

```bash
# UBUNTU
curl http://localhost:5000/v2/_catalog
curl http://localhost:5000/v2/fastapi-demo/tags/list

# MAC
curl http://192.168.0.112:5000/v2/_catalog
curl http://192.168.0.112:5000/v2/fastapi-demo/tags/list

```