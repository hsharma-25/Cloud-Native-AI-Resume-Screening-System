## Phase 1: Docker
### Docker helps in containerizing an application which ensures that the application runs consistently across different environments such as local machines, cloud servers, CI/CD pipelines, and Kubernetes clusters.
### In this step we write the Dockerfile, .dockerignore file, build the image from the Dockerfile and run our container off of the built image

### Step 1: The Dockerfile and .dockerignore
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

### Step 2: Building the Docker image
- The Docker image is built using the following command
```bash
docker build -t resumeiq .
```
- "docker build" creates the image
- "-t resumeiq" assigns the image name
- "." specifies the current directory as build context

### Step 3: Running the Docker container
- The Docker container was started using
```bash
docker run -d -p 8501:8501 resumeiq
```
- The "-d" makes the container run indetached mode
- The "-p" field allows the application to be accessed on the specified port
- By default, Streamlit uses port no. "8501"

### Step 4: Accessing the application
- The application is now containerized
- The application can be accessed on localhost port 8501
```
http://localhost:8501
```

---


## Phase 2: EC2 Deployment
### The objective of this phase is to deploy our application onto an EC2 instance so that it can be run on the cloud
### Step 1: Creating and launching the EC2 instance
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
  

### Step 2: Connecting to EC2 instance(SSH)
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

### Step 3: Installing Docker and Containerization
### Docker helps us in containerizing an application. Containerization packages the application with its dependencies into isolated containers. This ensures that the application runs same everywhere and on evey device. 
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