import netmiko
from netmiko import ConnectHandler

router = {'device_type':'cisco_ios','host':'192.168.56.102','username':'cisco','password':'cisco123!','port':'22','secret':'cisco','verbose': True}

def FixPeer(newIP,oldIP):
    connection = ConnectHandler(**router)
    prompt = connection.find_prompt()
    if'>'in prompt:
        connection.enable()

    if not connection.check_config_mode():
        connection.config_mode()

    output1 = connection.send_command('no crypto isakmp key cisco address '+oldIP)
    print(output1+"1")
    output2 = connection.send_command('crypto isakmp key cisco address '+newIP)
    print(output2+"2")
    Crypt = ['crypto map Crypt 10 ipsec-isakmp', 'no set peer '+oldIP, 'set peer '+newIP]
    output3 = connection.send_config_set(Crypt)
    print(output3+"3")
    connection.exit_config_mode()
    print('Closing connection')
    connection.disconnect()