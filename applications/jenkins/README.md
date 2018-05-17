Pipeline:

node {
  def mvnHome stage('Preparation') {
    // for display purposes
    // Get some code from a GitHub repository
    git 'git://github.com/victorock/phillyapp.git'
    // Get the Maven tool.
    // ** NOTE: This 'M3' Maven tool must be configured
    // ** in the global configuration.
    mvnHome = tool 'test'
  }

  // The following variables need to be defined at the top level and not inside
  // the scope of a stage - otherwise they would not be accessible from other stages.
  // Extract version and other properties from the pom.xml
  def pom = readMavenPom file: 'pom.xml'
  def packageName = pom.name
  def version = pom.version
  def newVersion = "${version}-${BUILD_NUMBER}"
  def artifactId = pom.artifactId
  def groupId = pom.groupId

  stage ('Build') {
    sh 'mvn clean install -Dv=${newVersion}'
  }
  stage ('Deploy on Artifactory') {
    sh 'mvn deploy -Dv=${version}'
  }
  stage ('Deploy new app with Ansible Tower') {
    ansibleTower( towerServer: 'TowerDemo', jobTemplate: 'Demo Deploy PhillyApp', extraVars: "app_release: ${version}" )
  } 
