pipeline {
//This agent is a global agent  ,like docker as an agent , but we can always use the agents specified for each stage
    agent none
    stages {
        //This is a build stage where we will build or execute the code that was taken from the git repository.
        stage('Build') {
            agent {
                docker {
                    //This image parameter in the docker agent uses the the python:2-alpine image form the docker hub
                    //if this is not present in your container it download form the docker hub
                    //Docker image and runs this image as a separate container. The Python container becomes
                    //the agent that Jenkins uses to run the Build stage of the pipeline
                    image 'python:2-alpine'
                }
            }
            steps {
                //This sh step runs the Python command to compile your application and
                //convert into byte code files, which are placed into the sources workspace directory
                sh 'python -m py_compile sources/calcy.py'
                //This step saves the Python source code and compiled byte code files from the sources workspace directory
                stash(name: 'results', includes: 'sources/*.py*')
            }
        }
        stage('Test') {
            agent {
                docker {
                    //This image parameter like the above downloads the qnib:pytest Docker image from docker hub and runs this image as a
                    //separate container. The pytest container becomes the agent that Jenkins uses to run the Test stage.
                    image 'qnib/pytest'
                }
            }
            steps {
                //This sh step executes pytest’s py.test command on test_calcy.py
                //The --junit-xml test-reports/results.xml option makes py.test generate a JUnit XML report,
                //which is saved to test-reports/results.xml
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calcy.py'
            }
            post {
                always {
                    //This junit step archives the JUnit XML report and exposes the results through the Jenkins interface.
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
                    agent any

                    environment {
                        VOLUME = '$(pwd)/sources:/src'
                        IMAGE = 'cdrx/pyinstaller-linux:python2'
                    }
                    steps {
                        //This dir step creates a new subdirectory named by the build number.
                        //The final program will be created in that directory by pyinstaller.
                        //BUILD_ID is one of the Jenkins environment variable.
                        //This unstash step restores the Python source code and compiled byte code files (with .pyc extension) from the previously saved stash. image]
                        //and runs this image as a separate container.
                        dir(path: env.BUILD_ID) {
                            unstash(name: 'results')

                            //This sh step executes the pyinstaller command (in the PyInstaller container) on your simple Python application.
                            //This makes our Python application into a single standalone executable file
                            sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F calcy.py'"
                        }
                    }
                    post {
                        success {
                            //This archiveArtifacts step archives the standalone executable file and exposes this file
                            //through the Jenkins interface.
                            archiveArtifacts "${env.BUILD_ID}/sources/dist/calcy"
                            sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                        }
                    }
        }
    }
}
