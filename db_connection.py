from sshtunnel import SSHTunnelForwarder
import pymysql

"""
I create a SSH Tunnel to connect to a Ubuntu server which is placed on a virtual machine on my computer.
On that Ubuntu server is located the "dissertation" database.
"""

tunnel = SSHTunnelForwarder(('192.168.64.128', 22), ssh_username="paw", ssh_password="masteretti", remote_bind_address=("127.0.0.1", 3306)) 
tunnel.start()

conn = pymysql.connect(host='localhost', user="root", password="masteretti", database="dissertation", port=tunnel.local_bind_port)