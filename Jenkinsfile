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

        stage('Notify Lambda') {
            steps {
                sh '''
                curl -X POST https://YOUR-LAMBDA-URL
                '''
            }
        }
    }
}