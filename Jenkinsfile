pipeline {
  agent any
  options { timeout(time: 15, unit: 'MINUTES') }
  stages {
    stage('Prepare') {
      steps { sh 'cp .env.example .env' }
    }
    stage('Validate') {
      steps { sh 'docker compose config --quiet' }
    }
    stage('Build') {
      steps { sh 'docker build --pull -t activate:${GIT_COMMIT} .' }
    }
  }
  post {
    always { sh 'rm -f .env' }
  }
}
