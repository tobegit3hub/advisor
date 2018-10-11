# Server

## Command-line

```bash
advisor_admin server start
```

## Docker

```bash
docker run -d -p 8000:8000 tobegit3hub/advisor
```

## Docker Compose

```bash

wget https://raw.githubusercontent.com/tobegit3hub/advisor/master/docker-compose.yml

docker-compose up -d
```

## Kubernetes

```bash
wget https://raw.githubusercontent.com/tobegit3hub/advisor/master/kubernetes_advisor.yaml

kubectl create -f ./kubernetes_advisor.yaml
```

## From Source

```bash
git clone --depth 1 https://github.com/tobegit3hub/advisor.git && cd ./advisor/

pip install -r ./requirements.txt

./manage.py migrate

./manage.py runserver 0.0.0.0:8000
```