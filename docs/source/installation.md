# Installation

## Pip

```bash
pip install advisor
```

## From Source

```bash
git clone git@github.com:tobegit3hub/advisor.git

cd ./advisor/advisor_client/

python ./setup.py install
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