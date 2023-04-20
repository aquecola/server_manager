import asyncio
import paramiko
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


env_hostname = (os.environ.get('HOST'))
env_username = (os.environ.get('LOGIN'))
env_port = (os.environ.get('PORT'))
env_password = (os.environ.get('PASSWORD'))


async def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=env_hostname, username=env_username, port=env_port, password=env_password)

    uptime_output = await uptime_call(ssh)
    print("Uptime output:", uptime_output)

    docker_ps_output = await docker_ps(ssh)
    print("Docker PS output:\n\n", docker_ps_output)

    ssh.close()

async def uptime_call(ssh):
    stdin, stdout, stderr = ssh.exec_command("uptime")
    output = await asyncio.to_thread(stdout.read)
    return output.decode()

async def docker_ps(ssh):
    stdin, stdout, stderr = ssh.exec_command("docker ps")
    output = await asyncio.to_thread(stdout.read)
    return output.decode()

asyncio.run(main())