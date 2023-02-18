# Multitask
Multitask is a Python script that allows you to run various maintenance tasks on multiple remote servers concurrently using asyncio and paramiko.

### Installation
To use Multitask, you'll need to have Python 3.7 or higher installed on your system. You can download Python from the official website: https://www.python.org/downloads/

To install the dependencies for Multitask, run the following command:

``` 
pip install -r requirements.txt
```

### Usage
Multitask provides several functions for running maintenance tasks on remote servers:

- ssh_connect(hostname, username, password): Connects to an SSH server with the given hostname, username, and password, and returns a paramiko.SSHClient object.
- update_packages(ssh): Updates the packages on the remote server by running the apt-get update and apt-get upgrade commands.
- install_package(ssh, package_name): Installs the specified package on the remote server using the package manager.
- run_tasks_on_servers(servers, tasks): Runs the specified tasks on each of the given servers concurrently.

###### To use these functions, you can create a Python script that imports them and calls them as needed. For example:
```
import asyncio
from multitask import ssh_connect, update_packages, install_package, run_tasks_on_servers

async def main():
    # Connect to the remote servers
    server1 = await ssh_connect('example.com', 'user1', 'password1')
    server2 = await ssh_connect('example.org', 'user2', 'password2')

    # Define the tasks to run on the remote servers
    tasks = [
        lambda ssh: update_packages(ssh),
        lambda ssh: install_package(ssh, 'nginx'),
        lambda ssh: install_package(ssh, 'python3'),
    ]

    # Run the tasks on the remote servers
    servers = [server1, server2]
    await run_tasks_on_servers(servers, tasks)

    # Close the SSH connections
    server1.close()
    server2.close()

asyncio.run(main())
```

This script connects to two remote servers, updates the packages, and installs the nginx and python3 packages on both servers concurrently using the run_tasks_on_servers function.

### Testing
Multitask comes with a test suite that can be run using the unittest module. To run the tests, simply execute the following command in your terminal:

```
python -m unittest discover tests
```

This will run all of the test cases in the tests directory and output the results.

### License
Multitask is released under the MIT License. See the LICENSE file for more details.

### Contributing
If you'd like to contribute to Multitask, please fork the repository and submit a pull request. We welcome bug fixes, feature requests, and other contributions.
