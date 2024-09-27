import paramiko
import logging
import os

import DP832_Power_supply as Power_Supply_Control # type: ignore
import time

paramiko.util.log_to_file("paramiko.log")
logging.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     handlers=[logging.StreamHandler()])

def list_connection_to_internet():
    try:
        os.system("nmcli connection show")
    except Exception as e:
        print("Error listing devices:", e)
        return []


def connect_to_ssh(ip_address, username, private_key_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if not os.path.exists(private_key_path):
            print("Private key file does not exist.")
            return None
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh_client.connect(ip_address, username=username, pkey=private_key)
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
        return None
    except paramiko.SSHException as e:
        print(f"An SSH error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return ssh_client

def execute_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    stdout.channel.recv_exit_status()  # Wait for the command to complete
    output = stdout.read().decode()
    error = stderr.read().decode()
    return output, error

def main():
    print("Connecting to Morgan Lab Pi")
    private_key_path = r"C:\Users\mhans\SSH\id_rsa.txt"
    ssh_client = connect_to_ssh("192.168.86.32", "morgan", private_key_path)

    if ssh_client:
        print("Connected to Morgan Lab Pi")
        virtual_environment = "/myenv/bin/activate"
        home = "/home/morgan/Lab_Projects"
        # Commands to navigate to the repository, activate the virtual environment, and perform git pull
        commands = [
            "cd /home/morgan/myenv/bin"
            "source activate",
            
            f"cd {home}",  # Ensure this path is correct
          
            "git pull origin main"
        ]
        print(commands)
        for command in commands:
            time.sleep(5)
            output, error = execute_command(ssh_client, command)
            if output:
                print(f"Output: {output}")
            if error:
                print(f"Error: {error}")
        
        # Example of power supply control usage
        try:
            psu = Power_Supply_Control.EAPSB9000Controller("USB0::0x1AB1::0x0E11::DP8C172602885::INSTR")
          
            device_connected = psu.check_connection()
            if device_connected:
                print("Power Supply connected")
                read_vi = psu.get_voltage()
                print(read_vi)
            else:
                print("Power Supply not connected")
        except Exception as e:
            print(f"An error occurred while initializing the power supply controller: {e}")

        ssh_client.close()
    else:
        print("Failed to connect to Morgan Lab Pi")

if __name__ == "__main__":
    main()
