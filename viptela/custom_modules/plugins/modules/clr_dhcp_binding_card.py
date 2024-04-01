import paramiko
import csv
import time
import getpass
import sys

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Enter the side code to connect to.

site_ip = input("Enter side Code: ")

# dictionary made from csv file
dict_site = {}

#creates site_code dict_site:

with open("vEdge.csv") as f:
    reader = csv.reader(f, delimiter=";")
    dict_site = {rows[0]:rows[1] for rows in reader}

ip = dict_site[str(site_ip)]

print (f'you are connecting to: {ip}')

username = input("enter username: ")
password = getpass.getpass(" Enter Password:")

try:
    ssh_client.connect(hostname = ip , port = "22", username = username, password = password,
                        look_for_keys=False, allow_agent=False)
except paramiko.AuthenticationException as error:
    print("authentication failed")
    error = input("press enter to exit")

# sending commands

shell = ssh_client.invoke_shell()
shell.send('term len 0 \n')
shell.send('clear ip dhcp binding vrf 3 *\n')
shell.send('sho ip dhcp binding \n')
time.sleep(1)

output = shell.recv(10000)
print(type(output))
output = output.decode('utf-8')
print(output)

pause = input("Press enter to exit;")

if ssh_client.get_transport().is_active() == True:
    print("closing the connection")
    ssh_client.close()

