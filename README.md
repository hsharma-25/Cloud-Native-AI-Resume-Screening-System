## Phase 1: Docker
### Docker helps in containerizing an application which ensures that the application runs consistently across different environments such as local machines, cloud servers, CI/CD pipelines, and Kubernetes clusters.
### In this step we write the Dockerfile, .dockerignore file, build the image from the Dockerfile and run our container off of the built image

### Step 1: The Dockerfile and .dockerignore
- Before building the image we need to define all the instructions Docker would follow while building the image. 
- These instructions are defined in the Dockerfile. A Docker file executes instructions, copies various files etc.. 
- To ensure no unnecessary files are copied a .dockerignore file is created  
Example:
```gitignore
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

RUN pip install --no-cache-dir -r requirements.txt

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


## Phase 2: EC2 Deployment + Jenkins CI/CD
