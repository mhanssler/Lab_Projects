import paramiko
import time
import logging
import Power_Supply_Control
import os


"""
This script is used to control the lab equipment for the measurement. Using SSH to control the power supply and the oscilloscope, and the load"""

paramiko.util.log_to_file("paramiko.log")
logging.basicConfig(level=logging.INFO)

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
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return ssh_client

def disconnect_from_ssh(ssh_client):
    ssh_client.close()

def main():
    # Connect to the SSH server
    print("Connecting to Morgan Lab Pi")
    path = os.path.exists(r"C:\Users\mhans\SSH\id_rsa.txt")
    print(path)
    private_key_path = r"C:\Users\mhans\SSH\id_rsa.txt"
    ssh_client = connect_to_ssh("192.168.86.32", "morgan", private_key_path )
    
    if ssh_client:
        print("Connected to Morgan Lab Pi")
    else:
        print("Failed to connect to Morgan Lab Pi")
        return
    psu = Power_Supply_Control.EAPSB9000Controller("USB0::0x1AB1::0x0E11::DP8A204800001::INSTR")
    # Create a power supply controller
    device_connected = psu.check_connection()
    if device_connected:
        print("Power Supply connected")
    else:
        print("Power Supply not connected")
    
    read_vi = psu.get_voltage()
    print(read_vi)

    # Create an oscilloscope controller
    #oscilloscope = RigolScopeController("USB0::0x1AB1::0x0588::DS1ET153818956::INSTR")
if __name__ == "__main__":
    main()

