// Jenkinsfile – Declarative Pipeline
// Student Feedback Registration Form
// DevOps CA2 Project

pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PROJECT_DIR  = "${WORKSPACE}"
        REPORTS_DIR  = "${WORKSPACE}/test-results"
        PYTHON_CMD   = "python"       // Change to "python3" on Linux/Mac
        // Source folder on this machine (used when no Git SCM is configured)
        SOURCE_DIR   = "C:\\Users\\Jeevan\\Downloads\\Devops-CA2"
    }

    stages {

        // ── Stage 1: Checkout ──────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '========== Stage 1: Checkout =========='

                // OPTION A – Git SCM (uncomment when GitHub is configured):
                // git url: 'https://github.com/<your-username>/Devops-CA2.git', branch: 'main'

                // OPTION B – Copy from local project folder (no Git needed)
                // This copies all files from your project directory into the Jenkins workspace
                bat """
                    echo Copying project files from ${SOURCE_DIR} ...
                    xcopy /E /Y /I "${SOURCE_DIR}\\*" "%WORKSPACE%\\"
                    echo Done.
                """

                echo "Working directory: ${PROJECT_DIR}"
                bat 'dir'
            }
        }

        // ── Stage 2: Setup Python Environment ─────────────────────────────
        stage('Setup Python Environment') {
            steps {
                echo '========== Stage 2: Setup Python Environment =========='
                // Use 'python -m pip' to avoid Windows permission issues with bare 'pip'
                bat "${PYTHON_CMD} -m pip install --upgrade pip"
                bat "${PYTHON_CMD} -m pip install -r requirements.txt"
                bat "${PYTHON_CMD} --version"
                bat "${PYTHON_CMD} -m pip show selenium pytest webdriver-manager"
            }
        }

        // ── Stage 3: Validate HTML (optional static check) ────────────────
        stage('Validate Source Files') {
            steps {
                echo '========== Stage 3: Validate Source Files =========='
                bat "if exist index.html (echo index.html found) else (exit 1)"
                bat "if exist style.css (echo style.css found) else (exit 1)"
                bat "if exist script.js (echo script.js found) else (exit 1)"
                bat "if exist tests\\test_form.py (echo test_form.py found) else (exit 1)"
                echo 'All required source files present.'
            }
        }

        // ── Stage 4: Run Selenium Tests ────────────────────────────────────
        stage('Run Selenium Tests') {
            steps {
                echo '========== Stage 4: Run Selenium Tests =========='
                // Create reports directory
                bat "if not exist test-results mkdir test-results"

                // Run pytest: verbose output + JUnit XML report
                bat """
                    ${PYTHON_CMD} -m pytest tests/ ^
                        --tb=short ^
                        -v ^
                        --junit-xml=${REPORTS_DIR}/test-results.xml ^
                        --no-header
                """
            }
        }

        // ── Stage 5: Publish Test Results ─────────────────────────────────
        stage('Publish Test Results') {
            steps {
                echo '========== Stage 5: Publish Test Results =========='
            }
            post {
                always {
                    // Publish JUnit-style test results in Jenkins UI
                    junit allowEmptyResults: true,
                          testResults: 'test-results/test-results.xml'
                    echo 'Test results published to Jenkins dashboard.'
                }
            }
        }

    }

    // ── Post-build Actions ─────────────────────────────────────────────────
    post {
        success {
            echo '✅ BUILD SUCCESS: All Selenium tests passed!'
        }
        failure {
            echo '❌ BUILD FAILED: One or more Selenium tests failed. Check Console Output.'
        }
        always {
            echo "Build completed. Result: ${currentBuild.currentResult}"
            echo "Duration: ${currentBuild.durationString}"
        }
    }
}
