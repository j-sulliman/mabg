# meraki

# MABG - Meraki AS Built Generator: Automation of AS Built Document for Meraki
Retrieves Meraki configuration via an API call, stores returned data and writes to a word document for further 
editing and customisation. 

Optional editing and review of imported data through Django admin front end (i.e. http://127.0.0.1:8080/meraki/defaults/)  



# Setup

1) Ensure Meraki API Access is enabled
![alt text](https://github.com/j-sulliman/meraki/blob/master/AsBuilts/media/Enable-API.png)


# Create virtual environment / sandbox
```
JASULLI2-M-F04H:Programming jasulli2$ cd meraki_asbuilt/
JASULLI2-M-F04H:meraki_asbuilt jasulli2$ ls
JASULLI2-M-F04H:meraki_asbuilt jasulli2$ python3 -m venv venv
JASULLI2-M-F04H:meraki_asbuilt jasulli2$ source venv/bin/activate
```

# Initialise git and pull remote MABG repository
```
(venv) JASULLI2-M-F04H:meraki_asbuilt jasulli2$ git init
Initialized empty Git repository in /Users/jasulli2/OneDrive - Cisco/Programming/meraki_asbuilt/.git/
(venv) JASULLI2-M-F04H:meraki_asbuilt jasulli2$ git pull https://github.com/j-sulliman/meraki.git
 
remote: Enumerating objects: 1511, done.
remote: Counting objects: 100% (1511/1511), done.
remote: Compressing objects: 100% (1153/1153), done.
remote: Total 1511 (delta 329), reused 1463 (delta 284), pack-reused 0
Receiving objects: 100% (1511/1511), 5.95 MiB | 2.13 MiB/s, done.
Resolving deltas: 100% (329/329), done.
From https://github.com/j-sulliman/meraki
 * branch            HEAD       -> FETCH_HEAD
```

# Install the python dependencies
```
(venv) JASULLI2-M-F04H:meraki_asbuilt jasulli2$ 
(venv) JASULLI2-M-F04H:meraki_asbuilt jasulli2$ pip3 install -r requirements.txt 


Successfully installed Django-2.2.4 bootstrap4-0.1.0 certifi-2019.6.16 chardet-3.0.4 django-tables2-2.1.0 et-xmlfile-1.0.1 idna-2.8 jdcal-1.4.1 lxml-4.4.0 numpy-1.17.0 openpyxl-2.6.2 pandas-0.25.0 pprint-0.1 python-dateutil-2.8.0 python-docx-0.8.10 pytz-2019.1 requests-2.22.0 six-1.12.0 sqlparse-0.3.0 urllib3-1.25.3
```

# Start Django Server
```
$ cd AsBuilts/
$ python3 manage.py runserver 0:8080

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Starting development server at http://0:8080/
Quit the server with CONTROL-C.
```

# Logon and Import NXOS file
i.e. http://127.0.0.1:8080
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.23.58%20PM.png)

Provide the defaults for configuration naming convention and BD construct.  BD mode in most cases should be l2 which will enable ARP and BUM flooding.  L3 mode will enable unicast routing and configure the SVI address as a BD Subnet.  EPGs will be created as "Preferred group - Include" members.
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.26.01%20PM.png)


View and Edit the Imported configuration
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.51.46%20PM.png)
 
Enter the APIC connection info and submit
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.52.47%20PM.png)


View the resulting JSON and HTTP Post status code
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.56.15%20PM.png)
- Object configuration and DN/URL can be used with other REST API clients - i.e. postman, curl, or paste directly into APIC

Check the APIC
![alt text](https://github.com/j-sulliman/nxos_to_aci/blob/master/Screen%20Shot%202019-07-18%20at%201.57.24%20PM.png)

# Create associated fabric access policies and L3Os manually
Rationale - items like Physical domain, vlan pools to legacy network will likely only be configured once.  
Fabric access policies therefore less far less time consuming than tenant policy.

L3O configuration is environment dependant.

# Disclaimer
Tested against NXOS 7.X configuration files, may work with IOS but needs testing.
Use at your own risk - recommend dry-run against a simulator or non-prod APIC
