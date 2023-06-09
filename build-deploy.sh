rm -rf sm-bank-transaction

git clone https://github.com/sen31088/sm-bank-transaction.git

cd sm-bank-transaction


name=`cat version.json | jq -r '.name'`
version=`cat version.json | jq -r '.version'`
docker_hub='sen31088'
#docker_repo='sm-bank-home'

#docker build 

docker build -t $docker_hub/$name:$version .

# Docker Push

docker push $docker_hub/$name:$version

#Deployment

sed -i "s/{{theversion}}/$version/g" resources/deployment.yaml

kubectl apply -f resources/deployment.yaml

kubectl apply -f resources/service.yaml


