# Create a container registry locally

In your Ubuntu run:

```bash
docker run -d \
  -p 5000:5000 \
  -v /opt/registry/data:/var/lib/registry \
  --restart=always \
  --name registry \
  registry:2
```

We are setting a volume in `/opt/registry/data` to persist images between restarts.

## Ensure you can reach it

Access an HTTP registry of containers:

- From Ubuntu: `curl http://localhost:5000/v2/_catalog`
- From Mac: `curl http://192.168.0.112:5000/v2/_catalog`
The result should be `{"repositories":[]}`.

## Mark registry to be trusted by Docker over HTTPS

By default, Docker only trusts registries over HTTPS.
Since this is your private LAN, we’ll configure both Docker daemons to allow HTTP.

### On Mac
Since we are using `colima` in our Mac we should configure the `Insecure Registries`:

```bash
code ~/.colima/default/colima.yaml
```

```bash
# Colima default behaviour: buildkit enabled
# Default: {}
docker:
  insecure-registries:
    - "192.168.0.112:5000"
```

Now Colima’s internal Docker daemon (the one your CLI uses) will happily push/pull to your Ubuntu registry.

Restart to apply changes:

```bash
colima stop
colima start
```


### On Ubuntu

```bash
# Edit the daemon to include insecure registries
sudo nano /etc/docker/daemon.json

{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "insecure-registries": [
        "192.168.0.112:5000"
    ]
}

# Restart to apply changes
sudo systemctl restart docker


# Ensure docker restarted
sudo systemctl status docker --no-pager

# Ensure insecure registry is there
docker info | grep -A3 'Insecure Registries'
```