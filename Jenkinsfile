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