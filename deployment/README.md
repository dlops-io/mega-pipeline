# Deployment

## Start Docker Container
To start the docker container run:  
`sh ./docker-shell.sh`

## API's to enbale in GCP
* Compute Engine API
* Service Usage API
* Cloud Resource Manager API
* Google Container Registry API

## SSH Setup
#### Configuring OS Login for service account
```
gcloud compute project-info add-metadata --project ac215-project --metadata enable-oslogin=TRUE
```

#### Create SSH key for service account
```
cd /secrets
ssh-keygen -f ssh-key-ai5-project
cd /app
```

#### Providing public SSH keys to instances
```
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-ai5-project.pub
```
From the output of the above command keep note of the username. Here is a snippet of the output 
```
 - accountId: ai5-project
    gid: '4241727572'
    homeDirectory: /home/sa_105148290446446408899
    name: users/deployment@ai5-project.iam.gserviceaccount.com/projects/ai5-project
    operatingSystemType: LINUX
    primary: true
    uid: '4241727572'
    username: sa_105148290446446408899
```
The username is `sa_105148290446446408899`




```
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-ac215-project.pub
```
From the output of the above command keep note of the username. Here is a snippet of the output 
```
- accountId: ac215-project
    gid: '3906553998'
    homeDirectory: /home/sa_100110341521630214262
    name: users/deployment@ac215-project.iam.gserviceaccount.com/projects/ac215-project
    operatingSystemType: LINUX
    primary: true
    uid: '3906553998'
    username: sa_100110341521630214262
```
The username is `sa_100110341521630214262`


## Deployment Setup
* GCP project details in env.dev file
* GCP project details in inventory-dev.yml file
* GCP Compute instance details in inventory-dev.yml file
* GCP project details in inventory-prod.yml file
* GCP Compute instance details in inventory-prod.yml file

## Deployment
#### Create Server in GCP
```
ansible-playbook deploy-gcp-setup.yml -i inventory.yml --extra-vars cluster_state=present

ansible-playbook deploy-create-instance.yml -i inventory.yml

```
Once the command runs successfully get the IP address of the compute instance from GCP and update the appserver>hosts in inventory-dev.yml or inventory-prod.yml file

#### Provision Dev Server in GCP
```
ansible-playbook deploy-provision-instance.yml -i inventory.yml
```

```
ansible-playbook deploy-setup-folders.yml -i inventory.yml
```

#### Build and Push Docker Containers to GCR
```
ansible-playbook deploy-docker-images.yml -i inventory.yml
```


#### Deploy Docker Containers to Server
```
ansible-playbook deploy-setup-containers.yml -i inventory.yml
```

#### Setup Webserver on Dev Server in GCP : Step 1
# SSL Setup
Comment out the second server {} section in nginx.conf when first running ansible-playbook deploy-setup-webserver.yml -i inventory.yml
Go to http://34.29.2.239/ to makes sure nginx default page comes up
Go to http://ac215-mega-pipeline.dlops.io/ to makes sure nginx default page comes up

Go to http://35.184.127.42/ to makes sure nginx default page comes up
Go to http://ai5-mega-pipeline.dlops.io/ to makes sure nginx default page comes up

```
ansible-playbook deploy-setup-webserver.yml -i inventory.yml
```

Once server is up run:
sudo docker run --rm --name temp_certbot \
    -v /data/certbot/letsencrypt:/etc/letsencrypt \
    -v /data/certbot/www:/tmp/letsencrypt \
    -v /data/servers-data/certbot/log:/var/log \
    certbot/certbot:v1.8.0 \
    certonly --webroot --agree-tos --renew-by-default \
    --preferred-challenges http-01 --server https://acme-v02.api.letsencrypt.org/directory \
    --text --email shivasj@gmail.com \
    -w /tmp/letsencrypt -d ai5-mega-pipeline.dlops.io

sudo docker run --rm --name temp_certbot \
    -v /data/certbot/letsencrypt:/etc/letsencrypt \
    -v /data/certbot/www:/tmp/letsencrypt \
    -v /data/servers-data/certbot/log:/var/log \
    certbot/certbot:v1.8.0 \
    certonly --webroot --agree-tos --renew-by-default \
    --preferred-challenges http-01 --server https://acme-v02.api.letsencrypt.org/directory \
    --text --email shivasj@gmail.com \
    -w /tmp/letsencrypt -d ac215-mega-pipeline.dlops.io

You should see successfull result like this:
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/ac215-mega-pipeline.dlops.io/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/ac215-mega-pipeline.dlops.io/privkey.pem
   Your cert will expire on 2023-12-10. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le


Un-comment out the server {} section in nginx.conf and run ansible-playbook deploy-setup-webserver.yml -i inventory.yml
Go to https://ac215-mega-pipeline.dlops.io/ 
Go to https://ai5-mega-pipeline.dlops.io/ 
========


<!-- Once the command runs you can go to `http://34.29.2.239/` and you should see the default nginx page. If you setup the DNS record for ac215-mega-pipeline.dlops.io then you can go to http://ac215-mega-pipeline.dlops.io/ and you should see the default nginx page
When running the above command for the very first time comment the line: `include /etc/nginx/sites-enabled/*;` -->




Once the command runs you can go to `http://34.70.35.238/` and you should see the default nginx page. If you setup the DNS record for ai5.dlops.io then you can go to http://ai5.dlops.io/ and you should see the default nginx page
When running the above command for the very first time comment the line: `include /etc/nginx/sites-enabled/*;`







After containers are setup uncomment `include /etc/nginx/sites-enabled/*;` and run setup-webserver again
 
You can SSH into the server from the GCP console and see status of containers
```
sudo docker container ls
sudo docker container logs api-service -f
```