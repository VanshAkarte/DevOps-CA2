# Jenkins Setup Guide
## Student Feedback Form – DevOps CA2 Project

This guide walks you through installing Jenkins and running the Selenium test suite automatically via a Jenkins pipeline.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Java (JDK) | 17 or 21 | Required by Jenkins |
| Python | 3.8+ | For running Selenium tests |
| Google Chrome | Latest | For Selenium WebDriver |
| Git | Any | Optional – for SCM integration |

---

## Step 1 – Install Java

1. Download **Java 21 JDK** from: https://adoptium.net/
2. Run the installer and follow the wizard.
3. Verify installation:
   ```powershell
   java -version
   ```
   Expected output: `openjdk version "21..."`

---

## Step 2 – Install Jenkins

1. Download Jenkins LTS (Windows installer) from: https://www.jenkins.io/download/
2. Run `jenkins.msi` → follow the installer wizard.
3. Jenkins will install as a **Windows Service** and start automatically.
4. Open your browser and navigate to: **http://localhost:8080**

### Unlock Jenkins
- Copy the initial admin password from:
  ```
  C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword
  ```
- Paste it into the **Unlock Jenkins** screen.

### Install Suggested Plugins
- Click **"Install suggested plugins"** – wait for installation to complete.

### Create Admin User
- Fill in username, password, full name, and email → Click **Save and Continue**.
- Click **Save and Finish** → **Start using Jenkins**.

---

## Step 3 – Install Required Jenkins Plugins

In Jenkins → **Manage Jenkins** → **Plugins** → **Available Plugins**, search for and install:

| Plugin | Purpose |
|--------|---------|
| **Pipeline** | Enables `Jenkinsfile` declarative pipelines |
| **Git** | Connects to Git repositories |
| **JUnit** | Publishes pytest XML test results |
| **HTML Publisher** | (Optional) Publishes HTML reports |

Click **Install** then **Restart Jenkins** when done.

---

## Step 4 – Configure Python & Chrome on Jenkins Agent

1. Make sure `python` and `pip` are available in your system PATH.
   ```powershell
   python --version
   pip --version
   ```
2. Ensure Google Chrome is installed (needed for headless Selenium).
3. No manual ChromeDriver installation is needed – **webdriver-manager** handles it automatically.

---

## Step 5 – Create a Jenkins Pipeline Job

1. On the Jenkins dashboard, click **"New Item"**.
2. Enter job name: `Student-Feedback-Form-Tests`
3. Select **"Pipeline"** → Click **OK**.

### Option A – Local Folder (No Git)

In the Pipeline section, set **Definition** to **"Pipeline script"** and paste the entire contents of `Jenkinsfile` directly.

### Option B – GitHub Repository (Recommended)

1. Push your project to GitHub:
   ```powershell
   cd "c:\Users\Jeevan\Downloads\Devops-CA2"
   git init
   git add .
   git commit -m "Initial commit – CA2 Student Feedback Form"
   git remote add origin https://github.com/<your-username>/Devops-CA2.git
   git push -u origin main
   ```

2. In the Jenkins job configuration:
   - **Definition**: `Pipeline script from SCM`
   - **SCM**: Git
   - **Repository URL**: `https://github.com/<your-username>/Devops-CA2.git`
   - **Branch Specifier**: `*/main`
   - **Script Path**: `Jenkinsfile`

3. Click **Save**.

---

## Step 6 – Run the Jenkins Job

1. On the job page, click **"Build Now"** (left sidebar).
2. A build entry will appear under **Build History** (e.g., `#1`).
3. Click the build number → **Console Output** to watch live logs.

### Expected Console Output (Success)

```
========== Stage 1: Checkout ==========
========== Stage 2: Setup Python Environment ==========
Successfully installed selenium pytest webdriver-manager
========== Stage 3: Validate Source Files ==========
index.html found
style.css found
script.js found
test_form.py found
========== Stage 4: Run Selenium Tests ==========
tests/test_form.py::TestTC1_PageLoads::test_page_title_contains_student_feedback PASSED
tests/test_form.py::TestTC1_PageLoads::test_form_element_present PASSED
...
tests/test_form.py::TestTC7_Buttons::test_submit_with_valid_data_shows_no_errors PASSED

===== 30 passed in XX.XXs =====
✅ BUILD SUCCESS: All Selenium tests passed!
```

---

## Step 7 – View Test Results

After a successful build:
1. Click the build number in **Build History**.
2. Click **"Test Result"** to see the JUnit test report.
3. Expand individual test classes and cases to see pass/fail details.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `java.io.IOException: Cannot run program "python"` | Add Python to system PATH; or set full path in Jenkinsfile `PYTHON_CMD` env var |
| `SessionNotCreatedException: ChromeDriver version mismatch` | Run `pip install --upgrade webdriver-manager` |
| `FileNotFoundError: index.html` | Ensure `WORKSPACE` in Jenkins matches project folder |
| Build stays in queue | Jenkins node may be offline — check **Manage Nodes** |

---

## Quick Reference Commands

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Run tests locally (before pushing to Jenkins)
pytest tests/ -v

# Run tests with JUnit XML output
pytest tests/ -v --junit-xml=test-results/test-results.xml
```

---

*DevOps CA2 – Student Feedback Registration Form | March 2026*
