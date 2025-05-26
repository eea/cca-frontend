pipeline {
  environment {
    RANCHER_STACKID = ""
    RANCHER_ENVID = ""
    GIT_NAME = "cca-frontend"
    registry = "eeacms/cca-frontend"
    template = "templates/volto-cca"
    dockerImage = ''
    tagName = ''
    SONARQUBE_TAG = 'climate-adapt.eea.europa.eu'
    SONARQUBE_TAG_DEMO = ''
  }

  agent any

  stages {

  //   stage('Integration tests') {
  //     parallel {
  //      stage('Cypress') {
  //        when {
  //          allOf {
  //            environment name: 'CHANGE_ID', value: ''
  //            not { branch 'master' }
  //            not { changelog '.*^Automated release [0-9\\.]+$' }
  //            not { buildingTag() }
  //          }
  //        }
  //        steps {
  //          node(label: 'docker') {
  //            script {
  //              try {
  //                sh '''docker pull eeacms/plone-backend; docker run --rm -d --name="$BUILD_TAG-plone" -e SITE="Plone" -e PROFILES="eea.kitkat:testing" eeacms/plone-backend'''
  //                sh '''docker pull eeacms/volto-project-ci; docker run -i --name="$BUILD_TAG-cypress" --link $BUILD_TAG-plone:plone -e GIT_NAME=$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e DEPENDENCIES="$DEPENDENCIES" eeacms/volto-project-ci'''

  //                } finally {
  //                try {
  //                  sh '''rm -rf cypress-reports cypress-results'''
  //                  sh '''mkdir -p cypress-reports cypress-results'''
  //                  sh '''docker cp $BUILD_TAG-cypress:/opt/frontend/my-volto-project/cypress/videos cypress-reports/'''
  //                  sh '''docker cp $BUILD_TAG-cypress:/opt/frontend/my-volto-project/cypress/reports cypress-results/'''
  //                  coverage = sh script: '''docker cp $BUILD_TAG-cypress:/opt/frontend/my-volto-project/coverage cypress-coverage/''', returnStatus: true
  //                  if ( coverage == 0 ) {
  //                       publishHTML (target : [allowMissing: false,
  //                           alwaysLinkToLastBuild: true,
  //                           keepAll: true,
  //                           reportDir: 'cypress-coverage/coverage/lcov-report',
  //                           reportFiles: 'index.html',
  //                           reportName: 'CypressCoverage',
  //                           reportTitles: 'Integration Tests Code Coverage'])
  //                  }
  //
  //                  sh '''touch empty_file; for ok_test in $(grep -E 'file=.*failures="0"' $(grep 'testsuites .*failures="0"' $(find cypress-results -name *.xml) empty_file | awk -F: '{print $1}') empty_file | sed 's/.* file="\\(.*\\)" time.*/\\1/' | sed 's#^cypress/integration/##g' | sed 's#^../../../node_modules/@eeacms/##g'); do rm -f cypress-reports/videos/$ok_test.mp4; rm -f cypress-reports/$ok_test.mp4; done'''
  //                  archiveArtifacts artifacts: 'cypress-reports/**/*.mp4', fingerprint: true, allowEmptyArchive: true
  //                }
  //                finally {
  //                  catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
  //                      junit testResults: 'cypress-results/**/*.xml', allowEmptyResults: true
  //                  }
  //                  sh script: "docker stop $BUILD_TAG-plone", returnStatus: true
  //                  sh script: "docker rm -v $BUILD_TAG-plone", returnStatus: true
  //                  sh script: "docker rm -v $BUILD_TAG-cypress", returnStatus: true
  //                }
  //              }
  //            }
  //          }
  //        }
  //      }


  //      stage("Docker test build") {
  //        when {
  //          allOf {
  //            not { changelog '.*^Automated release [0-9\\.]+$' }
  //            not { environment name: 'CHANGE_ID', value: '' }
  //            environment name: 'CHANGE_TARGET', value: 'master'
  //          }
  //        }
  //        environment {
  //          IMAGE_NAME = BUILD_TAG.toLowerCase()
  //        }
  //        steps {
  //          node(label: 'docker-host') {
  //            script {
  //              checkout scm
  //              try {
  //                dockerImage = docker.build("${IMAGE_NAME}", "--no-cache .")
  //              } finally {
  //                sh script: "docker rmi ${IMAGE_NAME}", returnStatus: true
  //              }
  //            }
  //          }
  //        }
  //      }
  //    }
  //  }


    stage('Bundlewatch') {
      when {
        branch 'develop'
      }
      steps {
        node(label: 'docker-big-jobs') {
          script {
            checkout scm
            env.NODEJS_HOME = "${tool 'NodeJS'}"
            env.PATH="${env.NODEJS_HOME}/bin:${env.PATH}"
            env.CI=false
            sh "yarn"
            sh "make develop"
            sh "make install"
            sh "make build"
            //sh "make bundlewatch"
          }
        }
      }
    }

    stage('Pull Request') {
      when {
        allOf {
            not { environment name: 'CHANGE_ID', value: '' }
            environment name: 'CHANGE_TARGET', value: 'master'
            not { changelog '.*^Automated release [0-9\\.]+$' }
        }
      }
      steps {
        node(label: 'docker') {
          script {
            if ( env.CHANGE_BRANCH != "develop" &&  !( env.CHANGE_BRANCH.startsWith("hotfix")) ) {
                error "Pipeline aborted due to PR not made from develop or hotfix branch"
            }
           withCredentials([string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN')]) {
            sh '''docker pull eeacms/gitflow'''
            sh '''docker run -i --rm --name="$BUILD_TAG-gitflow-pr" -e GIT_CHANGE_TARGET="$CHANGE_TARGET" -e GIT_CHANGE_BRANCH="$CHANGE_BRANCH" -e GIT_CHANGE_AUTHOR="$CHANGE_AUTHOR" -e GIT_CHANGE_TITLE="$CHANGE_TITLE" -e GIT_TOKEN="$GITHUB_TOKEN" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e GIT_ORG="$GIT_ORG" -e GIT_NAME="$GIT_NAME" -e LANGUAGE=javascript eeacms/gitflow'''
           }
          }
        }
      }
    }


    stage('Release') {
      when {
        allOf {
          environment name: 'CHANGE_ID', value: ''
          branch 'master'
        }
      }
      steps {
        node(label: 'docker') {
          withCredentials([string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN')]) {
            sh '''docker pull eeacms/gitflow'''
            sh '''docker run -i --rm --name="$BUILD_TAG-gitflow-master" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_NAME="$GIT_NAME" -e GIT_TOKEN="$GITHUB_TOKEN" -e LANGUAGE=javascript eeacms/gitflow'''
          }
        }
      }
    }

    stage('Build & Push ( on tag )') {
      when {
        buildingTag()
      }
      steps{
        node(label: 'docker-host') {
          script {
            checkout scm
            if (env.BRANCH_NAME == 'master') {
              tagName = 'latest'
            } else {
              tagName = "$BRANCH_NAME"
            }
            try {
              dockerImage = docker.build("$registry:$tagName", "--no-cache .")
              docker.withRegistry( '', 'eeajenkins' ) {
                dockerImage.push()
              }
            } finally {
              sh "docker rmi $registry:$tagName"
            }
          }
        }
      }
    }

    stage('Release catalog ( on tag )') {
      when {
        buildingTag()
      }
      steps{
        node(label: 'docker') {
          withCredentials([string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN'),  usernamePassword(credentialsId: 'jekinsdockerhub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
            sh '''docker pull eeacms/gitflow; docker run -i --rm --name="$BUILD_TAG-release"  -e GIT_BRANCH="$BRANCH_NAME" -e GIT_NAME="$GIT_NAME" -e DOCKERHUB_REPO="$registry" -e GIT_TOKEN="$GITHUB_TOKEN" -e DOCKERHUB_USER="$DOCKERHUB_USER" -e DOCKERHUB_PASS="$DOCKERHUB_PASS"  -e DEPENDENT_DOCKERFILE_URL="$DEPENDENT_DOCKERFILE_URL" -e RANCHER_CATALOG_PATHS="$template" -e GITFLOW_BEHAVIOR="RUN_ON_TAG" eeacms/gitflow'''
         }
        }
      }
    }

    stage('Upgrade demo ( on tag )') {
      when {
        buildingTag()
      }
      steps {
        node(label: 'docker') {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'Rancher_dev_token', usernameVariable: 'RANCHER_ACCESS', passwordVariable: 'RANCHER_SECRET'],string(credentialsId: 'Rancher_dev_url', variable: 'RANCHER_URL')]) {
            sh '''wget -O rancher_upgrade.sh https://raw.githubusercontent.com/eea/eea.docker.gitflow/master/src/rancher_upgrade.sh'''
            sh '''chmod 755 rancher_upgrade.sh'''
            sh '''./rancher_upgrade.sh'''
         }
        }
      }
    }

    stage('Update SonarQube Tags') {
      when {
        not {
          environment name: 'SONARQUBE_TAG', value: ''
        }
        buildingTag()
      }
      steps{
        node(label: 'docker') {
          withSonarQubeEnv('Sonarqube') {
            withCredentials([string(credentialsId: 'eea-jenkins-token', variable: 'GIT_TOKEN')]) {
              sh '''docker pull eeacms/gitflow'''
              sh '''docker run -i --rm --name="${BUILD_TAG}-sonar" -e GIT_NAME=${GIT_NAME} -e GIT_TOKEN="${GIT_TOKEN}" -e SONARQUBE_TAG=${SONARQUBE_TAG} -e SONARQUBE_TOKEN=${SONAR_AUTH_TOKEN} -e SONAR_HOST_URL=${SONAR_HOST_URL}  eeacms/gitflow /update_sonarqube_tags.sh'''
            }
          }
        }
      }
    }
  }

  post {
    changed {
      script {
        def url = "${env.BUILD_URL}/display/redirect"
        def status = currentBuild.currentResult
        def subject = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
        def details = """<h1>${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${status}</h1>
                         <p>Check console output at <a href="${url}">${env.JOB_BASE_NAME} - #${env.BUILD_NUMBER}</a></p>
                      """
        emailext (subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS', body: details)
      }
    }
  }
}
