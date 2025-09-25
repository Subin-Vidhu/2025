- [Course Link](https://www.udemy.com/course/metasploit-from-scratch-beginner-to-professional/)

- Install kali linux and metasploit - Setting up a lab environment

    - https://www.kali.org/get-kali/#kali-virtual-machines | vmware

    - https://sourceforge.net/projects/metasploitable/

- Open both virtual machines in vmware workstation 17 player | Configuring Framework

- Start kali linux and metasploit

- Make sure postgresql is running in kali linux

    - sudo service postgresql start

    - sudo service postgresql status

    - sudo msfdb init

    - sudo msfdb status

    - sudo msfconsole

    - db_status

    - db_connect -y /usr/share/metasploit-framework/config/database.yml

    - db_status


- Creating and managing workspaces

    - workspace -a <name> : create a new workspace

    - workspace : list all workspaces

    - workspace <name> : switch to a workspace

    - workspace -d <name> : delete a workspace

    - workspaces : list all workspaces

    - workspace -r : rename a workspace

    - hosts : list all hosts in the current workspace

    - services : list all services in the current workspace

    - db_nmap <ip> : scan a host and add it to the database

    - db_nmap -sV -p 1-65535 <ip> : scan all ports and services of a host

    - vulns : list all vulnerabilities in the current workspace

    - notes : list all notes in the current workspace

- msfconsole

    - msfconsole : start the metasploit console

    - help : list all commands

    - banner : display the metasploit banner

    - version : display the metasploit version

    - search <name> : search for a module, eg search vsftpd

    - use <module> : use a module, eg use exploit/unix/ftp/vsftpd_234_backdoor

    - show options : show the options of the current module

    - set <option> <value> : set an option, eg set RHOSTS <ip>

    - setg <option> <value> : set a global option, eg setg RHOSTS <ip>  

    - getg <option> : get a global option, eg getg RHOSTS 

    - unset <option> : unset an option, eg unset RHOSTS 

    - search type:payload : search for a payload 

    - show payloads : show all payloads for the current module

    - search type:auxiliary : search for auxiliary modules

    - show auxiliary : show all auxiliary modules

    - search type:payload platform:windows : search for windows payloads

    - search type:exploit platform:linux : search for linux exploits

    - search type:payload name:ssh : search for ssh payloads

    - set PAYLOAD <payload> : set a payload, eg set PAYLOAD linux/x86/meterpreter/reverse_tcp

    - show encoders : show all encoders

    - set LHOST <ip> : set the local host, eg set LHOST <ip>

    - set LPORT <port> : set the local port, eg set LPORT 4444

    - save : save the current module settings

- Port scanning and Enumeration

    - 