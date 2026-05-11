## Contents
- [Phase 1: Docker](#phase-1-docker)  
    - [Step 1: The Dockerfile and .dockerignore](#step-1-the-dockerfile-and-dockerignore)  
    - [Step 2: Building the Docker image](#step-2-building-the-docker-image)
    - [Step 3: Running the Docker container](#step-3-running-the-docker-container)
    - [Step 4: Accessing the application](#step-4-accessing-the-application)
- [Phase 2: EC2 Deployment + Containerization](#phase-2-ec2-deployment--containerization)
    - [Step 1: Creating and launching the EC2 instance](#step-1-creating-and-launching-the-ec2-instance)
    - [Step 2: Connecting to EC2 instance(SSH)](#step-2-connecting-to-ec2-instance-ssh)
    - [Step 3: Installing git and cloning the repo into the instance](#step-3-installing-git-and-cloning-the-repo-into-the-instance)
    - [Step 4: Installing Docker and Containerization](#step-4-installing-docker-and-containerization)
- [Phase 3: Jenkins Installation + Jenkins pipeline construction + Docker Hub integration](#phase-3-jenkins-installation--jenkins-pipeline-construction--docker-hub-integration)
    - [Step 1: Install Java and add Jenkins repository](#step-1-install-java-and-add-jenkins-repository)
    - [Step 2: Install Jenkins](#step-2-install-jenkins)
    - [Step 3: Further Jenkins setup through Jenkins UI](#step-3-further-jenkins-setup-through-jenkins-ui)
    - [Step 4: Creating Jenkins pipeline](#step-4-creating-jenkins-pipeline)
    - [Step 5: Integrating Docker Hub](#step-5-integrating-docker-hub)
- [Phase 4: Kubernetes Orchestration](#phase-4-kubernetes-orchestration)
    - [Step 1: Install K3s](#step-1-install-k3s)
    - [Step 2: Creating deployment.yml file](#step-2-creating-deploymentyml-file)
    - [Step 3: Kubernetes service](#step-3-kubernetes-service)
    - [Step 4: Deploy kubernetes resources](#step-4-deploy-kubernetes-resources)
    - [Step 5: Jenkins and Kubernetes integration](#step-5-jenkins-and-kubernetes-integration)
- [Phase 5: Monitoring and Visualization with Prometheus and Grafana](#phase-5-monitoring-and-visualization-with-prometheus-and-grafana)
    - [Step 1: Install Helm](#step-1-install-helm)
    - [Step 2: Install kube-prometheus-stack](#step-2-install-kube-prometheus-stack)
    - [Step 3: Expose Grafana using NodePort](#step-3-expose-grafana-using-nodeport)
    - [Step 4: Access Grafana dashboard](#step-4-access-grafana-dashboard)


## Phase 1: Docker
### Docker helps in containerizing an application which ensures that the application runs consistently across different environments such as local machines, cloud servers, CI/CD pipelines, and Kubernetes clusters.
### In this step we write the Dockerfile, .dockerignore file, build the image from the Dockerfile and run our container off of the built image

#### Step 1: The Dockerfile and .dockerignore
- Before building the image we need to define all the instructions Docker would follow while building the image. 
- These instructions are defined in the Dockerfile. A Docker file executes instructions, copies various files etc.. 
- To ensure no unnecessary files are copied a .dockerignore file is created  
Example:
```dockerignore
__pycache__/
.venv/
.git/
.env
.ipynb_checkpoints/
```
- Next we write the Dockerfile 
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0"]
```

#### Step 2: Building the Docker image
- The Docker image is built using the following command
```bash
docker build -t resumeiq .
```
- "docker build" creates the image
- "-t resumeiq" assigns the image name
- "." specifies the current directory as build context

#### Step 3: Running the Docker container
- The Docker container was started using
```bash
docker run -d -p 8501:8501 resumeiq
```
- The "-d" makes the container run in detached mode
- The "-p" field allows the application to be accessed on the specified port
- By default, Streamlit uses port no. "8501"

#### Step 4: Accessing the application
- The application is now containerized
- The application can be accessed on localhost port 8501
```
http://localhost:8501
```

---

## Phase 2: EC2 Deployment + Containerization
### The objective of this phase is to deploy our application onto an EC2 instance so that it can be run on the cloud. We'll deploy the containerized version of our application. 
#### Step 1: Creating and launching the EC2 instance
- An EC2 instance is just a virtual machine running on the cloud
- This step involves starting and launching the ec2 instance for our application
- We proceed by providing the required permissions and resources to the instance  

EC2 configuration used:  
| Setting      | Value        |
|:-------------|:-------------|
| Instance type | m7i-flex.large     |
| Storage      | 50GB gp3     |
| OS           | Ubuntu       |
| Authentication | SSH key pair |  
  

Security group configuration:
| Port      | Purpose        |
|:-------------|:-------------|
| 22 | SSH     |
| 8080      | Jenkins     |
| 8501           | Streamlit|  
  

#### Step 2: Connecting to EC2 instance (SSH)
- Use SSH to securely connect to EC2 instance  


Command:
```bash
ssh -i <key.pem> ubuntu@<EC2-PUBLIC-IP>
```

- Before installing anything, update packages  


Command:
```bash
sudo apt update && sudo apt upgrade -y
```
#### Step 3: Installing git and cloning the repo into the instance
#### Install git to enable repository cloning and version control operations.
- Install git
```
sudo apt install git -y 
```
- Clone the repo
```
git clone https://github.com/hsharma-25/Cloud-Native-AI-Resume-Screening-System.git
```

#### Step 4: Installing Docker and Containerization
#### Docker helps us in containerizing an application. Containerization packages the application with its dependencies into isolated containers. This ensures that the application runs same everywhere and on evey device. 
- Install Docker on EC2 instance
```bash
sudo apt install docker.io -y
```

- Start and enable Docker using the following commands
- These commands start Docker and ensure Docker restarts on reboot
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

- Docker requires sudo access
- Allow normal users to run Docker commands
```bash
sudo usermod -aG docker ubuntu
```
- Apply changes
```bash
newgrp docker
```

- Now create the Dockerfile
- Use the same Dockerfile we created intially 
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0"]
```
Dockerfile explanation:
| Instruction | Purpose                          |
| ----------- | -------------------------------- |
| FROM        | Base Python image                |
| WORKDIR     | Sets container working directory |
| COPY        | Copies project files             |
| RUN         | Installs dependencies            |
| EXPOSE      | Exposes Streamlit port           |
| CMD         | Starts application               |


An extra index was used:
```
--extra-index-url https://download.pytorch.org/whl/cpu
```
The purpose:
- Installs CPU-only PyTorch
- Avoids unnecessary CUDA/GPU libraries
- Reduces image size
- Speeds up CI/CD builds

The .dockerignore file:
- Use the same .dockerignore file from earlier
- Helps reduces Docker build context size
- Pevents unnecessary files from entering image

Building the Docker image and running the Docker container
- Use the same commands we used for local containerization
```
docker build -t resumeiq .
```
```
docker run -d --name resumeiq-container -p 8501:8501 resumeiq
```
To access the application which is now running on the EC2 instance  
Type in browser:
```
http://<EC2-IP>:8501
```

#### Now our application is containerized and deployed on cloud using an EC2 instance. Cool :)

---

## Phase 3: Jenkins Installation + Jenkins pipeline construction + Docker Hub integration
### Jenkins is an automation server used  for CI/CD pipelines, automated build and deployments.
#### Step 1: Install Java and add Jenkins repository
#### Java runtime is required for running Jenkins. 
- Install Java
```
sudo apt install openjdk-21-jdk -y
```
- Add Jenkins GPG key
```
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```
Why?
- Ubuntu verifies packages before installing them.
- This key proves:
    - the package is really from Jenkins
    - it hasn’t been tampered with
- Without this key:
    - apt will not trust the Jenkins packages.

- Add Jenkins repository
```
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```
Why?
- By default, Ubuntu repositories do not contain the latest Jenkins version.
- After adding this repository, apt knows:
    - where to download Jenkins from
    - where to check for future updates

#### Step 2: Install Jenkins
- Update apt
```
sudo apt update 
```
- Install Jenkins
```
sudo apt install jenkins -y
```
- Start and enable jenkins
```
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

#### Step 3: Further Jenkins setup through Jenkins UI
- Access Jenkins through browser
```
http://<EC2-IP>:8080
```
- Retrieve initial admin password
```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
- On next step, click on intall suggested plug-ins
- Jenkins will install all required plug-ins by itself
Jenkins-Docker integration
- Jenkins runs under jenkins user
- This user requires Docker permissions
```
sudo usermod -aG docker jenkins
```
- To apply new permissions, restart jenkins
```
sudo systemctl restart jenkins
```
- Verify Docker access
```
sudo su - jenkins
docker ps
```
- The above command verifies that Jenkins can communicate with Docker daemon

#### Step 4: Creating Jenkins pipeline
#### The new job in Jenkins was created as a pipeline. In this method, the complete pipeline is defined as code in a file called Jenkinsfile. Futher we perform SCM (Source Code Management) integration to connect the jenkins pipeline to our GitHub repo.
- Create the jenkinsfile
- Push file to repo
```
pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t hsharma25/resumeiq:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push hsharma25/resumeiq:latest'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop resumeiq-container || true'
                sh 'docker rm resumeiq-container || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                    --name resumeiq-container \
                    -p 8501:8501 \
                    hsharma25/resumeiq:latest
                '''
            }
        }
    }
}
```
Pipeline stage explanation:
| Stage              | Purpose                      |
| ------------------ | ---------------------------- |
| Build Docker Image | Creates updated Docker image |
| Push Docker Image  | Uploads image to Docker Hub  |
| Stop Old Container | Removes previous deployment  |
| Run New Container  | Deploys latest application   |

- Click on "Build Now" in jenkins to start the whole process
- Observe the console to see how each step is executed
- Each step previously done manually like Docker build and Docker start is automated by Jenkins now

#### Step 5: Integrating Docker Hub
#### Similar to how GitHub stores source code, Docker Hub is a container registry to store images. From now on, Jenkins will build image -> push it to Docker Hub and deployments will pull image from Docker Hub when required
- On EC2, log in to Docker hub
```
docker login
```
- Build tagged image
```
docker build -t hsharma25/resumeiq:latest .
```
- Push image to Docker hub
```
docker push hsharma25/resumeiq:latest
```

---

## Phase 4: Kubernetes Orchestration
### Docker alone can not handle automatic recovery, scaling, orchestration, cluster management etc.. Kubernetes solves this by managing containers, deployments, networking, self-healing and scaling. This phase focuses on installing Kubernetes, defining deployment and service manifests and integrating K8s with the Jenkins pipeline

#### Step 1: Install K3s
#### We'll continue by integrating Kubernetes through K3s. Other methods like using minikube could have been used, but K3s proves to be a better option sice it provides lower RAM usage, lower CPU overhead, and fewer operational issues. 
- Stop and remove current running container
```
docker stop resumeiq-container
docker rm resumeiq-container
```
- Install K3s
```
curl -sfL https://get.k3s.io | sh -
```
K3s installs:
- Kubernetes API server
- scheduler
- kubelet
- container runtime
- networking
- kubectl  
  
Verify K3s service
```
sudo systemctl status k3s
```
Verify Kubernetes nodes
```
sudo kubectl get nodes
```
Purpose:
- verifies cluster node readiness
- confirms Kubernetes control plane functionality  

#### Step 2: Creating deployment.yml file
#### Kubernetes uses declarative infrastructure instead of manually running containers. The desired infrastructure state is defined through YAML manifests, particularly the deployment.yaml file. Kubernetes continuously ensures actual system state matches declared state.

- Create the deployment.yaml file 
```
apiVersion: apps/v1
kind: Deployment

metadata:
  name: resumeiq-deployment

spec:
  replicas: 1

  selector:
    matchLabels:
      app: resumeiq

  template:
    metadata:
      labels:
        app: resumeiq

    spec:
      containers:
      - name: resumeiq-container
        image: hsharma25/resumeiq:latest

        imagePullPolicy: Always

        ports:
        - containerPort: 8501
```
Explanation:
| Field           | Purpose                     |
| --------------- | --------------------------- |
| apiVersion      | Kubernetes API version      |
| kind            | Type of Kubernetes resource |
| metadata        | Resource identification     |
| replicas        | Desired pod count           |
| selector        | Pod matching labels         |
| template        | Pod definition              |
| image           | Docker image source         |
| imagePullPolicy | Always fetch latest image   |
| containerPort   | Exposed application port    |

#### Step 3: Kubernetes service
#### K8s service ensures consistent networking and load balancing. All required states are defined in the service.yaml file
- Create service.yaml file
```
apiVersion: v1
kind: Service

metadata:
  name: resumeiq-service

spec:
  type: NodePort

  selector:
    app: resumeiq

  ports:
    - port: 8501
      targetPort: 8501
      nodePort: 30007
```
Explanation:
| Field          | Purpose                  |
| -------------- | ------------------------ |
| kind: Service  | Creates networking layer |
| type: NodePort | Exposes app externally   |
| selector       | Maps service to pods     |
| port           | Service port             |
| targetPort     | Container port           |
| nodePort       | External EC2 port        |

#### Step 4: Deploy kubernetes resources
- Apply deployment
```
sudo kubectl apply -f k8s/deployment.yaml
```
- Apply service
```
sudo kubectl apply -f k8s/service.yaml
```
- Access the application using
```
http://<ELASTIC-IP>:30007
```

#### Step 5: Jenkins and Kubernetes integration
#### We'll enable Jenkins CI/CD pipeline to communicate with Kubernetes cluster, trigger rolling deployments, automate Kubernetes re-deployment process
- Firstly, Jenkins needs ability to execute kubectl commands
- For this, we need to update the Kubernetes configuration file
- The file is stored at ```/etc/rancher/k3s/k3s.yaml```
- Copy kubernetes congig for Jenkins
```
sudo cp /etc/rancher/k3s/k3s.yaml /var/lib/jenkins/kubeconfig
```
- Configure KUBECONFIG environment variable
- Open ```sudo systemctl edit jenkins```  

Add:
```
[Service]
Environment="KUBECONFIG=/var/lib/jenkins/kubeconfig"
```
- "KUBECONFIG"environment variable tells kubectl which Kubernetes configuration file to use
- Without this, Jenkins cannot communicate with Kubernetes cluster.
- Reload Jenkins service
```
sudo systemctl daemon-reload
sudo systemctl restart jenkins
```
- Confirm Jenkins-Kubernetes integration 
```
sudo su - jenkins
kubectl get nodes
```
- Confirms Jenkins user can access Kubernetes cluster  

**Important**: Update the old Jenkins pipeline:
```
pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t hsharma25/resumeiq:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push hsharma25/resumeiq:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl rollout restart deployment resumeiq-deployment'
            }
        }
    }
}
```
The line:
```
kubectl rollout restart deployment resumeiq-deployment
```
Triggers:
- old pod termination
- new pod creation
- deployment using latest Docker image

---

## Phase 5: Monitoring and Visualization with Prometheus and Grafana
### The objective of this phase is to implement a complete monitoring and observability stack for the ResumeIQ Kubernetes infrastructure using Prometheus, Grafana, Helm and Kubernetes monitoring exporters
#### Technologies used:
| Technology         | Purpose                    |
| ------------------ | -------------------------- |
| Prometheus         | Metrics collection         |
| Grafana            | Dashboard visualization    |
| Helm               | Kubernetes package manager |
| Node Exporter      | Node-level metrics         |
| kube-state-metrics | Kubernetes object metrics  |

#### Step 1: Install Helm
#### What is Helm?
Helm is a package manager for Kubernetes. It simplifies Kubernetes application deployment using Helm Charts. A Helm chart is a pre-configured Kubernetes application template.
```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
- Add Prometheus Helm repository. 
- Purpose: adds official Prometheus Helm chart repository
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
- Update Helm repositories
- Purpose: downloads latest Helm chart metadata
```
helm repo update
```

- Create monitoring namespace
- Purpose: isolates monitoring resources inside Kubernetes

What is a Kubernetes Namespace?  
Namespaces logically separate Kubernetes resources.
Examples:
- default
- kube-system
- monitoring

This improves organization and resource management.
```
sudo kubectl create namespace monitoring
```

#### Step 2: Install kube-prometheus-stack
- Purpose: installs complete monitoring stack

Components installed:
- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- kube-state-metrics
```
KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring
```

- Verify monitoring pods
- Checks monitoring stack deployment
```
sudo kubectl get pods -n monitoring
```

- Verify monitoring services
```
sudo kubectl get svc -n monitoring
```

#### Step 3: Expose Grafana using NodePort
#### Grafana is initially accessible only inside the Kubernetes cluster. To access Grafana externally, a NodePort service was created.
- Command:
```
sudo kubectl expose service monitoring-grafana \
  --type=NodePort \
  --target-port=3000 \
  --name=grafana-nodeport \
  -n monitoring
```

- Retrieve Grafana NodePort
- Grafana is accessible on this port
- Accordingly, add inbound rule to EC2 security group  
```
sudo kubectl get svc -n monitoring
```

#### Step 4: Access Grafana dashboard
- Type in browser
- Example:
```
http://<ELASTIC-IP>:30244
```

- Retrieve Grafana admin password

Grafana login credentials:  
| Field    | Value          |
| -------- | -------------- |
| Username | admin          |
| Password | command output |

```
sudo kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

---
