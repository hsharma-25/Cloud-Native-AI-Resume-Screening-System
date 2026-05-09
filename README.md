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
| Instance type | t3.small     |
| Stroage      | 50GB gp3     |
| OS           | Ubuntu       |
| Authentication | SSH key pair |  
  

Security group configuration:
| Port      | Purpose        |
|:-------------|:-------------|
| 22 | SSH     |
| 8080      | Jenkins     |
| 8501           | Streamlit|  
  

#### Step 2: Connecting to EC2 instance(SSH)
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