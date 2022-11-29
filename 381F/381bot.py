# bot.py
import os
import VPNpeer as peer
import GetIP as get
import schedule
import time
import discord
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

oldIP = '172.16.0.2'
changed = True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

def check():
    global oldIP
    global changed
    global newIP
    newIP = get.sendIP()
    if newIP != oldIP:
        peer.FixPeer(newIP, oldIP)
        print("The new ip is: "+newIP)
        changed = False
        oldIP = newIP
    else:
        changed = True

a = """
type "hi" for a greeting
type "start" to start continous VPN debugging program
type "test" to run VPN debugging once
type "monitor to monitor the interfaces on CSR1
"""

@client.event
async def on_message(message):
    if message.author == client.user:
        global changed
        global newIP
        return
 
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
    
    elif message.content.startswith('start'):

        schedule.every(1).minutes.do(check())
        if changed == False:
            await message.channel.send("The new ip address of G0/2 on CSR2 is: " + newIP)

    elif message.content.startswith('test'):
        await message.channel.send("Testing")
        check()
        if changed == False:
            await message.channel.send("The new ip address of G0/2 on CSR2 is: " + newIP)

    elif message.content.startswith('monitor'):
        os.system("ansible-playbook -i ./inventory 318ans.yaml")
        f = open('intMonitor.txt', 'r')
        file_contents = f.read()
        await message.channel.send("CSR2")
        await message.channel.send(file_contents)
        f.close()
        os.system("ansible-playbook -i ./inventory1 318ans.yaml")
        f = open('intMonitor.txt', 'r')
        file_contents = f.read()
        await message.channel.send("CSR1")
        await message.channel.send(file_contents)
        f.close()

    elif message.content.startswith('help'):
        await message.channel.send(a)
        
    else :
        await message.channel.send('type "help" for list of commands')
client.run(TOKEN)
