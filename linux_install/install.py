import asyncio
import paramiko

async def ssh_connect(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    await asyncio.get_running_loop().run_in_executor(None, ssh.connect, hostname, username, password)
    return ssh

async def update_packages(ssh):
    stdin, stdout, stderr = await asyncio.get_running_loop().run_in_executor(None, ssh.exec_command, 'sudo apt-get update')
    print(stdout.read().decode())

async def install_package(ssh, package):
    stdin, stdout, stderr = await asyncio.get_running_loop().run_in_executor(None, ssh.exec_command, f'sudo apt-get install -y {package}')
    print(stdout.read().decode())

async def run_tasks_on_servers(servers, tasks):
    tasks_to_run = []
    for server in servers:
        async with ssh_connect(**server) as ssh:
            for task in tasks:
                tasks_to_run.append(asyncio.create_task(task(ssh)))
    await asyncio.gather(*tasks_to_run)

if __name__ == '__main__':
    servers = [
        {'hostname': 'remote-server1.com', 'username': 'user1', 'password': 'password1'},
        {'hostname': 'remote-server2.com', 'username': 'user2', 'password': 'password2'}
    ]
    tasks = [update_packages, lambda ssh: install_package(ssh, 'nginx'), lambda ssh: install_package(ssh, 'python3')]
    asyncio.run(run_tasks_on_servers(servers, tasks))

