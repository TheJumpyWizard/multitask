import unittest
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor, Future
from io import StringIO
import sys

import asyncio
from paramiko import SSHClient

from linux_install.install import ssh_connect, update_packages, install_package, run_tasks_on_servers


class TestAsyncScript(unittest.IsolatedAsyncioTestCase):

    async def test_ssh_connect(self):
        with patch.object(SSHClient, 'connect', return_value=None) as mock_connect:
            ssh = await ssh_connect('test.com', 'user', 'password')
            self.assertIsInstance(ssh, SSHClient)
            mock_connect.assert_called_once_with('test.com', 'user', 'password')

    async def test_update_packages(self):
        mock_ssh = MagicMock(spec=SSHClient)
        mock_stdout = MagicMock()
        mock_stdout.read.return_value.decode.return_value = 'Packages updated successfully'
        mock_ssh.exec_command.return_value = (None, mock_stdout, None)
        expected_output = 'Packages updated successfully\n'
        with patch('sys.stdout', new=StringIO()) as fake_output:
            await update_packages(mock_ssh)
            self.assertEqual(fake_output.getvalue(), expected_output)

    async def test_install_package(self):
        mock_ssh = MagicMock(spec=SSHClient)
        mock_stdout = MagicMock()
        mock_stdout.read.return_value.decode.return_value = 'Package installed successfully'
        mock_ssh.exec_command.return_value = (None, mock_stdout, None)
        expected_output = 'Package installed successfully\n'
        with patch('sys.stdout', new=StringIO()) as fake_output:
            await install_package(mock_ssh, 'nginx')
            self.assertEqual(fake_output.getvalue(), expected_output)


    async def test_run_tasks_on_servers(self):
        mock_ssh = MagicMock(spec=SSHClient)
        with patch.object(asyncio, 'gather', return_value=None) as mock_gather, \
            patch.object(asyncio, 'get_running_loop', return_value=asyncio.get_event_loop()) as mock_loop, \
            patch.object(ThreadPoolExecutor, 'submit', return_value=Future()):
            servers = [
                {'hostname': 'test1.com', 'username': 'user1', 'password': 'password1'},
                {'hostname': 'test2.com', 'username': 'user2', 'password': 'password2'}
            ]
            tasks = [update_packages, lambda ssh: install_package(ssh, 'nginx'), lambda ssh: install_package(ssh, 'python3')]
            for server in servers:
                ssh = await ssh_connect(server['hostname'], server['username'], server['password'])
                tasks_to_run = []
                for task in tasks:
                    tasks_to_run.append(asyncio.create_task(task(ssh)))
                await asyncio.gather(*tasks_to_run)
                ssh.close()
            mock_gather.assert_called_once()
            mock_loop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
