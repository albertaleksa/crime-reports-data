# CrimeTrendsExplorer: A Multi-City Crime Analysis Project
Final Project for Data Engineering Zoomcamp Course

## Table of contents

- [Problem Description](#problem-description)
- [Dataset](#dataset)
- [Technologies & Tools](#technologies--tools)
- [Data Pipeline Architecture diagram](#data-pipeline-architecture-diagram)
- [Pipeline explanation](#pipeline-explanation)
- [Dashboard & Results](#dashboard--results)
- [How to reproduce](#how-to-reproduce)
  - [Step 1. Set Up Cloud Environment](#step-1-set-up-cloud-environment)
  - [Step 2.]()
- [Future Improvements](#future-improvements)
- [Credits](#credits)

---

## Problem Description


_[Back to the top](#table-of-contents)_

## Dataset


_[Back to the top](#table-of-contents)_

## Technologies & Tools


_[Back to the top](#table-of-contents)_

## Data Pipeline Architecture diagram


_[Back to the top](#table-of-contents)_

## Pipeline explanation


_[Back to the top](#table-of-contents)_

## Dashboard & Results


_[Back to the top](#table-of-contents)_

## How to reproduce

### Step 1. Set Up Cloud Environment. Using Google Console and local terminal
1. Create an **account** on **Google's Cloud platform** with your Google email ID (if you don't have one).
2. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a **new project**.
Copy Project ID (in my case it was: `crime-trends-explorer`) and press `Create`.

    ![create_project](/images/01_create_project.png)

    Then choose to use your new project:
![change_project](/images/01_change_project.png)
3. Create **Service Account** for this project:
   * Go to `IAM & Admin` -> `Service accounts` -> `Create Service Account`
   * Name: **crime-trends-explorer-user**
   * Grant those roles to this account:
     * `Viewer`
     * `BigQuery Admin`
     * `Storage Admin`
     * `Storage Object Admin`
     * `Dataproc Administrator`
     * `Service Account User`
   * After pressing `Done` click Actions on created account and choose `Manage keys`:
     * `Add key` -> `Create new key` -> `JSON` -> `Create`
     * Create New Key for this account (json)
   * Download created service-account-key, rename it to `crime-trends-explorer-user-key.json` and put it in `~/.gc` dir (create folder if needed). It's for convenient. Then we'll put it into our VM.
4. Enable these **APIs** for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   * Compute Engine API (You'll find it when choose `Compute Engine` menu)
   * Cloud Dataproc API
5. Generate **SSH keys** to login to VM instances. This will generate a 2048 bit rsa ssh keypair, named `gcp` and a comment of `de_user`. The comment (`de_user`) will be the user on VM :
   * In terminal:
   ```
   cd ~/.ssh
   ssh-keygen -t rsa -f ~/.ssh/gcp -C de_user -b 2048
   ```
   * Put generated public key to google cloud:
    (`Compute Engine` -> `Metadata` -> `SSH Keys` -> `Add ssh key`) and copy all from file `gcp.pub`. If you already have SSH key to work with your gcp, you can use it.

6. Create **Virtual Machine** Instance (`Compute Engine` -> `VM Instances` -> `Create Instance`).
    ```
    Name: whatever name you would like to call this VM (crime-vm)
    Region, Zone: select a region near you, same with Zone (us-east1-b)
    Machine type: Standard, 4vCPu, 16 GB Memory (e2-standard-4)
    Operating system: Ubuntu
    Version: Ubuntu 20.04 LTS
    Boot disk size: 20Gb.
    ```
    ![vm_name](/images/01_vm_name.png)
    ![vm_disk](/images/01_vm_disk.png)

    When VM is created, note the external IP address.

7. Connect to created VM from terminal (Copy an external ip of created VM): 
    ```
    ssh -i ~/.ssh/gcp de_user@<external_ip_you_copied>
    ```
   You can also update or create a **config file** in your ~/.ssh folder, inputing the external IP address of your VM. This will allow you to just do `ssh crime-vm` to login to your VM
   ```
   $ cd ~/.ssh/
   # Create config file (or open if exists)
   $ touch config
   ```
   Add:
   ```
   Host crime-vm
    Hostname <external_ip_you_copied>
    User de_user
    IdentityFile ~/.ssh/gcp
   ```
   Then you can run `ssh crime-vm` to connect to this VM.

### Step 2. Set Up Cloud Environment. Using VM Terminal
1. **Connect** to remote VM:
   ```
   ssh crime-vm
   ```
2. In VM **clone** repository and `cd` into it:
    ```
    git clone https://github.com/albertaleksa/crime-reports-data.git
    cd crime-reports-data
    ```
3. Run bash script to install software in VM:
    ```
    bash ./setup/setup.sh
    ```
   This will :
   * **update** system
   * download and install **Anaconda**. 
   * install **Docker**
   * Give permission to run **docker** commands **without sudo** in VM
   * Install docker-compose
   * Install Terraform

4. **IMPORTANT**: Log out and log back in so that your group membership is re-evaluated.

5. **Check** if **docker** works:
    ```
    docker run hello-world
    ```
    Check docker-compose version:
    ```
    docker-compose version
    ```
6. **(From local terminal)** Copy service-account-key `crime-trends-explorer-user-key.json` from `~/.gc` to our VM. It'll make possible to work with our Google Cloud from VM using this service account: 
    ```
    scp ~/.gc/crime-trends-explorer-user-key.json de_user@crime-vm:~/.gc/
    ```
7. **(In Remote VM)** Configure gcloud with your service account .json file:
   - If needed change **<path-to-your-key-file>** in file `setup/activate_service_account.sh` to your value
   - Run command:
       ```
      bash ./setup/activate_service_account.sh
      ```
   - Log out and log back

### Step 3. Run Terraform to deploy your infrastructure to your Google Cloud Project **(In Remote VM)**

0) If needed you can change variables in `terraform.tfvars` (change region,..)

1) Initialize terraform:
    ```
    terraform -chdir="./terraform" init
    ```
2) Build a deployment plan (change `crime-trends-explorer` to your `project_id` if needed):
    ```
    terraform -chdir="./terraform" plan -var="project_id=crime-trends-explorer"
    ```
3) Apply the deployment plan and deploy the infrastructure (change `crime-trends-explorer` to your `project_id` if needed). If needed type `yes` to accept actions:
    ```
    terraform -chdir="./terraform" apply -var="project_id=crime-trends-explorer"
    ```
4) Go to Google Cloud Console to make sure that infrastructure is created:
    - Google Cloud Storage:
   ![03_bucket.png](/images/03_bucket.png)
    - BigQuery
   ![03_bigquery.png](/images/03_bigquery.png)
    - DataProc
   ![03_dataproc.png](/images/03_dataproc.png)



_[Back to the top](#table-of-contents)_

## Future Improvements


_[Back to the top](#table-of-contents)_

## Credits


_[Back to the top](#table-of-contents)_