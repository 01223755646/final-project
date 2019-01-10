import sys, os, django
import sqlite3

linkDB = "/home/pi/Desktop/final_project/final_project/db.sqlite3"

def Get_Info_Network(DlinkDB):
    con = sqlite3.connect(linkDB)
    c = con.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(c.fetchall())
    c.execute("SELECT * FROM 'network_network'")
    ID, MODE, SSID, PSK, IP, GATEWAY, SUBNET, IP_MODE, SIGNALSTRENGTH, UPDATE = c.fetchall()[0]
    print(ID, MODE, SSID, PSK, IP, GATEWAY, SUBNET, IP_MODE, SIGNALSTRENGTH, UPDATE)
    c.close()
    return ID, MODE, SSID, PSK, IP, GATEWAY, SUBNET, IP_MODE, SIGNALSTRENGTH, UPDATE

ID, MODE, SSID, PSK, IP, GATEWAY, SUBNET, IP_MODE, SIGNALSTRENGTH, UPDATE = Get_Info_Network(linkDB)

# MODE: ACCESSPOINT, WIFISTATION
# SSID: 
# PSK: 
# IP:
# GATEWAY:
# SUBNETMASK:
# IP_MODE: STATIC, DHCP

#IP_MODE = 1
#MODE = 2 
if MODE == 'STATICWS':
    # 1. Stop dnsmasq & hostapd
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl stop hostapd")
    # 2. Fix wpa_supplicant.conf
    os.system("sudo sed -i 's/network.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/key_.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/ssid.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/psk.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/}.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/wpa_supplicant/wpa_supplicant.conf")
    # 3. Insert network get from database
    os.system("sudo sed -i '/update_config=1/a network={\\n\\tssid=\"%s\"\\n\\tpsk=\"%s\" \\n\\tkey_mgmt=WPA-PSK \\n}' /etc/wpa_supplicant/wpa_supplicant.conf"%(SSID, PSK)) 
    # 4. Clean IP of AP mode
    #    Clean static ip of WS mode dhcpcd.conf
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/interface.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static routers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static domain_name_servers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/interface.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/nohook wpa_supplicant.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/dhcpcd.conf")
    # 5. Insert IP of Static mode
    os.system("sudo sed -i '/#<wlan0>#start/a interface wlan0\\nstatic ip_address=%s/24\\nstatic routers=%s\\nstatic domain_name_servers=%s' /etc/dhcpcd.conf"%(IP,GATEWAY, GATEWAY))
    # 6. Restart dhcpcd
    os.system("sudo service dhcpcd restart")

elif MODE == 'DHCPSW': 
    # 1. Stop dnsmasq & hostapd 
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl stop hostapd")
    # 2. Fix wpa_supplicant.conf
    os.system("sudo sed -i 's/network.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/key_.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/ssid.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/psk.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/}.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/wpa_supplicant/wpa_supplicant.conf")
    # 3. Insert network get from database
    os.system("sudo sed -i '/update_config=1/a network={\\n\\tssid=\"%s\"\\n\\tpsk=\"%s\" \\n\\tkey_mgmt=WPA-PSK \\n}' /etc/wpa_supplicant/wpa_supplicant.conf"%(SSID, PSK)) 
    # 4. Clean IP of AP mode
    #    Clean static ip of WS mode dhcpcd.conf
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/interface.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static routers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static domain_name_servers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/dhcpcd.conf")
    
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/interface.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/nohook wpa_supplicant.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/dhcpcd.conf")
    ifc = os.popen("ifconfig wlan0")
    for line in ifc:
    #print(line)
        if 'inet ' in line:
        #print(line[13:28])
            IP = line[8:len(line)-1].split("  ")[0][5:]
            print(IP)
            wl.IP = IP
            wl.save()
    # 5. Restart dhcpcd
    os.system("sudo service dhcpcd restart")
elif  MODE == 'ACCESSPOINT':
    # 1. Stop dnsmasq & hostapd 
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl stop hostapd")
    # 2. Fix wpa_supplicant.conf
    os.system("sudo sed -i 's/network.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/key_.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/ssid.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/psk.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i 's/}.*//g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    # 3. Clean static ip of WS mode dhcpcd.conf
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/interface.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static routers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<wlan0>#start/,/#<wlan0>#end/s/static domain_name_servers.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/dhcpcd.conf")
    # 4. Insert SSID & PSK of AP 
    os.system("sudo sed -i 's/ssid.*/ssid=%s/g' /etc/hostapd/hostapd.conf"%(SSID))
    os.system("sudo sed -i 's/wpa_passphrase=.*/wpa_passphrase=%s/g' /etc/hostapd/hostapd.conf"%(PSK))
    os.system("sudo sed -i 's/_ssid.*/_ssid=0/g' /etc/hostapd/hostapd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/hostapd/hostapd.conf")
    # 5. Insert static ip of AP mode dhcpcd.conf
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/interface wlan0//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/static ip_address.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/,/#<ap>#end/s/nohook wpa_supplicant.*//g' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/^\s*$/d' /etc/dhcpcd.conf")
    os.system("sudo sed -i '/#<ap>#start/a interface wlan0\\n\\tstatic ip_address=192.168.4.1\/24\\n\\tnohook wpa_supplicant' /etc/dhcpcd.conf")
    os.system("sudo service dhcpcd restart")
    os.system("sudo systemctl start dnsmasq")
    os.system("sudo systemctl start hostapd")


os.system('sudo sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = [\'%s\',]/g" /home/pi/Desktop/final_project/final_project/final_project/settings.py'%(IP))
os.system('sudo python /home/pi/Desktop/final_project/final_project/manage.py runserver %s:80'%(IP))
