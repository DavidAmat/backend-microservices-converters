```bash
docker build -t mysql-db .
docker run --name mysql-container --env-file ./.env -p 3306:3306 -d mysql-db
docker exec -it mysql-container bash
mysql -u root -p
# Remove
docker rm mysql-container
```

# Init SQL
You should remove the lines that create the user and database, as these are handled by the environment variables (MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE) and the Docker entrypoint. Your init.sql should primarily focus on creating tables and inserting initial data within the database that has already been created.

# Push to local registry

```bash
docker build \
  --platform linux/amd64 \
  -t 192.168.0.112:5000/mysql-db:latest .
docker images
docker push 192.168.0.112:5000/mysql-db:latest
```

# Run the manifests

Run the `k apply -f` for each manifest

# SSH into the pod

```bash
# get in k9s the pod name
# SSH into the pod
kubectl exec -it mysql-deployment-84ccd5d966-5b682 -- bash
```

Run MySQL client:
```bash
mysql -u root -p -h 127.0.0.1
```