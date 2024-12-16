<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml)</a>
  
</div>

<div style="text-align: center;">
  <img src="https://www.veggiegib.com/wp-content/uploads/2016/12/IMG_20161129_192533-768x768.jpg" alt="Logo">
</div>

# uvlhub.io

Repository based on uvlhub, which is, in turn, a repository of feature models in UVL format integrated with Zenodo and flamapy following Open Science principles - Developed by DiversoLab
This repository is developed by Potaje-hub, a team formed by six students of Software Engineering on Universidad de Sevilla. 
This is a project for EGC subject.

This repository contains the UVLHUB web application. Follow the steps below to set up and run the application locally.

## Prerequisites

Before running the application, ensure that you have the following installed:

- [Python 3.12+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/)
- [Flask](https://flask.palletsprojects.com/)
- [pip](https://pip.pypa.io/en/stable/)

## Setting up the environment

1. Clone the repository:

   ```bash
   git clone https://github.com/potaje-hub/potaje-hub.git
   
   cd potaje-hub
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv

   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy the `.env` file from the provided example:

   ```bash
   rm .env # If you already have an .env file.
   cp .env.local.example .env
   ```

   Note: The `.env` file contains sensitive information like database credentials and API keys. Make sure to update it with the appropriate values if necessary.

5. Configure the database:

   - Install & configure MariaDB:
      ```sudo apt install mariadb-server -y
      sudo systemctl start mariadb
      sudo mysql_secure_installation
      ```

   - Log in to MySQL:
     ```bash
     mysql -u root -p
     ```

   - Create a new database:
     ```sql
     CREATE DATABASE uvlhub;
     ```

   - Create a user and grant privileges:
     ```sql
     CREATE USER 'uvlhub_user'@'localhost' IDENTIFIED BY 'uvlhub_password';
     GRANT ALL PRIVILEGES ON uvlhub.* TO 'uvlhub_user'@'localhost';
     FLUSH PRIVILEGES;
     ```

   - Verify the user and database:
     ```sql
     SHOW DATABASES;
     SHOW GRANTS FOR 'uvlhub_user'@'localhost';
     ```

6. Configure database connection in `.env` file:

   Open the `.env` file and set the following variables:
   ```env
   MARIADB_HOSTNAME=127.0.0.1
   MARIADB_PORT=3306
   MARIADB_DATABASE=uvlhub
   MARIADB_USER=uvlhub_user
   MARIADB_PASSWORD=uvlhub_password
   ```

7. Apply database migrations:

   ```bash
   flask db upgrade
   ```

8. Seed the database with initial data:

   ```bash
   rosemary db:seed
   ```

## Running the application

Once the environment is set up, run the application using the following command:

   ```bash
   flask run --host=0.0.0.0
   ```

This will start the web server, and you can access the application in your browser at `http://localhost:5000`.

## Running Tests

To run the tests, execute the following command:

   ```bash
   pytest
   ```

This will run all the tests in the `app/modules/` directory.

Make sure that the necessary services (like MySQL) are running and accessible before running the tests.

## Installation with Vagrant

Follow these steps to set up the application using Vagrant:

1. **Install Vagrant**:
   Ensure you have Vagrant installed. You can download it from [here](https://www.vagrantup.com/downloads).

2. **Install Ansible & VIrtualBox**
   ```bash
   sudo apt install ansible virtualbox
   ```
   
3. **Copy the .env file**:
   ```bash
   rm .env # If you already have an .env file.
   cp .env.vagrant.example .env
   ```
   
4. **Change to Vagrant directory**:
   ```bash
   cd vagrant
   ```

5. **Start the Vagrant machine**:
   ```bash
   vagrant up
   ```
   This command will download the necessary box, set up the virtual machine, and provision it with all the required dependencies.

   If some error occurs during the provision, you should use the command `vagrant up --provision`

6. **Access the Vagrant machine**:
   ```bash
   vagrant ssh
   ```

7. **Run the application**:
   ```bash
   flask run --host=0.0.0.0
   ```
   The application will be accessible at `http://localhost:5000` on your host machine.

9. **Run tests**:
   ```bash
   pytest app/modules/ --ignore-glob='*selenium*'
   ```

10. **Stop the Vagrant machine**:
    
    When you're done, you can stop the Vagrant machine with:
   
    ```bash
    vagrant halt
    ```
   
11. **Destroy the Vagrant machine**:

    If you want to destroy the Vagrant machine, use:
    ```bash
    vagrant destroy
    ```

12. **(Optional) Restore the local configuration**:

    Ensure you are in the root directory.
    ```bash
    rm -rf venv
    deactivate
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    pip install -r requirements.txt
    rm .env # If you already have an .env file.
    cp .env.local.example .env
    ```

## Official documentation

You can consult the official documentation of the project at [docs.uvlhub.io](https://docs.uvlhub.io/)
