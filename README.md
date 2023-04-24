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
  - [Step 2.](#step-2)
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

### Step 1. Set Up Cloud Environment
1. Create an **account** on **Google's Cloud platform** with your Google email ID (if you don't have one).
2. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a **new project**. Copy Project ID (in my case it was: `crime-trends-explorer`) and press `Create`.

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
   * After pressing `Done` click Actions on created account and choose `Manage keys`:
     * `Add key` -> `Create new key` -> `JSON` -> `Create`
     * Create New Key for this account (json)
   * Download created service-account-key, rename it to `crime-trends-explorer-user-key.json` and put it in `~/.gc` dir (create folder if needed). It's for convenient.
4. Enable these **APIs** for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   * Compute Engine API (You'll find it when choose `Compute Engine` menu)
5. Generate **SSH keys** to login to VM instances. This will generate a 2048 bit rsa ssh keypair, named `gcp` and a comment of `de_user`. The comment (`de_user`) will be the user on VM :
   * In terminal:
   ```
   cd ~/.ssh
   ssh-keygen -t rsa -f ~/.ssh/gcp -C de_user -b 2048
   ```
   * Put generated public key to google cloud:
    (`Compute Engine` -> `Metadata` -> `SSH Keys` -> `Add ssh key`) and copy all from file `gcp.pub`. If you already have SSH key to work with your gcp, you can use it.

6. Create ***Virtual Machine** Instance (`Compute Engine` -> `VM Instances` -> `Create Instance`).
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

    Whe VM is created, note the external IP address.

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


### Step 2. Setup on VM Terminal
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

    During installation you should type `yes` or press `Enter` several times. For the Anaconda setup you should press `f` for more prompt.



### Step 3.


_[Back to the top](#table-of-contents)_

## Future Improvements


_[Back to the top](#table-of-contents)_

## Credits


_[Back to the top](#table-of-contents)_