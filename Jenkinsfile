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
                sh 'kubectl apply -f k8s/deployment.yaml'
            }
        }

        // stage('Notify Lambda') {
        //     steps {
        //         sh '''
        //         curl -X POST https://gbdbxdzd33ljat4gd4cu34mohq0evozu.lambda-url.us-east-1.on.aws/
        //         '''
        //     }
        // }
    }
}