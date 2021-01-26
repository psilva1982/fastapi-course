#!/bin/bash
# Script for automate deploy 
ssh root@172.17.0.2 'rm -r ~/bookstore/bookstoreAPI'
scp -r ../bookstoreAPI root@172.17.0.2:~/bookstore

ssh root@172.17.0.2 'docker stop bookstore-api'
ssh root@172.17.0.2 'docker rm bookstore-api'

ssh root@172.17.0.2 'docker build -t bookstore-build ~/bookstore/bookstoreAPI'
ssh root@172.17.0.2 'docker run -idt -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build'


ssh root@172.17.0.2 'docker stop api-nginx'
ssh root@172.17.0.2 'docker rm api-nginx'

ssh root@172.17.0.2 'docker build -t bookstore-nginx ~/bookstore/bookstoreAPI/nginx-reverse-proxy'
ssh root@172.17.0.2 'docker run -idt --name=api-nginx -p 80:80 bookstore-nginx'

