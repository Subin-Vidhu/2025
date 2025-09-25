# NMAP Mastery - Ultimate Guide to Network Scanning

[![Udemy Course](https://img.shields.io/badge/Udemy-Course-blue?style=flat-square&logo=udemy)](https://www.udemy.com/course/nmap-mastery-ultimate-guide-to-network-scanning)
[![PDF Certificate](https://img.shields.io/badge/Certificate-PDF-red?style=flat-square&logo=adobe)](NMAP%20Mastery%20-%20Ultimate%20Guide%20to%20Network%20Scanning.pdf)

## 📖 Course Overview

This comprehensive course covers NMAP (Network Mapper), a powerful open-source tool essential for network security professionals, penetration testers, and system administrators.

## 🔍 What is NMAP?

**Nmap (Network Mapper)** is a free and open-source network discovery and security auditing utility. It uses raw IP packets in novel ways to determine:

### Core Capabilities:
- **Host Discovery** - Identifying live hosts on a network
- **Port Scanning** - Determining which ports are open on target hosts  
- **Service Enumeration** - Identifying services running on open ports
- **OS Detection** - Determining the operating system of target hosts
- **Vulnerability Scanning** - Identifying known vulnerabilities in running services

## 🚀 Quick Start Commands

### Basic Network Discovery
```bash
# Windows - Ping Scan (List all active devices on network)
nmap -sn 192.168.1.0/24

# Linux - Ping Scan (requires sudo for raw packets)
sudo nmap -sn 192.168.1.0/24

# Scan specific port on target
nmap -p 8080 10.0.2.15
```

### Advanced Comprehensive Scan
```bash
# Full port scan with comprehensive analysis
nmap -p 1-65535 -T4 -A -v <target>

# Scan top 20 most common ports
nmap --top-ports 20 192.168.0.41
```

## 🔬 Scan Types and Techniques

### Primary Scan Types

| Scan Type | Flag | Description | Use Case |
|-----------|------|-------------|----------|
| **Ping Scan** | `-sn` | Determines which hosts are up using ICMP echo requests | Network discovery |
| **SYN Scan** | `-sS` | Half-open scan using SYN packets (default) | Stealthy port scanning |
| **UDP Scan** | `-sU` | Scans for open UDP ports | Finding UDP services |
| **TCP Connect** | `-sT` | Establishes full TCP connections | When SYN scan not possible |
| **Idle Scan** | `-sI` | Uses zombie host for ultra-stealthy scanning | Advanced evasion |

### Detection and Analysis

| Feature | Flag | Description |
|---------|------|-------------|
| **Service Version** | `-sV` | Determines service versions on open ports |
| **OS Detection** | `-O` | Identifies target operating system |
| **Aggressive Scan** | `-A` | Combines OS detection, version detection, script scanning, and traceroute |

### Examples

```bash
# Ping scan to find live hosts
nmap -sn 192.168.1.0/24

# SYN scan (default, stealthy)
nmap -sS target.com

# UDP port scan
nmap -sU target.com

# Service version detection
nmap -sV target.com

# OS detection
nmap -O target.com

# Aggressive comprehensive scan
nmap -A target.com

# TCP connect scan
nmap -sT target.com

# Idle scan using zombie host
nmap -sI zombie_host target.com
```


## 💻 Practical Examples and Output Analysis

### Example 1: Top Ports Scan
```bash
nmap --top-ports 20 192.168.0.41
```

**Output Analysis:**
```
PORT     STATE    SERVICE
135/tcp  open     msrpc          # Windows RPC service
3306/tcp open     mysql          # MySQL database
21/tcp   filtered ftp            # FTP potentially blocked by firewall
22/tcp   filtered ssh            # SSH potentially blocked by firewall
80/tcp   filtered http           # HTTP potentially blocked by firewall
443/tcp  filtered https          # HTTPS potentially blocked by firewall
```

### Example 2: Web Service Analysis
```bash
# Basic scan
nmap testphp.vulnweb.com

# Targeted port scan with service detection
nmap -p 80 -Pn -sV testphp.vulnweb.com
```

**Key Findings:**
- **Port 80/tcp**: Open HTTP service
- **Service**: nginx 1.19.0
- **Host Status**: Active and responding

```
D:\__SHARED__\subin_gpu_server_3>nmap -O -sV 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:06 +0530
Nmap scan report for 192.168.0.41
Host is up (0.0027s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
135/tcp  open  msrpc   Microsoft Windows RPC
2179/tcp open  vmrdp?
3306/tcp open  mysql   MySQL (unauthorized)
5001/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.9.13)
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 11|10|2008 (91%), FreeBSD 6.X (88%)
OS CPE: cpe:/o:microsoft:windows_11 cpe:/o:freebsd:freebsd:6.2 cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2008::beta3 cpe:/o:microsoft:windows_server_2008
Aggressive OS guesses: Microsoft Windows 11 21H2 (91%), FreeBSD 6.2-RELEASE (88%), Microsoft Windows 10 (86%), Microsoft Windows Server 2008 or 2008 Beta 3 (85%), Microsoft Windows 10 1607 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.30 seconds
```


```
C:\Program Files\Orthanc Server\Tools>nmap -sP 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:43 +0530
Nmap scan report for 192.168.0.41
Host is up (0.00s latency).
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)
Nmap done: 1 IP address (1 host up) scanned in 3.71 seconds

C:\Program Files\Orthanc Server\Tools>nmap -sP 192.168.0.196
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:44 +0530
Nmap scan report for 192.168.0.196
Host is up (0.00s latency).
MAC Address: D8:5E:D3:8E:3B:E8 (Giga-byte Technology)
Nmap done: 1 IP address (1 host up) scanned in 3.70 seconds

C:\Program Files\Orthanc Server\Tools>nmap -p 22,80 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:45 +0530
Nmap scan report for 192.168.0.41
Host is up (0.00s latency).

PORT   STATE    SERVICE
22/tcp filtered ssh
80/tcp filtered http
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Nmap done: 1 IP address (1 host up) scanned in 5.00 seconds

C:\Program Files\Orthanc Server\Tools>nmap -sS 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:47 +0530
Nmap scan report for 192.168.0.41
Host is up (0.00076s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE
135/tcp  open  msrpc
2179/tcp open  vmrdp
3306/tcp open  mysql
5001/tcp open  commplex-link
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Nmap done: 1 IP address (1 host up) scanned in 8.96 seconds

C:\Program Files\Orthanc Server\Tools>D:

D:\>cd __SHARED__

D:\__SHARED__>cd subin_gpu_server_3

D:\__SHARED__\subin_gpu_server_3>nmap -sS 192.168.0.41 -oN out.txt
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:52 +0530
Nmap scan report for 192.168.0.41
Host is up (0.0015s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE
135/tcp  open  msrpc
2179/tcp open  vmrdp
3306/tcp open  mysql
5001/tcp open  commplex-link
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Nmap done: 1 IP address (1 host up) scanned in 8.53 seconds

D:\__SHARED__\subin_gpu_server_3>cat out.txt
'cat' is not recognized as an internal or external command,
operable program or batch file.

D:\__SHARED__\subin_gpu_server_3>type out.txt
# Nmap 7.98 scan initiated Thu Sep 25 09:52:23 2025 as: nmap -sS -oN out.txt 192.168.0.41
Nmap scan report for 192.168.0.41
Host is up (0.0015s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE
135/tcp  open  msrpc
2179/tcp open  vmrdp
3306/tcp open  mysql
5001/tcp open  commplex-link
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

# Nmap done at Thu Sep 25 09:52:32 2025 -- 1 IP address (1 host up) scanned in 8.53 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -top-ports 5 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:53 +0530
Nmap scan report for 192.168.0.41
Host is up (0.0010s latency).

PORT    STATE    SERVICE
21/tcp  filtered ftp
22/tcp  filtered ssh
23/tcp  filtered telnet
80/tcp  filtered http
443/tcp filtered https
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Nmap done: 1 IP address (1 host up) scanned in 4.99 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -top-ports 20 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 09:53 +0530
Nmap scan report for 192.168.0.41
Host is up (0.00023s latency).

PORT     STATE    SERVICE
21/tcp   filtered ftp
22/tcp   filtered ssh
23/tcp   filtered telnet
25/tcp   filtered smtp
53/tcp   filtered domain
80/tcp   filtered http
110/tcp  filtered pop3
111/tcp  filtered rpcbind
135/tcp  open     msrpc
139/tcp  filtered netbios-ssn
143/tcp  filtered imap
443/tcp  filtered https
445/tcp  filtered microsoft-ds
993/tcp  filtered imaps
995/tcp  filtered pop3s
1723/tcp filtered pptp
3306/tcp open     mysql
3389/tcp filtered ms-wbt-server
5900/tcp filtered vnc
8080/tcp filtered http-proxy
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Nmap done: 1 IP address (1 host up) scanned in 5.24 seconds

D:\__SHARED__\subin_gpu_server_3>nmap http://testphp.vulnweb.com/
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:00 +0530
Unable to split netmask from target expression: "http://testphp.vulnweb.com/"
WARNING: No targets were specified, so 0 hosts scanned.
Nmap done: 0 IP addresses (0 hosts up) scanned in 0.04 seconds

D:\__SHARED__\subin_gpu_server_3>nmap testphp.vulnweb.com
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:00 +0530
Nmap scan report for testphp.vulnweb.com (44.228.249.3)
Host is up (0.25s latency).
rDNS record for 44.228.249.3: ec2-44-228-249-3.us-west-2.compute.amazonaws.com
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 24.23 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -p 80 -Pn testphp.vulnweb.com
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:02 +0530
Nmap scan report for testphp.vulnweb.com (44.228.249.3)
Host is up (0.24s latency).
rDNS record for 44.228.249.3: ec2-44-228-249-3.us-west-2.compute.amazonaws.com

PORT   STATE  SERVICE
80/tcp closed http

Nmap done: 1 IP address (1 host up) scanned in 0.94 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -p 80 -Pn testphp.vulnweb.com
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:02 +0530
Nmap scan report for testphp.vulnweb.com (44.228.249.3)
Host is up (0.26s latency).
rDNS record for 44.228.249.3: ec2-44-228-249-3.us-west-2.compute.amazonaws.com

PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 6.50 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -p 80 -Pn -sV testphp.vulnweb.com
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:02 +0530
Nmap scan report for testphp.vulnweb.com (44.228.249.3)
Host is up (0.25s latency).
rDNS record for 44.228.249.3: ec2-44-228-249-3.us-west-2.compute.amazonaws.com

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.19.0

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.12 seconds

D:\__SHARED__\subin_gpu_server_3>nmap -O -sV 192.168.0.41
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:06 +0530
Nmap scan report for 192.168.0.41
Host is up (0.0027s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
135/tcp  open  msrpc   Microsoft Windows RPC
2179/tcp open  vmrdp?
3306/tcp open  mysql   MySQL (unauthorized)
5001/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.9.13)
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 11|10|2008 (91%), FreeBSD 6.X (88%)
OS CPE: cpe:/o:microsoft:windows_11 cpe:/o:freebsd:freebsd:6.2 cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2008::beta3 cpe:/o:microsoft:windows_server_2008
Aggressive OS guesses: Microsoft Windows 11 21H2 (91%), FreeBSD 6.2-RELEASE (88%), Microsoft Windows 10 (86%), Microsoft Windows Server 2008 or 2008 Beta 3 (85%), Microsoft Windows 10 1607 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.30 seconds

D:\__SHARED__\subin_gpu_server_3>nmap /usr
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:13 +0530
Unable to split netmask from target expression: "/usr"
WARNING: No targets were specified, so 0 hosts scanned.
Nmap done: 0 IP addresses (0 hosts up) scanned in 0.04 seconds

D:\__SHARED__\subin_gpu_server_3>cd C:\Program Files (x86)\Nmap\scripts

D:\__SHARED__\subin_gpu_server_3>C:

C:\Program Files (x86)\Nmap\scripts>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

C:\Program Files (x86)\Nmap\scripts>dir
 Volume in drive C has no label.
 Volume Serial Number is CEC7-9556

 Directory of C:\Program Files (x86)\Nmap\scripts

24-09-2025  16:40    <DIR>          .
24-09-2025  16:40    <DIR>          ..
09-08-2025  08:39             3,901 acarsd-info.nse
09-08-2025  08:39             8,749 address-info.nse
09-08-2025  08:39             3,345 afp-brute.nse
09-08-2025  08:39             6,463 afp-ls.nse
09-08-2025  08:39             7,001 afp-path-vuln.nse
09-08-2025  08:39             5,600 afp-serverinfo.nse
09-08-2025  08:39             2,621 afp-showmount.nse
09-08-2025  08:39             2,262 ajp-auth.nse
09-08-2025  08:39             2,983 ajp-brute.nse
09-08-2025  08:39             1,329 ajp-headers.nse
09-08-2025  08:39             2,590 ajp-methods.nse
09-08-2025  08:39             3,051 ajp-request.nse
09-08-2025  08:39             6,719 allseeingeye-info.nse
09-08-2025  08:39             1,678 amqp-info.nse
09-08-2025  08:39            15,024 asn-query.nse
09-08-2025  08:39             2,054 auth-owners.nse
09-08-2025  08:39               870 auth-spoof.nse
09-08-2025  08:39             9,050 backorifice-brute.nse
09-08-2025  08:39            10,193 backorifice-info.nse
09-08-2025  08:39            53,131 bacnet-info.nse
09-08-2025  08:39             6,136 banner.nse
09-08-2025  08:39             2,012 bitcoin-getaddr.nse
09-08-2025  08:39             1,812 bitcoin-info.nse
09-08-2025  08:39             4,437 bitcoinrpc-info.nse
09-08-2025  08:39             4,079 bittorrent-discovery.nse
09-08-2025  08:39             1,344 bjnp-discover.nse
09-08-2025  08:39             4,441 broadcast-ataoe-discover.nse
09-08-2025  08:39             2,964 broadcast-avahi-dos.nse
09-08-2025  08:39             4,740 broadcast-bjnp-discover.nse
09-08-2025  08:39             2,438 broadcast-db2-discover.nse
09-08-2025  08:39             9,256 broadcast-dhcp-discover.nse
09-08-2025  08:39             2,693 broadcast-dhcp6-discover.nse
09-08-2025  08:39             1,444 broadcast-dns-service-discovery.nse
09-08-2025  08:39             3,866 broadcast-dropbox-listener.nse
09-08-2025  08:39            11,696 broadcast-eigrp-discovery.nse
09-08-2025  08:39             3,472 broadcast-hid-discoveryd.nse
09-08-2025  08:39            14,081 broadcast-igmp-discovery.nse
09-08-2025  08:39             3,184 broadcast-jenkins-discover.nse
09-08-2025  08:39             9,225 broadcast-listener.nse
09-08-2025  08:39             3,813 broadcast-ms-sql-discover.nse
09-08-2025  08:39             1,909 broadcast-netbios-master-browser.nse
09-08-2025  08:39             2,748 broadcast-networker-discover.nse
09-08-2025  08:39             2,005 broadcast-novell-locate.nse
09-08-2025  08:39            16,288 broadcast-ospf2-discover.nse
09-08-2025  08:39             1,966 broadcast-pc-anywhere.nse
09-08-2025  08:39             3,550 broadcast-pc-duo.nse
09-08-2025  08:39             6,300 broadcast-pim-discovery.nse
09-08-2025  08:39             8,830 broadcast-ping.nse
09-08-2025  08:39             2,617 broadcast-pppoe-discover.nse
09-08-2025  08:39             4,966 broadcast-rip-discover.nse
09-08-2025  08:39             6,145 broadcast-ripng-discover.nse
09-08-2025  08:39             3,869 broadcast-sonicwall-discover.nse
09-08-2025  08:39             5,316 broadcast-sybase-asa-discover.nse
09-08-2025  08:39             1,892 broadcast-tellstick-discover.nse
09-08-2025  08:39             1,511 broadcast-upnp-info.nse
09-08-2025  08:39               924 broadcast-versant-locate.nse
09-08-2025  08:39             2,084 broadcast-wake-on-lan.nse
09-08-2025  08:39             6,851 broadcast-wpad-discover.nse
09-08-2025  08:39             3,117 broadcast-wsdd-discover.nse
09-08-2025  08:39             1,996 broadcast-xdmcp-discover.nse
09-08-2025  08:39             3,742 cassandra-brute.nse
09-08-2025  08:39             2,564 cassandra-info.nse
09-08-2025  08:39             1,506 cccam-version.nse
09-08-2025  08:39            18,114 cics-enum.nse
09-08-2025  08:39            13,755 cics-info.nse
09-08-2025  08:39            11,113 cics-user-brute.nse
09-08-2025  08:39             9,403 cics-user-enum.nse
09-08-2025  08:39             4,749 citrix-brute-xml.nse
09-08-2025  08:39             4,644 citrix-enum-apps-xml.nse
09-08-2025  08:39             4,170 citrix-enum-apps.nse
09-08-2025  08:39             1,126 citrix-enum-servers-xml.nse
09-08-2025  08:39             3,880 citrix-enum-servers.nse
09-08-2025  08:39             7,092 clamav-exec.nse
09-08-2025  08:39             5,019 clock-skew.nse
09-08-2025  08:39             9,405 coap-resources.nse
09-08-2025  08:39             2,594 couchdb-databases.nse
09-08-2025  08:39             8,986 couchdb-stats.nse
09-08-2025  08:39             1,082 creds-summary.nse
09-08-2025  08:39             2,137 cups-info.nse
09-08-2025  08:39             1,420 cups-queue-info.nse
09-08-2025  08:39             3,879 cvs-brute-repository.nse
09-08-2025  08:39             2,948 cvs-brute.nse
09-08-2025  08:39             9,203 daap-get-library.nse
09-08-2025  08:39               578 daytime.nse
09-08-2025  08:39            14,353 db2-das-info.nse
09-08-2025  08:39             4,398 deluge-rpc-brute.nse
09-08-2025  08:39             8,462 dhcp-discover.nse
09-08-2025  08:39             2,275 dicom-brute.nse
09-08-2025  08:39             2,543 dicom-ping.nse
09-08-2025  08:39             2,499 dict-info.nse
09-08-2025  08:39             3,519 distcc-cve2004-2687.nse
09-08-2025  08:39             5,329 dns-blacklist.nse
09-08-2025  08:39            10,100 dns-brute.nse
09-08-2025  08:39             6,639 dns-cache-snoop.nse
09-08-2025  08:39            15,152 dns-check-zone.nse
09-08-2025  08:39            14,826 dns-client-subnet-scan.nse
09-08-2025  08:39            10,168 dns-fuzz.nse
09-08-2025  08:39             3,803 dns-ip6-arpa-scan.nse
09-08-2025  08:39            10,580 dns-nsec-enum.nse
09-08-2025  08:39            12,702 dns-nsec3-enum.nse
09-08-2025  08:39             3,441 dns-nsid.nse
09-08-2025  08:39             4,364 dns-random-srcport.nse
09-08-2025  08:39             4,363 dns-random-txid.nse
09-08-2025  08:39             1,456 dns-recursion.nse
09-08-2025  08:39             2,167 dns-service-discovery.nse
09-08-2025  08:39             5,679 dns-srv-enum.nse
09-08-2025  08:39             5,765 dns-update.nse
09-08-2025  08:39             2,123 dns-zeustracker.nse
09-08-2025  08:39            24,731 dns-zone-transfer.nse
09-08-2025  08:39             1,271 docker-version.nse
09-08-2025  08:39             3,865 domcon-brute.nse
09-08-2025  08:39             4,539 domcon-cmd.nse
09-08-2025  08:39             4,205 domino-enum-users.nse
09-08-2025  08:39             2,835 dpap-brute.nse
09-08-2025  08:39             5,805 drda-brute.nse
09-08-2025  08:39             3,796 drda-info.nse
09-08-2025  08:39             7,477 duplicates.nse
09-08-2025  08:39             5,693 eap-info.nse
09-08-2025  08:39            57,869 enip-info.nse
09-08-2025  08:39             1,716 epmd-info.nse
09-08-2025  08:39             2,564 eppc-enum-processes.nse
09-08-2025  08:39             3,910 fcrdns.nse
09-08-2025  08:39             1,083 finger.nse
09-08-2025  08:39             4,183 fingerprint-strings.nse
09-08-2025  08:39            29,093 firewalk.nse
09-08-2025  08:39             8,865 firewall-bypass.nse
09-08-2025  08:39            10,811 flume-master-info.nse
09-08-2025  08:39             3,796 fox-info.nse
09-08-2025  08:39             3,806 freelancer-info.nse
09-08-2025  08:39             4,530 ftp-anon.nse
09-08-2025  08:39             3,253 ftp-bounce.nse
09-08-2025  08:39             3,108 ftp-brute.nse
09-08-2025  08:39             3,272 ftp-libopie.nse
09-08-2025  08:39             3,290 ftp-proftpd-backdoor.nse
09-08-2025  08:39             3,768 ftp-syst.nse
09-08-2025  08:39             6,021 ftp-vsftpd-backdoor.nse
09-08-2025  08:39             5,923 ftp-vuln-cve2010-4221.nse
09-08-2025  08:39             7,919 ganglia-info.nse
09-08-2025  08:39             1,859 giop-info.nse
09-08-2025  08:39             6,850 gkrellm-info.nse
09-08-2025  08:39             2,342 gopher-ls.nse
09-08-2025  08:39             2,618 gpsd-info.nse
09-08-2025  08:39             1,927 hadoop-datanode-info.nse
09-08-2025  08:39             7,033 hadoop-jobtracker-info.nse
09-08-2025  08:39             6,697 hadoop-namenode-info.nse
09-08-2025  08:39             4,514 hadoop-secondary-namenode-info.nse
09-08-2025  08:39             2,955 hadoop-tasktracker-info.nse
09-08-2025  08:39            10,904 hartip-info.nse
09-08-2025  08:39             5,483 hbase-master-info.nse
09-08-2025  08:39             3,645 hbase-region-info.nse
09-08-2025  08:39             1,853 hddtemp-info.nse
09-08-2025  08:39             4,424 hnap-info.nse
09-08-2025  08:39             3,798 hostmap-bfk.nse
09-08-2025  08:39             4,933 hostmap-crtsh.nse
09-08-2025  08:39             2,100 hostmap-robtex.nse
09-08-2025  08:39             2,153 http-adobe-coldfusion-apsa1301.nse
09-08-2025  08:39             5,149 http-affiliate-id.nse
09-08-2025  08:39             1,950 http-apache-negotiation.nse
09-08-2025  08:39             4,499 http-apache-server-status.nse
09-08-2025  08:39             1,805 http-aspnet-debug.nse
09-08-2025  08:39             3,959 http-auth-finder.nse
09-08-2025  08:39             3,187 http-auth.nse
09-08-2025  08:39             2,865 http-avaya-ipoffice-users.nse
09-08-2025  08:39             4,372 http-awstatstotals-exec.nse
09-08-2025  08:39             6,872 http-axis2-dir-traversal.nse
09-08-2025  08:39             5,484 http-backup-finder.nse
09-08-2025  08:39             6,387 http-barracuda-dir-traversal.nse
09-08-2025  08:39             2,038 http-bigip-cookie.nse
09-08-2025  08:39             4,920 http-brute.nse
09-08-2025  08:39             4,436 http-cakephp-version.nse
09-08-2025  08:39             4,927 http-chrono.nse
09-08-2025  08:39             1,695 http-cisco-anyconnect.nse
09-08-2025  08:39             5,520 http-coldfusion-subzero.nse
09-08-2025  08:39             4,150 http-comments-displayer.nse
09-08-2025  08:39             7,251 http-config-backup.nse
09-08-2025  08:39             5,139 http-cookie-flags.nse
09-08-2025  08:39             2,577 http-cors.nse
09-08-2025  08:39            13,803 http-cross-domain-policy.nse
09-08-2025  08:39             5,418 http-csrf.nse
09-08-2025  08:39             1,718 http-date.nse
09-08-2025  08:39            17,388 http-default-accounts.nse
09-08-2025  08:39             4,288 http-devframework.nse
09-08-2025  08:39             2,529 http-dlink-backdoor.nse
09-08-2025  08:39             4,452 http-dombased-xss.nse
09-08-2025  08:39            13,893 http-domino-enum-passwords.nse
09-08-2025  08:39             2,256 http-drupal-enum-users.nse
09-08-2025  08:39             6,931 http-drupal-enum.nse
09-08-2025  08:39            20,667 http-enum.nse
09-08-2025  08:39             3,347 http-errors.nse
09-08-2025  08:39            20,413 http-exif-spider.nse
09-08-2025  08:39             5,199 http-favicon.nse
09-08-2025  08:39             4,451 http-feed.nse
09-08-2025  08:39             9,076 http-fetch.nse
09-08-2025  08:39            11,327 http-fileupload-exploiter.nse
09-08-2025  08:39            21,101 http-form-brute.nse
09-08-2025  08:39             7,934 http-form-fuzzer.nse
09-08-2025  08:39             2,739 http-frontpage-login.nse
09-08-2025  08:39             2,164 http-generator.nse
09-08-2025  08:39            12,100 http-git.nse
09-08-2025  08:39             3,195 http-gitweb-projects-enum.nse
09-08-2025  08:39             3,381 http-google-malware.nse
09-08-2025  08:39            11,692 http-grep.nse
09-08-2025  08:39             1,797 http-headers.nse
09-08-2025  08:39             3,383 http-hp-ilo-info.nse
09-08-2025  08:39             6,973 http-huawei-hg5xx-vuln.nse
09-08-2025  08:39             2,801 http-icloud-findmyiphone.nse
09-08-2025  08:39             4,085 http-icloud-sendmsg.nse
09-08-2025  08:39             6,073 http-iis-short-name-brute.nse
09-08-2025  08:39             7,921 http-iis-webdav-vuln.nse
09-08-2025  08:39             2,540 http-internal-ip-disclosure.nse
09-08-2025  08:39             5,422 http-joomla-brute.nse
09-08-2025  08:39             5,479 http-jsonp-detection.nse
09-08-2025  08:39             2,649 http-litespeed-sourcecode-download.nse
09-08-2025  08:39             6,120 http-ls.nse
09-08-2025  08:39             3,269 http-majordomo2-dir-traversal.nse
09-08-2025  08:39             2,833 http-malware-host.nse
09-08-2025  08:39             3,704 http-mcmp.nse
09-08-2025  08:39             6,895 http-method-tamper.nse
09-08-2025  08:39             7,320 http-methods.nse
09-08-2025  08:39             2,726 http-mobileversion-checker.nse
09-08-2025  08:39             4,461 http-ntlm-info.nse
09-08-2025  08:39             8,269 http-open-proxy.nse
09-08-2025  08:39             4,756 http-open-redirect.nse
09-08-2025  08:39             7,023 http-passwd.nse
09-08-2025  08:39             7,070 http-php-version.nse
09-08-2025  08:39             6,225 http-phpmyadmin-dir-traversal.nse
09-08-2025  08:39             5,822 http-phpself-xss.nse
09-08-2025  08:39             3,487 http-proxy-brute.nse
09-08-2025  08:39             1,930 http-put.nse
09-08-2025  08:39             3,591 http-qnap-nas-info.nse
09-08-2025  08:39             2,175 http-referer-checker.nse
09-08-2025  08:39             9,599 http-rfi-spider.nse
09-08-2025  08:39             2,737 http-robots.txt.nse
09-08-2025  08:39             2,305 http-robtex-reverse-ip.nse
09-08-2025  08:39             2,776 http-robtex-shared-ns.nse
09-08-2025  08:39             5,034 http-sap-netweaver-leak.nse
09-08-2025  08:39            15,956 http-security-headers.nse
09-08-2025  08:39             3,283 http-server-header.nse
09-08-2025  08:39             5,489 http-shellshock.nse
09-08-2025  08:39             5,344 http-sitemap-generator.nse
09-08-2025  08:39             5,464 http-slowloris-check.nse
09-08-2025  08:39            11,167 http-slowloris.nse
09-08-2025  08:39             9,404 http-sql-injection.nse
09-08-2025  08:39             8,451 http-stored-xss.nse
09-08-2025  08:39             4,018 http-svn-enum.nse
09-08-2025  08:39             4,360 http-svn-info.nse
09-08-2025  08:39             2,317 http-title.nse
09-08-2025  08:39             6,026 http-tplink-dir-traversal.nse
09-08-2025  08:39             1,947 http-trace.nse
09-08-2025  08:39             5,294 http-traceroute.nse
09-08-2025  08:39             6,437 http-trane-info.nse
09-08-2025  08:39             5,549 http-unsafe-output-escaping.nse
09-08-2025  08:39             5,403 http-useragent-tester.nse
09-08-2025  08:39             4,550 http-userdir-enum.nse
09-08-2025  08:39             5,785 http-vhosts.nse
09-08-2025  08:39            10,770 http-virustotal.nse
09-08-2025  08:39             2,078 http-vlcstreamer-ls.nse
09-08-2025  08:39             4,111 http-vmware-path-vuln.nse
09-08-2025  08:39             3,273 http-vuln-cve2006-3392.nse
09-08-2025  08:39             6,610 http-vuln-cve2009-3960.nse
09-08-2025  08:39             2,957 http-vuln-cve2010-0738.nse
09-08-2025  08:39             5,607 http-vuln-cve2010-2861.nse
09-08-2025  08:39             4,527 http-vuln-cve2011-3192.nse
09-08-2025  08:39             5,851 http-vuln-cve2011-3368.nse
09-08-2025  08:39             4,403 http-vuln-cve2012-1823.nse
09-08-2025  08:39             4,831 http-vuln-cve2013-0156.nse
09-08-2025  08:39             2,853 http-vuln-cve2013-6786.nse
09-08-2025  08:39             5,009 http-vuln-cve2013-7091.nse
09-08-2025  08:39             2,974 http-vuln-cve2014-2126.nse
09-08-2025  08:39             3,363 http-vuln-cve2014-2127.nse
09-08-2025  08:39             3,222 http-vuln-cve2014-2128.nse
09-08-2025  08:39             3,008 http-vuln-cve2014-2129.nse
09-08-2025  08:39            14,018 http-vuln-cve2014-3704.nse
09-08-2025  08:39             4,523 http-vuln-cve2014-8877.nse
09-08-2025  08:39             7,774 http-vuln-cve2015-1427.nse
09-08-2025  08:39             3,443 http-vuln-cve2015-1635.nse
09-08-2025  08:39             4,372 http-vuln-cve2017-1001000.nse
09-08-2025  08:39             2,594 http-vuln-cve2017-5638.nse
09-08-2025  08:39             5,480 http-vuln-cve2017-5689.nse
09-08-2025  08:39             5,187 http-vuln-cve2017-8917.nse
09-08-2025  08:39             2,699 http-vuln-misfortune-cookie.nse
09-08-2025  08:39             4,225 http-vuln-wnr1000-creds.nse
09-08-2025  08:39             5,422 http-waf-detect.nse
09-08-2025  08:39            19,339 http-waf-fingerprint.nse
09-08-2025  08:39             5,806 http-webdav-scan.nse
09-08-2025  08:39             5,061 http-wordpress-brute.nse
09-08-2025  08:39            10,866 http-wordpress-enum.nse
09-08-2025  08:39             4,641 http-wordpress-users.nse
09-08-2025  08:39             2,653 http-xssed.nse
09-08-2025  08:39             2,528 https-redirect.nse
09-08-2025  08:39             2,133 iax2-brute.nse
09-08-2025  08:39             1,377 iax2-version.nse
09-08-2025  08:39             3,462 icap-info.nse
09-08-2025  08:39             4,343 iec-identify.nse
09-08-2025  08:39            12,333 iec61850-mms.nse
09-08-2025  08:39             5,107 ike-version.nse
09-08-2025  08:39             4,441 imap-brute.nse
09-08-2025  08:39             1,515 imap-capabilities.nse
09-08-2025  08:39             5,366 imap-ntlm-info.nse
09-08-2025  08:39             6,494 impress-remote-discover.nse
09-08-2025  08:39             2,935 informix-brute.nse
09-08-2025  08:39             3,414 informix-query.nse
09-08-2025  08:39             4,548 informix-tables.nse
09-08-2025  08:39             3,420 ip-forwarding.nse
09-08-2025  08:39             2,101 ip-geolocation-geoplugin.nse
09-08-2025  08:39             2,939 ip-geolocation-ipinfodb.nse
09-08-2025  08:39             6,025 ip-geolocation-map-bing.nse
09-08-2025  08:39             6,003 ip-geolocation-map-google.nse
09-08-2025  08:39             2,343 ip-geolocation-map-kml.nse
09-08-2025  08:39            23,366 ip-geolocation-maxmind.nse
09-08-2025  08:39             2,437 ip-https-discover.nse
09-08-2025  08:39             5,567 ipidseq.nse
09-08-2025  08:39             3,425 ipmi-brute.nse
09-08-2025  08:39             3,161 ipmi-cipher-zero.nse
09-08-2025  08:39             3,745 ipmi-version.nse
09-08-2025  08:39            16,113 ipv6-multicast-mld-list.nse
09-08-2025  08:39             8,388 ipv6-node-info.nse
09-08-2025  08:39             6,077 ipv6-ra-flood.nse
09-08-2025  08:39             6,946 irc-botnet-channels.nse
09-08-2025  08:39             3,574 irc-brute.nse
09-08-2025  08:39             4,507 irc-info.nse
09-08-2025  08:39             6,361 irc-sasl-brute.nse
09-08-2025  08:39             8,480 irc-unrealircd-backdoor.nse
09-08-2025  08:39             2,390 iscsi-brute.nse
09-08-2025  08:39             3,117 iscsi-info.nse
09-08-2025  08:39             1,952 isns-info.nse
09-08-2025  08:39             3,330 jdwp-exec.nse
09-08-2025  08:39             3,116 jdwp-info.nse
09-08-2025  08:39             3,048 jdwp-inject.nse
09-08-2025  08:39             2,330 jdwp-version.nse
09-08-2025  08:39            10,621 knx-gateway-discover.nse
09-08-2025  08:39             5,565 knx-gateway-info.nse
09-08-2025  08:39            13,235 krb5-enum-users.nse
09-08-2025  08:39            14,051 ldap-brute.nse
09-08-2025  08:39             4,995 ldap-novell-getpass.nse
09-08-2025  08:39             9,414 ldap-rootdse.nse
09-08-2025  08:39            12,435 ldap-search.nse
09-08-2025  08:39             2,546 lexmark-config.nse
09-08-2025  08:39             6,741 llmnr-resolve.nse
09-08-2025  08:39             9,032 lltd-discovery.nse
09-08-2025  08:39             7,598 lu-enum.nse
09-08-2025  08:39             6,423 maxdb-info.nse
09-08-2025  08:39             2,635 mcafee-epo-agent.nse
09-08-2025  08:39             2,884 membase-brute.nse
09-08-2025  08:39             4,900 membase-http-info.nse
09-08-2025  08:39             5,657 memcached-info.nse
09-08-2025  08:39            10,089 metasploit-info.nse
09-08-2025  08:39             2,952 metasploit-msgrpc-brute.nse
09-08-2025  08:39             3,199 metasploit-xmlrpc-brute.nse
09-08-2025  08:39             3,090 mikrotik-routeros-brute.nse
09-08-2025  08:39             4,161 mikrotik-routeros-username-brute.nse
09-08-2025  08:39             5,994 mikrotik-routeros-version.nse
09-08-2025  08:39             3,264 mmouse-brute.nse
09-08-2025  08:39             5,686 mmouse-exec.nse
09-08-2025  08:39             5,996 modbus-discover.nse
09-08-2025  08:39             2,588 mongodb-brute.nse
09-08-2025  08:39             2,593 mongodb-databases.nse
09-08-2025  08:39             3,673 mongodb-info.nse
09-08-2025  08:39            15,063 mqtt-subscribe.nse
09-08-2025  08:39             9,254 mrinfo.nse
09-08-2025  08:39            11,619 ms-sql-brute.nse
09-08-2025  08:39             5,498 ms-sql-config.nse
09-08-2025  08:39             2,631 ms-sql-dac.nse
09-08-2025  08:39             3,580 ms-sql-dump-hashes.nse
09-08-2025  08:39             6,563 ms-sql-empty-password.nse
09-08-2025  08:39             5,378 ms-sql-hasdbaccess.nse
09-08-2025  08:39             9,782 ms-sql-info.nse
09-08-2025  08:39             4,051 ms-sql-ntlm-info.nse
09-08-2025  08:39             4,221 ms-sql-query.nse
09-08-2025  08:39             8,936 ms-sql-tables.nse
09-08-2025  08:39             5,899 ms-sql-xp-cmdshell.nse
09-08-2025  08:39             3,235 msrpc-enum.nse
09-08-2025  08:39            12,120 mtrace.nse
09-08-2025  08:39            10,124 multicast-profinet-discovery.nse
09-08-2025  08:39             3,424 murmur-version.nse
09-08-2025  08:39             6,688 mysql-audit.nse
09-08-2025  08:39             2,977 mysql-brute.nse
09-08-2025  08:39             2,945 mysql-databases.nse
09-08-2025  08:39             3,263 mysql-dump-hashes.nse
09-08-2025  08:39             2,020 mysql-empty-password.nse
09-08-2025  08:39             3,413 mysql-enum.nse
09-08-2025  08:39             3,455 mysql-info.nse
09-08-2025  08:39             3,714 mysql-query.nse
09-08-2025  08:39             2,811 mysql-users.nse
09-08-2025  08:39             3,265 mysql-variables.nse
09-08-2025  08:39             6,977 mysql-vuln-cve2012-2122.nse
09-08-2025  08:39             1,257 nat-pmp-info.nse
09-08-2025  08:39             4,520 nat-pmp-mapport.nse
09-08-2025  08:39             5,387 nbd-info.nse
09-08-2025  08:39             1,997 nbns-interfaces.nse
09-08-2025  08:39             7,718 nbstat.nse
09-08-2025  08:39             1,341 ncp-enum-users.nse
09-08-2025  08:39             1,259 ncp-serverinfo.nse
09-08-2025  08:39             2,323 ndmp-fs-info.nse
09-08-2025  08:39             2,307 ndmp-version.nse
09-08-2025  08:39             4,562 nessus-brute.nse
09-08-2025  08:39             4,100 nessus-xmlrpc-brute.nse
09-08-2025  08:39             1,830 netbus-auth-bypass.nse
09-08-2025  08:39             1,677 netbus-brute.nse
09-08-2025  08:39             5,690 netbus-info.nse
09-08-2025  08:39             1,179 netbus-version.nse
09-08-2025  08:39             2,734 nexpose-brute.nse
09-08-2025  08:39            14,534 nfs-ls.nse
09-08-2025  08:39             2,714 nfs-showmount.nse
09-08-2025  08:39             9,947 nfs-statfs.nse
09-08-2025  08:39             6,422 nje-node-brute.nse
09-08-2025  08:39             6,139 nje-pass-brute.nse
09-08-2025  08:39             5,119 nntp-ntlm-info.nse
09-08-2025  08:39             4,098 nping-brute.nse
09-08-2025  08:39             7,689 nrpe-enum.nse
09-08-2025  08:39             6,098 ntp-info.nse
09-08-2025  08:39            32,773 ntp-monlist.nse
09-08-2025  08:39             2,180 omp2-brute.nse
09-08-2025  08:39             3,320 omp2-enum-targets.nse
09-08-2025  08:39             6,805 omron-info.nse
09-08-2025  08:39             6,594 openflow-info.nse
09-08-2025  08:39             5,243 openlookup-info.nse
09-08-2025  08:39             3,172 openvas-otp-brute.nse
09-08-2025  08:39             7,077 openwebnet-discovery.nse
09-08-2025  08:39             6,733 oracle-brute-stealth.nse
09-08-2025  08:39             7,416 oracle-brute.nse
09-08-2025  08:39             3,951 oracle-enum-users.nse
09-08-2025  08:39             4,821 oracle-sid-brute.nse
09-08-2025  08:39             3,167 oracle-tns-version.nse
09-08-2025  08:39             3,021 ovs-agent-version.nse
09-08-2025  08:39            22,474 p2p-conficker.nse
09-08-2025  08:39            10,157 path-mtu.nse
09-08-2025  08:39             5,317 pcanywhere-brute.nse
09-08-2025  08:39             3,563 pcworx-info.nse
09-08-2025  08:39             5,378 pgsql-brute.nse
09-08-2025  08:39             3,042 pjl-ready-message.nse
09-08-2025  08:39             4,047 pop3-brute.nse
09-08-2025  08:39             1,397 pop3-capabilities.nse
09-08-2025  08:39             4,941 pop3-ntlm-info.nse
09-08-2025  08:39             4,393 port-states.nse
09-08-2025  08:39             3,328 pptp-version.nse
09-08-2025  08:39             5,603 profinet-cm-lookup.nse
09-08-2025  08:39             8,712 puppet-naivesigning.nse
09-08-2025  08:39             4,326 qconn-exec.nse
09-08-2025  08:39            14,597 qscan.nse
09-08-2025  08:39            11,070 quake1-info.nse
09-08-2025  08:39             6,732 quake3-info.nse
09-08-2025  08:39             7,274 quake3-master-getservers.nse
09-08-2025  08:39             5,961 rdp-enum-encryption.nse
09-08-2025  08:39             5,791 rdp-ntlm-info.nse
09-08-2025  08:39             9,425 rdp-vuln-ms12-020.nse
09-08-2025  08:39             3,264 realvnc-auth-bypass.nse
09-08-2025  08:39             2,795 redis-brute.nse
09-08-2025  08:39             7,004 redis-info.nse
09-08-2025  08:39             4,846 resolveall.nse
09-08-2025  08:39             3,554 reverse-index.nse
09-08-2025  08:39             3,128 rexec-brute.nse
09-08-2025  08:39             1,884 rfc868-time.nse
09-08-2025  08:39             5,564 riak-http-info.nse
09-08-2025  08:39             4,865 rlogin-brute.nse
09-08-2025  08:39            10,621 rmi-dumpregistry.nse
09-08-2025  08:39             4,011 rmi-vuln-classloader.nse
09-08-2025  08:39             8,869 rpc-grind.nse
09-08-2025  08:39             2,140 rpcap-brute.nse
09-08-2025  08:39             2,654 rpcap-info.nse
09-08-2025  08:39             4,601 rpcinfo.nse
09-08-2025  08:39             6,528 rsa-vuln-roca.nse
09-08-2025  08:39             3,132 rsync-brute.nse
09-08-2025  08:39             1,216 rsync-list-modules.nse
09-08-2025  08:39             1,479 rtsp-methods.nse
09-08-2025  08:39             5,739 rtsp-url-brute.nse
09-08-2025  08:39             5,528 rusers.nse
09-08-2025  08:39            10,287 s7-info.nse
09-08-2025  08:39             4,148 samba-vuln-cve-2012-1182.nse
09-08-2025  08:39            52,837 script.db
09-08-2025  08:39             8,733 servicetags.nse
09-08-2025  08:39             6,573 shodan-api.nse
09-08-2025  08:39             3,627 sip-brute.nse
09-08-2025  08:39             6,099 sip-call-spoof.nse
09-08-2025  08:39             8,585 sip-enum-users.nse
09-08-2025  08:39             1,652 sip-methods.nse
09-08-2025  08:39             2,164 skypev2-version.nse
09-08-2025  08:39            45,061 smb-brute.nse
09-08-2025  08:39             5,289 smb-double-pulsar-backdoor.nse
09-08-2025  08:39             4,840 smb-enum-domains.nse
09-08-2025  08:39             5,971 smb-enum-groups.nse
09-08-2025  08:39             8,043 smb-enum-processes.nse
09-08-2025  08:39            27,274 smb-enum-services.nse
09-08-2025  08:39            12,017 smb-enum-sessions.nse
09-08-2025  08:39             6,923 smb-enum-shares.nse
09-08-2025  08:39            12,527 smb-enum-users.nse
09-08-2025  08:39             4,418 smb-flood.nse
09-08-2025  08:39             7,471 smb-ls.nse
09-08-2025  08:39             8,758 smb-mbenum.nse
09-08-2025  08:39             8,220 smb-os-discovery.nse
09-08-2025  08:39             4,982 smb-print-text.nse
09-08-2025  08:39             1,833 smb-protocols.nse
09-08-2025  08:39            63,596 smb-psexec.nse
09-08-2025  08:39             5,190 smb-security-mode.nse
09-08-2025  08:39             2,424 smb-server-stats.nse
09-08-2025  08:39            14,159 smb-system-info.nse
09-08-2025  08:39             7,524 smb-vuln-conficker.nse
09-08-2025  08:39            23,154 smb-vuln-cve-2017-7494.nse
09-08-2025  08:39             6,402 smb-vuln-cve2009-3103.nse
09-08-2025  08:39             6,545 smb-vuln-ms06-025.nse
09-08-2025  08:39             5,386 smb-vuln-ms07-029.nse
09-08-2025  08:39             5,688 smb-vuln-ms08-067.nse
09-08-2025  08:39             5,647 smb-vuln-ms10-054.nse
09-08-2025  08:39             7,214 smb-vuln-ms10-061.nse
09-08-2025  08:39             7,344 smb-vuln-ms17-010.nse
09-08-2025  08:39             4,400 smb-vuln-regsvc-dos.nse
09-08-2025  08:39             6,586 smb-vuln-webexec.nse
09-08-2025  08:39             5,084 smb-webexec-exploit.nse
09-08-2025  08:39             3,753 smb2-capabilities.nse
09-08-2025  08:39             2,689 smb2-security-mode.nse
09-08-2025  08:39             1,408 smb2-time.nse
09-08-2025  08:39             5,269 smb2-vuln-uptime.nse
09-08-2025  08:39             4,309 smtp-brute.nse
09-08-2025  08:39             4,957 smtp-commands.nse
09-08-2025  08:39            12,006 smtp-enum-users.nse
09-08-2025  08:39             5,915 smtp-ntlm-info.nse
09-08-2025  08:39            10,148 smtp-open-relay.nse
09-08-2025  08:39               716 smtp-strangeport.nse
09-08-2025  08:39            14,781 smtp-vuln-cve2010-4344.nse
09-08-2025  08:39             7,719 smtp-vuln-cve2011-1720.nse
09-08-2025  08:39             7,603 smtp-vuln-cve2011-1764.nse
09-08-2025  08:39             4,327 sniffer-detect.nse
09-08-2025  08:39             7,816 snmp-brute.nse
09-08-2025  08:39             4,388 snmp-hh3c-logins.nse
09-08-2025  08:39             5,216 snmp-info.nse
09-08-2025  08:39            28,644 snmp-interfaces.nse
09-08-2025  08:39             5,978 snmp-ios-config.nse
09-08-2025  08:39             4,156 snmp-netstat.nse
09-08-2025  08:39             4,431 snmp-processes.nse
09-08-2025  08:39             1,857 snmp-sysdescr.nse
09-08-2025  08:39             2,570 snmp-win32-services.nse
09-08-2025  08:39             2,739 snmp-win32-shares.nse
09-08-2025  08:39             4,713 snmp-win32-software.nse
09-08-2025  08:39             2,016 snmp-win32-users.nse
09-08-2025  08:39             1,753 socks-auth-info.nse
09-08-2025  08:39             2,521 socks-brute.nse
09-08-2025  08:39             6,527 socks-open-proxy.nse
09-08-2025  08:39             1,665 ssh-auth-methods.nse
09-08-2025  08:39             2,881 ssh-brute.nse
09-08-2025  08:39            16,036 ssh-hostkey.nse
09-08-2025  08:39             6,165 ssh-publickey-acceptance.nse
09-08-2025  08:39             3,817 ssh-run.nse
09-08-2025  08:39             5,391 ssh2-enum-algos.nse
09-08-2025  08:39             1,423 sshv1.nse
09-08-2025  08:39            10,142 ssl-ccs-injection.nse
09-08-2025  08:39             3,900 ssl-cert-intaddr.nse
09-08-2025  08:39            13,175 ssl-cert.nse
09-08-2025  08:39             6,836 ssl-date.nse
09-08-2025  08:39            39,926 ssl-dh-params.nse
09-08-2025  08:39            40,040 ssl-enum-ciphers.nse
09-08-2025  08:39             7,797 ssl-heartbleed.nse
09-08-2025  08:39             4,457 ssl-known-key.nse
09-08-2025  08:39            11,230 ssl-poodle.nse
09-08-2025  08:39            11,278 sslv2-drown.nse
09-08-2025  08:39             1,604 sslv2.nse
09-08-2025  08:39             2,325 sstp-discover.nse
09-08-2025  08:39             1,188 stun-info.nse
09-08-2025  08:39             1,141 stun-version.nse
09-08-2025  08:39             3,393 stuxnet-detect.nse
09-08-2025  08:39             3,737 supermicro-ipmi-conf.nse
09-08-2025  08:39             7,528 svn-brute.nse
09-08-2025  08:39             2,923 targets-asn.nse
09-08-2025  08:39             3,463 targets-ipv6-eui64.nse
09-08-2025  08:39             7,536 targets-ipv6-map4to6.nse
09-08-2025  08:39             4,405 targets-ipv6-multicast-echo.nse
09-08-2025  08:39             5,693 targets-ipv6-multicast-invalid-dst.nse
09-08-2025  08:39             4,173 targets-ipv6-multicast-mld.nse
09-08-2025  08:39             8,591 targets-ipv6-multicast-slaac.nse
09-08-2025  08:39             9,268 targets-ipv6-wordlist.nse
09-08-2025  08:39             4,902 targets-sniffer.nse
09-08-2025  08:39             1,822 targets-traceroute.nse
09-08-2025  08:39             3,596 targets-xml.nse
09-08-2025  08:39             2,489 teamspeak2-version.nse
09-08-2025  08:39            20,262 telnet-brute.nse
09-08-2025  08:39             3,008 telnet-encryption.nse
09-08-2025  08:39             4,564 telnet-ntlm-info.nse
09-08-2025  08:39             5,736 tftp-enum.nse
09-08-2025  08:39            10,034 tftp-version.nse
09-08-2025  08:39             6,187 tls-alpn.nse
09-08-2025  08:39             4,203 tls-nextprotoneg.nse
09-08-2025  08:39            11,773 tls-ticketbleed.nse
09-08-2025  08:39             4,118 tn3270-screen.nse
09-08-2025  08:39             3,832 tor-consensus-checker.nse
09-08-2025  08:39             5,954 traceroute-geolocation.nse
09-08-2025  08:39            13,692 tso-brute.nse
09-08-2025  08:39            10,304 tso-enum.nse
09-08-2025  08:39            10,107 ubiquiti-discovery.nse
09-08-2025  08:39               895 unittest.nse
09-08-2025  08:39             3,836 unusual-port.nse
09-08-2025  08:39             1,669 upnp-info.nse
09-08-2025  08:39             3,125 uptime-agent-info.nse
09-08-2025  08:39             4,296 url-snarf.nse
09-08-2025  08:39            25,403 ventrilo-info.nse
09-08-2025  08:39             3,190 versant-info.nse
09-08-2025  08:39             3,367 vmauthd-brute.nse
09-08-2025  08:39             3,013 vmware-version.nse
09-08-2025  08:39             4,217 vnc-brute.nse
09-08-2025  08:39             4,348 vnc-info.nse
09-08-2025  08:39             3,039 vnc-title.nse
09-08-2025  08:39             5,559 voldemort-info.nse
09-08-2025  08:39            10,409 vtam-enum.nse
09-08-2025  08:39             7,077 vulners.nse
09-08-2025  08:39             2,553 vuze-dht-info.nse
09-08-2025  08:39             7,789 wdb-version.nse
09-08-2025  08:39             3,589 weblogic-t3-info.nse
09-08-2025  08:39             4,203 whois-domain.nse
09-08-2025  08:39            89,578 whois-ip.nse
09-08-2025  08:39             2,629 wsdd-discover.nse
09-08-2025  08:39             2,286 x11-access.nse
09-08-2025  08:39             2,095 xdmcp-discover.nse
09-08-2025  08:39             4,362 xmlrpc-methods.nse
09-08-2025  08:39             4,316 xmpp-brute.nse
09-08-2025  08:39            17,285 xmpp-info.nse
             613 File(s)      3,897,701 bytes
               2 Dir(s)  24,234,340,352 bytes free

### Script Example: Domain WHOIS Lookup
```bash
nmap --script=whois-domain.nse testphp.vulnweb.com
```

**Script Output Analysis:**
|
| Domain name record found at whois.verisign-grs.com
| No match for "TESTPHP.VULNWEB.COM".\x0D
| >>> Last update of whois database: 2025-09-25T04:45:07Z <<<\x0D
| \x0D
| NOTICE: The expiration date displayed in this record is the date the\x0D
| registrar's sponsorship of the domain name registration in the registry is\x0D
| currently set to expire. This date does not necessarily reflect the expiration\x0D
| date of the domain name registrant's agreement with the sponsoring\x0D
| registrar.  Users may consult the sponsoring registrar's Whois database to\x0D
| view the registrar's reported date of expiration for this registration.\x0D
| \x0D
| TERMS OF USE: You are not authorized to access or query our Whois\x0D
| database through the use of electronic processes that are high-volume and\x0D
| automated except as reasonably necessary to register domain names or\x0D
| modify existing registrations; the Data in VeriSign Global Registry\x0D
| Services' ("VeriSign") Whois database is provided by VeriSign for\x0D
| information purposes only, and to assist persons in obtaining information\x0D
| about or related to a domain name registration record. VeriSign does not\x0D
| guarantee its accuracy. By submitting a Whois query, you agree to abide\x0D
| by the following terms of use: You agree that you may use this Data only\x0D
| for lawful purposes and that under no circumstances will you use this Data\x0D
| to: (1) allow, enable, or otherwise support the transmission of mass\x0D
| unsolicited, commercial advertising or solicitations via e-mail, telephone,\x0D
| or facsimile; or (2) enable high volume, automated, electronic processes\x0D
| that apply to VeriSign (or its computer systems). The compilation,\x0D
| repackaging, dissemination or other use of this Data is expressly\x0D
| prohibited without the prior written consent of VeriSign. You agree not to\x0D
| use electronic processes that are automated and high-volume to access or\x0D
| query the Whois database except as reasonably necessary to register\x0D
| domain names or modify existing registrations. VeriSign reserves the right\x0D
| to restrict your access to the Whois database in its sole discretion to ensure\x0D
| operational stability.  VeriSign may restrict or terminate your access to the\x0D
| Whois database for failure to abide by these terms of use. VeriSign\x0D
| reserves the right to modify these terms at any time.\x0D
| \x0D
| The Registry database contains ONLY .COM, .NET, .EDU domains and\x0D
|_Registrars.\x0D

Nmap done: 1 IP address (1 host up) scanned in 23.73 seconds

C:\Program Files (x86)\Nmap\scripts>nmap --script=whois-domain.nse radiumonline.in
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:15 +0530
Nmap scan report for radiumonline.in (3.110.211.57)
Host is up (0.042s latency).
rDNS record for 3.110.211.57: ec2-3-110-211-57.ap-south-1.compute.amazonaws.com
Not shown: 996 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3389/tcp open  ms-wbt-server

Host script results:
| whois-domain:
|
| Domain name record found at whois.nixiregistry.in
| Domain Name: radiumonline.in\x0D
| Registry Domain ID: D2C6524786A1E4CA1AE4928ECEF6E4302-IN\x0D
| Registrar WHOIS Server: whois.godaddy.com\x0D
| Registrar URL: www.godaddy.com\x0D
| Updated Date: 2025-05-31T02:26:38.748Z\x0D
| Creation Date: 2023-07-01T08:52:41.076Z\x0D
| Registry Expiry Date: 2033-07-01T08:52:41.076Z\x0D
| Registrar: GoDaddy\x0D
| Registrar IANA ID: 146\x0D
| Registrar Abuse Contact Email: reg_admin@godaddy.com\x0D
| Registrar Abuse Contact Phone: +1.4805058800\x0D
| Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited\x0D
| Domain Status: clientRenewProhibited https://icann.org/epp#clientRenewProhibited\x0D
| Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited\x0D
| Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited\x0D
| Registry Registrant ID: REDACTED FOR PRIVACY\x0D
| Registrant Name: REDACTED FOR PRIVACY\x0D
| Registrant Organization: \x0D
| Registrant Street: REDACTED FOR PRIVACY\x0D
| Registrant City: REDACTED FOR PRIVACY\x0D
| Registrant State/Province: Kerala\x0D
| Registrant Postal Code: REDACTED FOR PRIVACY\x0D
| Registrant Country: IN\x0D
| Registrant Phone: REDACTED FOR PRIVACY\x0D
| Registrant Fax: REDACTED FOR PRIVACY\x0D
| Registrant Email: Please query the RDDS service of the Registrar of Record identified in this output for information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.\x0D
| Registry Admin ID: REDACTED FOR PRIVACY\x0D
| Admin Name: REDACTED FOR PRIVACY\x0D
| Admin Organization: REDACTED FOR PRIVACY\x0D
| Admin Street: REDACTED FOR PRIVACY\x0D
| Admin City: REDACTED FOR PRIVACY\x0D
| Admin State/Province: REDACTED FOR PRIVACY\x0D
| Admin Postal Code: REDACTED FOR PRIVACY\x0D
| Admin Country: REDACTED FOR PRIVACY\x0D
| Admin Phone: REDACTED FOR PRIVACY\x0D
| Admin Fax: REDACTED FOR PRIVACY\x0D
| Admin Email: Please query the RDDS service of the Registrar of Record identified in this output for information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.\x0D
| Registry Tech ID: REDACTED FOR PRIVACY\x0D
| Tech Name: REDACTED FOR PRIVACY\x0D
| Tech Organization: REDACTED FOR PRIVACY\x0D
| Tech Street: REDACTED FOR PRIVACY\x0D
| Tech City: REDACTED FOR PRIVACY\x0D
| Tech State/Province: REDACTED FOR PRIVACY\x0D
| Tech Postal Code: REDACTED FOR PRIVACY\x0D
| Tech Country: REDACTED FOR PRIVACY\x0D
| Tech Phone: REDACTED FOR PRIVACY\x0D
| Tech Fax: REDACTED FOR PRIVACY\x0D
| Tech Email: Please query the RDDS service of the Registrar of Record identified in this output for information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.\x0D
| Registry Billing ID: REDACTED FOR PRIVACY\x0D
| Billing Name: REDACTED FOR PRIVACY\x0D
| Billing Organization: REDACTED FOR PRIVACY\x0D
| Billing Street: REDACTED FOR PRIVACY\x0D
| Billing City: REDACTED FOR PRIVACY\x0D
| Billing State/Province: REDACTED FOR PRIVACY\x0D
| Billing Postal Code: REDACTED FOR PRIVACY\x0D
| Billing Country: REDACTED FOR PRIVACY\x0D
| Billing Phone: REDACTED FOR PRIVACY\x0D
| Billing Fax: REDACTED FOR PRIVACY\x0D
| Billing Email: Please query the RDDS service of the Registrar of Record identified in this output for information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.\x0D
| Name Server: ns20.domaincontrol.com\x0D
| Name Server: ns19.domaincontrol.com\x0D
| DNSSEC: unsigned\x0D
| URL of the ICANN RDDS Inaccuracy Complaint Form: https://icann.org/wicf\x0D
| \x0D
| >>> Last update of WHOIS database: 2025-09-25T04:46:02.177Z <<<\x0D
| \x0D
| For more information on domain status codes, please visit https://icann.org/epp\x0D
| \x0D
| The WHOIS information provided in this page has been redacted\x0D
| in compliance with ICANN's Temporary Specification for gTLD\x0D
| Registration Data.\x0D
| \x0D
| The data in this record is provided by Tucows Registry for informational\x0D
| purposes only, and it does not guarantee its accuracy. Tucows Registry is\x0D
| authoritative for whois information in top-level domains it operates\x0D
| under contract with the Internet Corporation for Assigned Names and\x0D
| Numbers. Whois information from other top-level domains is provided by\x0D
| a third-party under license to Tucows Registry.\x0D
| \x0D
| This service is intended only for query-based access. By using this\x0D
| service, you agree that you will use any data presented only for lawful\x0D
| purposes and that, under no circumstances will you use (a) data\x0D
| acquired for the purpose of allowing, enabling, or otherwise supporting\x0D
| the transmission by e-mail, telephone, facsimile or other\x0D
| communications mechanism of mass  unsolicited, commercial advertising\x0D
| or solicitations to entities other than your existing  customers; or\x0D
| (b) this service to enable high volume, automated, electronic processes\x0D
| that send queries or data to the systems of any Registrar or any\x0D
| Registry except as reasonably necessary to register domain names or\x0D
| modify existing domain name registrations.\x0D
| \x0D
| Tucows Registry reserves the right to modify these terms at any time. By\x0D
| submitting this query, you agree to abide by this policy. All rights\x0D
|_reserved.\x0D

Nmap done: 1 IP address (1 host up) scanned in 12.36 seconds

C:\Program Files (x86)\Nmap\scripts>nmap --script=whois-ip.nse protosonline.in
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:17 +0530
Nmap scan report for protosonline.in (136.185.21.72)
Host is up (0.0020s latency).
rDNS record for 136.185.21.72: abts-tn-static-72.21.185.136.airtelbroadband.in
Not shown: 985 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
135/tcp  open  msrpc
443/tcp  open  https
445/tcp  open  microsoft-ds
2179/tcp open  vmrdp
4242/tcp open  vrml-multi-use
5001/tcp open  commplex-link
5222/tcp open  xmpp-client
7070/tcp open  realserver
7777/tcp open  cbt
7778/tcp open  interwise
8042/tcp open  fs-agent
8045/tcp open  unknown
8081/tcp open  blackice-icecap

Host script results:
| whois-ip: Record found at whois.apnic.net
| inetnum: 136.185.0.0 - 136.185.255.255
| netname: BHARTI-IN
| descr: Bharti Airtel Limited
| country: IN
| orgname: Bharti Airtel Limited
| organisation: ORG-BAL1-AP
| email: apnic@airtel.com
| role: ABUSE BHARTITELEMEDIAIN
| email: shankar.B@airtel.com
| person: Network Administrator
|_email: noc-dataprov@airtel.com

Nmap done: 1 IP address (1 host up) scanned in 12.21 seconds

C:\Program Files (x86)\Nmap\scripts>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.

C:\Program Files (x86)\Nmap\scripts>dir
 Volume in drive C has no label.
 Volume Serial Number is CEC7-9556

 Directory of C:\Program Files (x86)\Nmap\scripts

24-09-2025  16:40    <DIR>          .
24-09-2025  16:40    <DIR>          ..
09-08-2025  08:39             3,901 acarsd-info.nse
09-08-2025  08:39             8,749 address-info.nse
09-08-2025  08:39             3,345 afp-brute.nse
09-08-2025  08:39             6,463 afp-ls.nse
09-08-2025  08:39             7,001 afp-path-vuln.nse
09-08-2025  08:39             5,600 afp-serverinfo.nse
09-08-2025  08:39             2,621 afp-showmount.nse
09-08-2025  08:39             2,262 ajp-auth.nse
09-08-2025  08:39             2,983 ajp-brute.nse
09-08-2025  08:39             1,329 ajp-headers.nse
09-08-2025  08:39             2,590 ajp-methods.nse
09-08-2025  08:39             3,051 ajp-request.nse
09-08-2025  08:39             6,719 allseeingeye-info.nse
09-08-2025  08:39             1,678 amqp-info.nse
09-08-2025  08:39            15,024 asn-query.nse
09-08-2025  08:39             2,054 auth-owners.nse
09-08-2025  08:39               870 auth-spoof.nse
09-08-2025  08:39             9,050 backorifice-brute.nse
09-08-2025  08:39            10,193 backorifice-info.nse
09-08-2025  08:39            53,131 bacnet-info.nse
09-08-2025  08:39             6,136 banner.nse
09-08-2025  08:39             2,012 bitcoin-getaddr.nse
09-08-2025  08:39             1,812 bitcoin-info.nse
09-08-2025  08:39             4,437 bitcoinrpc-info.nse
09-08-2025  08:39             4,079 bittorrent-discovery.nse
09-08-2025  08:39             1,344 bjnp-discover.nse
09-08-2025  08:39             4,441 broadcast-ataoe-discover.nse
09-08-2025  08:39             2,964 broadcast-avahi-dos.nse
09-08-2025  08:39             4,740 broadcast-bjnp-discover.nse
09-08-2025  08:39             2,438 broadcast-db2-discover.nse
09-08-2025  08:39             9,256 broadcast-dhcp-discover.nse
09-08-2025  08:39             2,693 broadcast-dhcp6-discover.nse
09-08-2025  08:39             1,444 broadcast-dns-service-discovery.nse
09-08-2025  08:39             3,866 broadcast-dropbox-listener.nse
09-08-2025  08:39            11,696 broadcast-eigrp-discovery.nse
09-08-2025  08:39             3,472 broadcast-hid-discoveryd.nse
09-08-2025  08:39            14,081 broadcast-igmp-discovery.nse
09-08-2025  08:39             3,184 broadcast-jenkins-discover.nse
09-08-2025  08:39             9,225 broadcast-listener.nse
09-08-2025  08:39             3,813 broadcast-ms-sql-discover.nse
09-08-2025  08:39             1,909 broadcast-netbios-master-browser.nse
09-08-2025  08:39             2,748 broadcast-networker-discover.nse
09-08-2025  08:39             2,005 broadcast-novell-locate.nse
09-08-2025  08:39            16,288 broadcast-ospf2-discover.nse
09-08-2025  08:39             1,966 broadcast-pc-anywhere.nse
09-08-2025  08:39             3,550 broadcast-pc-duo.nse
09-08-2025  08:39             6,300 broadcast-pim-discovery.nse
09-08-2025  08:39             8,830 broadcast-ping.nse
09-08-2025  08:39             2,617 broadcast-pppoe-discover.nse
09-08-2025  08:39             4,966 broadcast-rip-discover.nse
09-08-2025  08:39             6,145 broadcast-ripng-discover.nse
09-08-2025  08:39             3,869 broadcast-sonicwall-discover.nse
09-08-2025  08:39             5,316 broadcast-sybase-asa-discover.nse
09-08-2025  08:39             1,892 broadcast-tellstick-discover.nse
09-08-2025  08:39             1,511 broadcast-upnp-info.nse
09-08-2025  08:39               924 broadcast-versant-locate.nse
09-08-2025  08:39             2,084 broadcast-wake-on-lan.nse
09-08-2025  08:39             6,851 broadcast-wpad-discover.nse
09-08-2025  08:39             3,117 broadcast-wsdd-discover.nse
09-08-2025  08:39             1,996 broadcast-xdmcp-discover.nse
09-08-2025  08:39             3,742 cassandra-brute.nse
09-08-2025  08:39             2,564 cassandra-info.nse
09-08-2025  08:39             1,506 cccam-version.nse
09-08-2025  08:39            18,114 cics-enum.nse
09-08-2025  08:39            13,755 cics-info.nse
09-08-2025  08:39            11,113 cics-user-brute.nse
09-08-2025  08:39             9,403 cics-user-enum.nse
09-08-2025  08:39             4,749 citrix-brute-xml.nse
09-08-2025  08:39             4,644 citrix-enum-apps-xml.nse
09-08-2025  08:39             4,170 citrix-enum-apps.nse
09-08-2025  08:39             1,126 citrix-enum-servers-xml.nse
09-08-2025  08:39             3,880 citrix-enum-servers.nse
09-08-2025  08:39             7,092 clamav-exec.nse
09-08-2025  08:39             5,019 clock-skew.nse
09-08-2025  08:39             9,405 coap-resources.nse
09-08-2025  08:39             2,594 couchdb-databases.nse
09-08-2025  08:39             8,986 couchdb-stats.nse
09-08-2025  08:39             1,082 creds-summary.nse
09-08-2025  08:39             2,137 cups-info.nse
09-08-2025  08:39             1,420 cups-queue-info.nse
09-08-2025  08:39             3,879 cvs-brute-repository.nse
09-08-2025  08:39             2,948 cvs-brute.nse
09-08-2025  08:39             9,203 daap-get-library.nse
09-08-2025  08:39               578 daytime.nse
09-08-2025  08:39            14,353 db2-das-info.nse
09-08-2025  08:39             4,398 deluge-rpc-brute.nse
09-08-2025  08:39             8,462 dhcp-discover.nse
09-08-2025  08:39             2,275 dicom-brute.nse
09-08-2025  08:39             2,543 dicom-ping.nse
09-08-2025  08:39             2,499 dict-info.nse
09-08-2025  08:39             3,519 distcc-cve2004-2687.nse
09-08-2025  08:39             5,329 dns-blacklist.nse
09-08-2025  08:39            10,100 dns-brute.nse
09-08-2025  08:39             6,639 dns-cache-snoop.nse
09-08-2025  08:39            15,152 dns-check-zone.nse
09-08-2025  08:39            14,826 dns-client-subnet-scan.nse
09-08-2025  08:39            10,168 dns-fuzz.nse
09-08-2025  08:39             3,803 dns-ip6-arpa-scan.nse
09-08-2025  08:39            10,580 dns-nsec-enum.nse
09-08-2025  08:39            12,702 dns-nsec3-enum.nse
09-08-2025  08:39             3,441 dns-nsid.nse
09-08-2025  08:39             4,364 dns-random-srcport.nse
09-08-2025  08:39             4,363 dns-random-txid.nse
09-08-2025  08:39             1,456 dns-recursion.nse
09-08-2025  08:39             2,167 dns-service-discovery.nse
09-08-2025  08:39             5,679 dns-srv-enum.nse
09-08-2025  08:39             5,765 dns-update.nse
09-08-2025  08:39             2,123 dns-zeustracker.nse
09-08-2025  08:39            24,731 dns-zone-transfer.nse
09-08-2025  08:39             1,271 docker-version.nse
09-08-2025  08:39             3,865 domcon-brute.nse
09-08-2025  08:39             4,539 domcon-cmd.nse
09-08-2025  08:39             4,205 domino-enum-users.nse
09-08-2025  08:39             2,835 dpap-brute.nse
09-08-2025  08:39             5,805 drda-brute.nse
09-08-2025  08:39             3,796 drda-info.nse
09-08-2025  08:39             7,477 duplicates.nse
09-08-2025  08:39             5,693 eap-info.nse
09-08-2025  08:39            57,869 enip-info.nse
09-08-2025  08:39             1,716 epmd-info.nse
09-08-2025  08:39             2,564 eppc-enum-processes.nse
09-08-2025  08:39             3,910 fcrdns.nse
09-08-2025  08:39             1,083 finger.nse
09-08-2025  08:39             4,183 fingerprint-strings.nse
09-08-2025  08:39            29,093 firewalk.nse
09-08-2025  08:39             8,865 firewall-bypass.nse
09-08-2025  08:39            10,811 flume-master-info.nse
09-08-2025  08:39             3,796 fox-info.nse
09-08-2025  08:39             3,806 freelancer-info.nse
09-08-2025  08:39             4,530 ftp-anon.nse
09-08-2025  08:39             3,253 ftp-bounce.nse
09-08-2025  08:39             3,108 ftp-brute.nse
09-08-2025  08:39             3,272 ftp-libopie.nse
09-08-2025  08:39             3,290 ftp-proftpd-backdoor.nse
09-08-2025  08:39             3,768 ftp-syst.nse
09-08-2025  08:39             6,021 ftp-vsftpd-backdoor.nse
09-08-2025  08:39             5,923 ftp-vuln-cve2010-4221.nse
09-08-2025  08:39             7,919 ganglia-info.nse
09-08-2025  08:39             1,859 giop-info.nse
09-08-2025  08:39             6,850 gkrellm-info.nse
09-08-2025  08:39             2,342 gopher-ls.nse
09-08-2025  08:39             2,618 gpsd-info.nse
09-08-2025  08:39             1,927 hadoop-datanode-info.nse
09-08-2025  08:39             7,033 hadoop-jobtracker-info.nse
09-08-2025  08:39             6,697 hadoop-namenode-info.nse
09-08-2025  08:39             4,514 hadoop-secondary-namenode-info.nse
09-08-2025  08:39             2,955 hadoop-tasktracker-info.nse
09-08-2025  08:39            10,904 hartip-info.nse
09-08-2025  08:39             5,483 hbase-master-info.nse
09-08-2025  08:39             3,645 hbase-region-info.nse
09-08-2025  08:39             1,853 hddtemp-info.nse
09-08-2025  08:39             4,424 hnap-info.nse
09-08-2025  08:39             3,798 hostmap-bfk.nse
09-08-2025  08:39             4,933 hostmap-crtsh.nse
09-08-2025  08:39             2,100 hostmap-robtex.nse
09-08-2025  08:39             2,153 http-adobe-coldfusion-apsa1301.nse
09-08-2025  08:39             5,149 http-affiliate-id.nse
09-08-2025  08:39             1,950 http-apache-negotiation.nse
09-08-2025  08:39             4,499 http-apache-server-status.nse
09-08-2025  08:39             1,805 http-aspnet-debug.nse
09-08-2025  08:39             3,959 http-auth-finder.nse
09-08-2025  08:39             3,187 http-auth.nse
09-08-2025  08:39             2,865 http-avaya-ipoffice-users.nse
09-08-2025  08:39             4,372 http-awstatstotals-exec.nse
09-08-2025  08:39             6,872 http-axis2-dir-traversal.nse
09-08-2025  08:39             5,484 http-backup-finder.nse
09-08-2025  08:39             6,387 http-barracuda-dir-traversal.nse
09-08-2025  08:39             2,038 http-bigip-cookie.nse
09-08-2025  08:39             4,920 http-brute.nse
09-08-2025  08:39             4,436 http-cakephp-version.nse
09-08-2025  08:39             4,927 http-chrono.nse
09-08-2025  08:39             1,695 http-cisco-anyconnect.nse
09-08-2025  08:39             5,520 http-coldfusion-subzero.nse
09-08-2025  08:39             4,150 http-comments-displayer.nse
09-08-2025  08:39             7,251 http-config-backup.nse
09-08-2025  08:39             5,139 http-cookie-flags.nse
09-08-2025  08:39             2,577 http-cors.nse
09-08-2025  08:39            13,803 http-cross-domain-policy.nse
09-08-2025  08:39             5,418 http-csrf.nse
09-08-2025  08:39             1,718 http-date.nse
09-08-2025  08:39            17,388 http-default-accounts.nse
09-08-2025  08:39             4,288 http-devframework.nse
09-08-2025  08:39             2,529 http-dlink-backdoor.nse
09-08-2025  08:39             4,452 http-dombased-xss.nse
09-08-2025  08:39            13,893 http-domino-enum-passwords.nse
09-08-2025  08:39             2,256 http-drupal-enum-users.nse
09-08-2025  08:39             6,931 http-drupal-enum.nse
09-08-2025  08:39            20,667 http-enum.nse
09-08-2025  08:39             3,347 http-errors.nse
09-08-2025  08:39            20,413 http-exif-spider.nse
09-08-2025  08:39             5,199 http-favicon.nse
09-08-2025  08:39             4,451 http-feed.nse
09-08-2025  08:39             9,076 http-fetch.nse
09-08-2025  08:39            11,327 http-fileupload-exploiter.nse
09-08-2025  08:39            21,101 http-form-brute.nse
09-08-2025  08:39             7,934 http-form-fuzzer.nse
09-08-2025  08:39             2,739 http-frontpage-login.nse
09-08-2025  08:39             2,164 http-generator.nse
09-08-2025  08:39            12,100 http-git.nse
09-08-2025  08:39             3,195 http-gitweb-projects-enum.nse
09-08-2025  08:39             3,381 http-google-malware.nse
09-08-2025  08:39            11,692 http-grep.nse
09-08-2025  08:39             1,797 http-headers.nse
09-08-2025  08:39             3,383 http-hp-ilo-info.nse
09-08-2025  08:39             6,973 http-huawei-hg5xx-vuln.nse
09-08-2025  08:39             2,801 http-icloud-findmyiphone.nse
09-08-2025  08:39             4,085 http-icloud-sendmsg.nse
09-08-2025  08:39             6,073 http-iis-short-name-brute.nse
09-08-2025  08:39             7,921 http-iis-webdav-vuln.nse
09-08-2025  08:39             2,540 http-internal-ip-disclosure.nse
09-08-2025  08:39             5,422 http-joomla-brute.nse
09-08-2025  08:39             5,479 http-jsonp-detection.nse
09-08-2025  08:39             2,649 http-litespeed-sourcecode-download.nse
09-08-2025  08:39             6,120 http-ls.nse
09-08-2025  08:39             3,269 http-majordomo2-dir-traversal.nse
09-08-2025  08:39             2,833 http-malware-host.nse
09-08-2025  08:39             3,704 http-mcmp.nse
09-08-2025  08:39             6,895 http-method-tamper.nse
09-08-2025  08:39             7,320 http-methods.nse
09-08-2025  08:39             2,726 http-mobileversion-checker.nse
09-08-2025  08:39             4,461 http-ntlm-info.nse
09-08-2025  08:39             8,269 http-open-proxy.nse
09-08-2025  08:39             4,756 http-open-redirect.nse
09-08-2025  08:39             7,023 http-passwd.nse
09-08-2025  08:39             7,070 http-php-version.nse
09-08-2025  08:39             6,225 http-phpmyadmin-dir-traversal.nse
09-08-2025  08:39             5,822 http-phpself-xss.nse
09-08-2025  08:39             3,487 http-proxy-brute.nse
09-08-2025  08:39             1,930 http-put.nse
09-08-2025  08:39             3,591 http-qnap-nas-info.nse
09-08-2025  08:39             2,175 http-referer-checker.nse
09-08-2025  08:39             9,599 http-rfi-spider.nse
09-08-2025  08:39             2,737 http-robots.txt.nse
09-08-2025  08:39             2,305 http-robtex-reverse-ip.nse
09-08-2025  08:39             2,776 http-robtex-shared-ns.nse
09-08-2025  08:39             5,034 http-sap-netweaver-leak.nse
09-08-2025  08:39            15,956 http-security-headers.nse
09-08-2025  08:39             3,283 http-server-header.nse
09-08-2025  08:39             5,489 http-shellshock.nse
09-08-2025  08:39             5,344 http-sitemap-generator.nse
09-08-2025  08:39             5,464 http-slowloris-check.nse
09-08-2025  08:39            11,167 http-slowloris.nse
09-08-2025  08:39             9,404 http-sql-injection.nse
09-08-2025  08:39             8,451 http-stored-xss.nse
09-08-2025  08:39             4,018 http-svn-enum.nse
09-08-2025  08:39             4,360 http-svn-info.nse
09-08-2025  08:39             2,317 http-title.nse
09-08-2025  08:39             6,026 http-tplink-dir-traversal.nse
09-08-2025  08:39             1,947 http-trace.nse
09-08-2025  08:39             5,294 http-traceroute.nse
09-08-2025  08:39             6,437 http-trane-info.nse
09-08-2025  08:39             5,549 http-unsafe-output-escaping.nse
09-08-2025  08:39             5,403 http-useragent-tester.nse
09-08-2025  08:39             4,550 http-userdir-enum.nse
09-08-2025  08:39             5,785 http-vhosts.nse
09-08-2025  08:39            10,770 http-virustotal.nse
09-08-2025  08:39             2,078 http-vlcstreamer-ls.nse
09-08-2025  08:39             4,111 http-vmware-path-vuln.nse
09-08-2025  08:39             3,273 http-vuln-cve2006-3392.nse
09-08-2025  08:39             6,610 http-vuln-cve2009-3960.nse
09-08-2025  08:39             2,957 http-vuln-cve2010-0738.nse
09-08-2025  08:39             5,607 http-vuln-cve2010-2861.nse
09-08-2025  08:39             4,527 http-vuln-cve2011-3192.nse
09-08-2025  08:39             5,851 http-vuln-cve2011-3368.nse
09-08-2025  08:39             4,403 http-vuln-cve2012-1823.nse
09-08-2025  08:39             4,831 http-vuln-cve2013-0156.nse
09-08-2025  08:39             2,853 http-vuln-cve2013-6786.nse
09-08-2025  08:39             5,009 http-vuln-cve2013-7091.nse
09-08-2025  08:39             2,974 http-vuln-cve2014-2126.nse
09-08-2025  08:39             3,363 http-vuln-cve2014-2127.nse
09-08-2025  08:39             3,222 http-vuln-cve2014-2128.nse
09-08-2025  08:39             3,008 http-vuln-cve2014-2129.nse
09-08-2025  08:39            14,018 http-vuln-cve2014-3704.nse
09-08-2025  08:39             4,523 http-vuln-cve2014-8877.nse
09-08-2025  08:39             7,774 http-vuln-cve2015-1427.nse
09-08-2025  08:39             3,443 http-vuln-cve2015-1635.nse
09-08-2025  08:39             4,372 http-vuln-cve2017-1001000.nse
09-08-2025  08:39             2,594 http-vuln-cve2017-5638.nse
09-08-2025  08:39             5,480 http-vuln-cve2017-5689.nse
09-08-2025  08:39             5,187 http-vuln-cve2017-8917.nse
09-08-2025  08:39             2,699 http-vuln-misfortune-cookie.nse
09-08-2025  08:39             4,225 http-vuln-wnr1000-creds.nse
09-08-2025  08:39             5,422 http-waf-detect.nse
09-08-2025  08:39            19,339 http-waf-fingerprint.nse
09-08-2025  08:39             5,806 http-webdav-scan.nse
09-08-2025  08:39             5,061 http-wordpress-brute.nse
09-08-2025  08:39            10,866 http-wordpress-enum.nse
09-08-2025  08:39             4,641 http-wordpress-users.nse
09-08-2025  08:39             2,653 http-xssed.nse
09-08-2025  08:39             2,528 https-redirect.nse
09-08-2025  08:39             2,133 iax2-brute.nse
09-08-2025  08:39             1,377 iax2-version.nse
09-08-2025  08:39             3,462 icap-info.nse
09-08-2025  08:39             4,343 iec-identify.nse
09-08-2025  08:39            12,333 iec61850-mms.nse
09-08-2025  08:39             5,107 ike-version.nse
09-08-2025  08:39             4,441 imap-brute.nse
09-08-2025  08:39             1,515 imap-capabilities.nse
09-08-2025  08:39             5,366 imap-ntlm-info.nse
09-08-2025  08:39             6,494 impress-remote-discover.nse
09-08-2025  08:39             2,935 informix-brute.nse
09-08-2025  08:39             3,414 informix-query.nse
09-08-2025  08:39             4,548 informix-tables.nse
09-08-2025  08:39             3,420 ip-forwarding.nse
09-08-2025  08:39             2,101 ip-geolocation-geoplugin.nse
09-08-2025  08:39             2,939 ip-geolocation-ipinfodb.nse
09-08-2025  08:39             6,025 ip-geolocation-map-bing.nse
09-08-2025  08:39             6,003 ip-geolocation-map-google.nse
09-08-2025  08:39             2,343 ip-geolocation-map-kml.nse
09-08-2025  08:39            23,366 ip-geolocation-maxmind.nse
09-08-2025  08:39             2,437 ip-https-discover.nse
09-08-2025  08:39             5,567 ipidseq.nse
09-08-2025  08:39             3,425 ipmi-brute.nse
09-08-2025  08:39             3,161 ipmi-cipher-zero.nse
09-08-2025  08:39             3,745 ipmi-version.nse
09-08-2025  08:39            16,113 ipv6-multicast-mld-list.nse
09-08-2025  08:39             8,388 ipv6-node-info.nse
09-08-2025  08:39             6,077 ipv6-ra-flood.nse
09-08-2025  08:39             6,946 irc-botnet-channels.nse
09-08-2025  08:39             3,574 irc-brute.nse
09-08-2025  08:39             4,507 irc-info.nse
09-08-2025  08:39             6,361 irc-sasl-brute.nse
09-08-2025  08:39             8,480 irc-unrealircd-backdoor.nse
09-08-2025  08:39             2,390 iscsi-brute.nse
09-08-2025  08:39             3,117 iscsi-info.nse
09-08-2025  08:39             1,952 isns-info.nse
09-08-2025  08:39             3,330 jdwp-exec.nse
09-08-2025  08:39             3,116 jdwp-info.nse
09-08-2025  08:39             3,048 jdwp-inject.nse
09-08-2025  08:39             2,330 jdwp-version.nse
09-08-2025  08:39            10,621 knx-gateway-discover.nse
09-08-2025  08:39             5,565 knx-gateway-info.nse
09-08-2025  08:39            13,235 krb5-enum-users.nse
09-08-2025  08:39            14,051 ldap-brute.nse
09-08-2025  08:39             4,995 ldap-novell-getpass.nse
09-08-2025  08:39             9,414 ldap-rootdse.nse
09-08-2025  08:39            12,435 ldap-search.nse
09-08-2025  08:39             2,546 lexmark-config.nse
09-08-2025  08:39             6,741 llmnr-resolve.nse
09-08-2025  08:39             9,032 lltd-discovery.nse
09-08-2025  08:39             7,598 lu-enum.nse
09-08-2025  08:39             6,423 maxdb-info.nse
09-08-2025  08:39             2,635 mcafee-epo-agent.nse
09-08-2025  08:39             2,884 membase-brute.nse
09-08-2025  08:39             4,900 membase-http-info.nse
09-08-2025  08:39             5,657 memcached-info.nse
09-08-2025  08:39            10,089 metasploit-info.nse
09-08-2025  08:39             2,952 metasploit-msgrpc-brute.nse
09-08-2025  08:39             3,199 metasploit-xmlrpc-brute.nse
09-08-2025  08:39             3,090 mikrotik-routeros-brute.nse
09-08-2025  08:39             4,161 mikrotik-routeros-username-brute.nse
09-08-2025  08:39             5,994 mikrotik-routeros-version.nse
09-08-2025  08:39             3,264 mmouse-brute.nse
09-08-2025  08:39             5,686 mmouse-exec.nse
09-08-2025  08:39             5,996 modbus-discover.nse
09-08-2025  08:39             2,588 mongodb-brute.nse
09-08-2025  08:39             2,593 mongodb-databases.nse
09-08-2025  08:39             3,673 mongodb-info.nse
09-08-2025  08:39            15,063 mqtt-subscribe.nse
09-08-2025  08:39             9,254 mrinfo.nse
09-08-2025  08:39            11,619 ms-sql-brute.nse
09-08-2025  08:39             5,498 ms-sql-config.nse
09-08-2025  08:39             2,631 ms-sql-dac.nse
09-08-2025  08:39             3,580 ms-sql-dump-hashes.nse
09-08-2025  08:39             6,563 ms-sql-empty-password.nse
09-08-2025  08:39             5,378 ms-sql-hasdbaccess.nse
09-08-2025  08:39             9,782 ms-sql-info.nse
09-08-2025  08:39             4,051 ms-sql-ntlm-info.nse
09-08-2025  08:39             4,221 ms-sql-query.nse
09-08-2025  08:39             8,936 ms-sql-tables.nse
09-08-2025  08:39             5,899 ms-sql-xp-cmdshell.nse
09-08-2025  08:39             3,235 msrpc-enum.nse
09-08-2025  08:39            12,120 mtrace.nse
09-08-2025  08:39            10,124 multicast-profinet-discovery.nse
09-08-2025  08:39             3,424 murmur-version.nse
09-08-2025  08:39             6,688 mysql-audit.nse
09-08-2025  08:39             2,977 mysql-brute.nse
09-08-2025  08:39             2,945 mysql-databases.nse
09-08-2025  08:39             3,263 mysql-dump-hashes.nse
09-08-2025  08:39             2,020 mysql-empty-password.nse
09-08-2025  08:39             3,413 mysql-enum.nse
09-08-2025  08:39             3,455 mysql-info.nse
09-08-2025  08:39             3,714 mysql-query.nse
09-08-2025  08:39             2,811 mysql-users.nse
09-08-2025  08:39             3,265 mysql-variables.nse
09-08-2025  08:39             6,977 mysql-vuln-cve2012-2122.nse
09-08-2025  08:39             1,257 nat-pmp-info.nse
09-08-2025  08:39             4,520 nat-pmp-mapport.nse
09-08-2025  08:39             5,387 nbd-info.nse
09-08-2025  08:39             1,997 nbns-interfaces.nse
09-08-2025  08:39             7,718 nbstat.nse
09-08-2025  08:39             1,341 ncp-enum-users.nse
09-08-2025  08:39             1,259 ncp-serverinfo.nse
09-08-2025  08:39             2,323 ndmp-fs-info.nse
09-08-2025  08:39             2,307 ndmp-version.nse
09-08-2025  08:39             4,562 nessus-brute.nse
09-08-2025  08:39             4,100 nessus-xmlrpc-brute.nse
09-08-2025  08:39             1,830 netbus-auth-bypass.nse
09-08-2025  08:39             1,677 netbus-brute.nse
09-08-2025  08:39             5,690 netbus-info.nse
09-08-2025  08:39             1,179 netbus-version.nse
09-08-2025  08:39             2,734 nexpose-brute.nse
09-08-2025  08:39            14,534 nfs-ls.nse
09-08-2025  08:39             2,714 nfs-showmount.nse
09-08-2025  08:39             9,947 nfs-statfs.nse
09-08-2025  08:39             6,422 nje-node-brute.nse
09-08-2025  08:39             6,139 nje-pass-brute.nse
09-08-2025  08:39             5,119 nntp-ntlm-info.nse
09-08-2025  08:39             4,098 nping-brute.nse
09-08-2025  08:39             7,689 nrpe-enum.nse
09-08-2025  08:39             6,098 ntp-info.nse
09-08-2025  08:39            32,773 ntp-monlist.nse
09-08-2025  08:39             2,180 omp2-brute.nse
09-08-2025  08:39             3,320 omp2-enum-targets.nse
09-08-2025  08:39             6,805 omron-info.nse
09-08-2025  08:39             6,594 openflow-info.nse
09-08-2025  08:39             5,243 openlookup-info.nse
09-08-2025  08:39             3,172 openvas-otp-brute.nse
09-08-2025  08:39             7,077 openwebnet-discovery.nse
09-08-2025  08:39             6,733 oracle-brute-stealth.nse
09-08-2025  08:39             7,416 oracle-brute.nse
09-08-2025  08:39             3,951 oracle-enum-users.nse
09-08-2025  08:39             4,821 oracle-sid-brute.nse
09-08-2025  08:39             3,167 oracle-tns-version.nse
09-08-2025  08:39             3,021 ovs-agent-version.nse
09-08-2025  08:39            22,474 p2p-conficker.nse
09-08-2025  08:39            10,157 path-mtu.nse
09-08-2025  08:39             5,317 pcanywhere-brute.nse
09-08-2025  08:39             3,563 pcworx-info.nse
09-08-2025  08:39             5,378 pgsql-brute.nse
09-08-2025  08:39             3,042 pjl-ready-message.nse
09-08-2025  08:39             4,047 pop3-brute.nse
09-08-2025  08:39             1,397 pop3-capabilities.nse
09-08-2025  08:39             4,941 pop3-ntlm-info.nse
09-08-2025  08:39             4,393 port-states.nse
09-08-2025  08:39             3,328 pptp-version.nse
09-08-2025  08:39             5,603 profinet-cm-lookup.nse
09-08-2025  08:39             8,712 puppet-naivesigning.nse
09-08-2025  08:39             4,326 qconn-exec.nse
09-08-2025  08:39            14,597 qscan.nse
09-08-2025  08:39            11,070 quake1-info.nse
09-08-2025  08:39             6,732 quake3-info.nse
09-08-2025  08:39             7,274 quake3-master-getservers.nse
09-08-2025  08:39             5,961 rdp-enum-encryption.nse
09-08-2025  08:39             5,791 rdp-ntlm-info.nse
09-08-2025  08:39             9,425 rdp-vuln-ms12-020.nse
09-08-2025  08:39             3,264 realvnc-auth-bypass.nse
09-08-2025  08:39             2,795 redis-brute.nse
09-08-2025  08:39             7,004 redis-info.nse
09-08-2025  08:39             4,846 resolveall.nse
09-08-2025  08:39             3,554 reverse-index.nse
09-08-2025  08:39             3,128 rexec-brute.nse
09-08-2025  08:39             1,884 rfc868-time.nse
09-08-2025  08:39             5,564 riak-http-info.nse
09-08-2025  08:39             4,865 rlogin-brute.nse
09-08-2025  08:39            10,621 rmi-dumpregistry.nse
09-08-2025  08:39             4,011 rmi-vuln-classloader.nse
09-08-2025  08:39             8,869 rpc-grind.nse
09-08-2025  08:39             2,140 rpcap-brute.nse
09-08-2025  08:39             2,654 rpcap-info.nse
09-08-2025  08:39             4,601 rpcinfo.nse
09-08-2025  08:39             6,528 rsa-vuln-roca.nse
09-08-2025  08:39             3,132 rsync-brute.nse
09-08-2025  08:39             1,216 rsync-list-modules.nse
09-08-2025  08:39             1,479 rtsp-methods.nse
09-08-2025  08:39             5,739 rtsp-url-brute.nse
09-08-2025  08:39             5,528 rusers.nse
09-08-2025  08:39            10,287 s7-info.nse
09-08-2025  08:39             4,148 samba-vuln-cve-2012-1182.nse
09-08-2025  08:39            52,837 script.db
09-08-2025  08:39             8,733 servicetags.nse
09-08-2025  08:39             6,573 shodan-api.nse
09-08-2025  08:39             3,627 sip-brute.nse
09-08-2025  08:39             6,099 sip-call-spoof.nse
09-08-2025  08:39             8,585 sip-enum-users.nse
09-08-2025  08:39             1,652 sip-methods.nse
09-08-2025  08:39             2,164 skypev2-version.nse
09-08-2025  08:39            45,061 smb-brute.nse
09-08-2025  08:39             5,289 smb-double-pulsar-backdoor.nse
09-08-2025  08:39             4,840 smb-enum-domains.nse
09-08-2025  08:39             5,971 smb-enum-groups.nse
09-08-2025  08:39             8,043 smb-enum-processes.nse
09-08-2025  08:39            27,274 smb-enum-services.nse
09-08-2025  08:39            12,017 smb-enum-sessions.nse
09-08-2025  08:39             6,923 smb-enum-shares.nse
09-08-2025  08:39            12,527 smb-enum-users.nse
09-08-2025  08:39             4,418 smb-flood.nse
09-08-2025  08:39             7,471 smb-ls.nse
09-08-2025  08:39             8,758 smb-mbenum.nse
09-08-2025  08:39             8,220 smb-os-discovery.nse
09-08-2025  08:39             4,982 smb-print-text.nse
09-08-2025  08:39             1,833 smb-protocols.nse
09-08-2025  08:39            63,596 smb-psexec.nse
09-08-2025  08:39             5,190 smb-security-mode.nse
09-08-2025  08:39             2,424 smb-server-stats.nse
09-08-2025  08:39            14,159 smb-system-info.nse
09-08-2025  08:39             7,524 smb-vuln-conficker.nse
09-08-2025  08:39            23,154 smb-vuln-cve-2017-7494.nse
09-08-2025  08:39             6,402 smb-vuln-cve2009-3103.nse
09-08-2025  08:39             6,545 smb-vuln-ms06-025.nse
09-08-2025  08:39             5,386 smb-vuln-ms07-029.nse
09-08-2025  08:39             5,688 smb-vuln-ms08-067.nse
09-08-2025  08:39             5,647 smb-vuln-ms10-054.nse
09-08-2025  08:39             7,214 smb-vuln-ms10-061.nse
09-08-2025  08:39             7,344 smb-vuln-ms17-010.nse
09-08-2025  08:39             4,400 smb-vuln-regsvc-dos.nse
09-08-2025  08:39             6,586 smb-vuln-webexec.nse
09-08-2025  08:39             5,084 smb-webexec-exploit.nse
09-08-2025  08:39             3,753 smb2-capabilities.nse
09-08-2025  08:39             2,689 smb2-security-mode.nse
09-08-2025  08:39             1,408 smb2-time.nse
09-08-2025  08:39             5,269 smb2-vuln-uptime.nse
09-08-2025  08:39             4,309 smtp-brute.nse
09-08-2025  08:39             4,957 smtp-commands.nse
09-08-2025  08:39            12,006 smtp-enum-users.nse
09-08-2025  08:39             5,915 smtp-ntlm-info.nse
09-08-2025  08:39            10,148 smtp-open-relay.nse
09-08-2025  08:39               716 smtp-strangeport.nse
09-08-2025  08:39            14,781 smtp-vuln-cve2010-4344.nse
09-08-2025  08:39             7,719 smtp-vuln-cve2011-1720.nse
09-08-2025  08:39             7,603 smtp-vuln-cve2011-1764.nse
09-08-2025  08:39             4,327 sniffer-detect.nse
09-08-2025  08:39             7,816 snmp-brute.nse
09-08-2025  08:39             4,388 snmp-hh3c-logins.nse
09-08-2025  08:39             5,216 snmp-info.nse
09-08-2025  08:39            28,644 snmp-interfaces.nse
09-08-2025  08:39             5,978 snmp-ios-config.nse
09-08-2025  08:39             4,156 snmp-netstat.nse
09-08-2025  08:39             4,431 snmp-processes.nse
09-08-2025  08:39             1,857 snmp-sysdescr.nse
09-08-2025  08:39             2,570 snmp-win32-services.nse
09-08-2025  08:39             2,739 snmp-win32-shares.nse
09-08-2025  08:39             4,713 snmp-win32-software.nse
09-08-2025  08:39             2,016 snmp-win32-users.nse
09-08-2025  08:39             1,753 socks-auth-info.nse
09-08-2025  08:39             2,521 socks-brute.nse
09-08-2025  08:39             6,527 socks-open-proxy.nse
09-08-2025  08:39             1,665 ssh-auth-methods.nse
09-08-2025  08:39             2,881 ssh-brute.nse
09-08-2025  08:39            16,036 ssh-hostkey.nse
09-08-2025  08:39             6,165 ssh-publickey-acceptance.nse
09-08-2025  08:39             3,817 ssh-run.nse
09-08-2025  08:39             5,391 ssh2-enum-algos.nse
09-08-2025  08:39             1,423 sshv1.nse
09-08-2025  08:39            10,142 ssl-ccs-injection.nse
09-08-2025  08:39             3,900 ssl-cert-intaddr.nse
09-08-2025  08:39            13,175 ssl-cert.nse
09-08-2025  08:39             6,836 ssl-date.nse
09-08-2025  08:39            39,926 ssl-dh-params.nse
09-08-2025  08:39            40,040 ssl-enum-ciphers.nse
09-08-2025  08:39             7,797 ssl-heartbleed.nse
09-08-2025  08:39             4,457 ssl-known-key.nse
09-08-2025  08:39            11,230 ssl-poodle.nse
09-08-2025  08:39            11,278 sslv2-drown.nse
09-08-2025  08:39             1,604 sslv2.nse
09-08-2025  08:39             2,325 sstp-discover.nse
09-08-2025  08:39             1,188 stun-info.nse
09-08-2025  08:39             1,141 stun-version.nse
09-08-2025  08:39             3,393 stuxnet-detect.nse
09-08-2025  08:39             3,737 supermicro-ipmi-conf.nse
09-08-2025  08:39             7,528 svn-brute.nse
09-08-2025  08:39             2,923 targets-asn.nse
09-08-2025  08:39             3,463 targets-ipv6-eui64.nse
09-08-2025  08:39             7,536 targets-ipv6-map4to6.nse
09-08-2025  08:39             4,405 targets-ipv6-multicast-echo.nse
09-08-2025  08:39             5,693 targets-ipv6-multicast-invalid-dst.nse
09-08-2025  08:39             4,173 targets-ipv6-multicast-mld.nse
09-08-2025  08:39             8,591 targets-ipv6-multicast-slaac.nse
09-08-2025  08:39             9,268 targets-ipv6-wordlist.nse
09-08-2025  08:39             4,902 targets-sniffer.nse
09-08-2025  08:39             1,822 targets-traceroute.nse
09-08-2025  08:39             3,596 targets-xml.nse
09-08-2025  08:39             2,489 teamspeak2-version.nse
09-08-2025  08:39            20,262 telnet-brute.nse
09-08-2025  08:39             3,008 telnet-encryption.nse
09-08-2025  08:39             4,564 telnet-ntlm-info.nse
09-08-2025  08:39             5,736 tftp-enum.nse
09-08-2025  08:39            10,034 tftp-version.nse
09-08-2025  08:39             6,187 tls-alpn.nse
09-08-2025  08:39             4,203 tls-nextprotoneg.nse
09-08-2025  08:39            11,773 tls-ticketbleed.nse
09-08-2025  08:39             4,118 tn3270-screen.nse
09-08-2025  08:39             3,832 tor-consensus-checker.nse
09-08-2025  08:39             5,954 traceroute-geolocation.nse
09-08-2025  08:39            13,692 tso-brute.nse
09-08-2025  08:39            10,304 tso-enum.nse
09-08-2025  08:39            10,107 ubiquiti-discovery.nse
09-08-2025  08:39               895 unittest.nse
09-08-2025  08:39             3,836 unusual-port.nse
09-08-2025  08:39             1,669 upnp-info.nse
09-08-2025  08:39             3,125 uptime-agent-info.nse
09-08-2025  08:39             4,296 url-snarf.nse
09-08-2025  08:39            25,403 ventrilo-info.nse
09-08-2025  08:39             3,190 versant-info.nse
09-08-2025  08:39             3,367 vmauthd-brute.nse
09-08-2025  08:39             3,013 vmware-version.nse
09-08-2025  08:39             4,217 vnc-brute.nse
09-08-2025  08:39             4,348 vnc-info.nse
09-08-2025  08:39             3,039 vnc-title.nse
09-08-2025  08:39             5,559 voldemort-info.nse
09-08-2025  08:39            10,409 vtam-enum.nse
09-08-2025  08:39             7,077 vulners.nse
09-08-2025  08:39             2,553 vuze-dht-info.nse
09-08-2025  08:39             7,789 wdb-version.nse
09-08-2025  08:39             3,589 weblogic-t3-info.nse
09-08-2025  08:39             4,203 whois-domain.nse
09-08-2025  08:39            89,578 whois-ip.nse
09-08-2025  08:39             2,629 wsdd-discover.nse
09-08-2025  08:39             2,286 x11-access.nse
09-08-2025  08:39             2,095 xdmcp-discover.nse
09-08-2025  08:39             4,362 xmlrpc-methods.nse
09-08-2025  08:39             4,316 xmpp-brute.nse
09-08-2025  08:39            17,285 xmpp-info.nse
             613 File(s)      3,897,701 bytes
               2 Dir(s)  24,233,660,416 bytes free

C:\Program Files (x86)\Nmap\scripts>nmap --script=http-title.nse, http-enum.nse -p 80,443 aira.protosonline.in
Starting Nmap 7.98 ( https://nmap.org ) at 2025-09-25 10:22 +0530
Failed to resolve "http-enum.nse".
Nmap scan report for aira.protosonline.in (136.185.21.72)
Host is up (0.0010s latency).
rDNS record for 136.185.21.72: abts-tn-static-72.21.185.136.airtelbroadband.in

PORT    STATE SERVICE
80/tcp  open  http
|_http-title: Did not follow redirect to https://aira.protosonline.in/
443/tcp open  https
|_http-title: Protos

Nmap done: 1 IP address (1 host up) scanned in 6.95 seconds
```


## 🌐 Host Discovery Techniques

**Host Discovery** is the fundamental process of identifying active hosts on a network before conducting detailed port scans.

### Network Discovery Example
```bash
nmap -sn 192.168.0.0/24
```

**Sample Results:**
```
Nmap scan report for 192.168.0.1
Host is up (0.0010s latency).
MAC Address: 9C:A2:F4:8F:40:A5 (TP-Link Limited)      # Router/Gateway

Nmap scan report for 192.168.0.8  
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D3:CA:FA (Giga-byte Technology)  # Desktop/Server

Nmap scan report for 192.168.0.18
Host is up (0.0010s latency). 
MAC Address: 08:BF:B8:76:CD:A3 (ASUSTek Computer)      # ASUS Device
Nmap scan report for 192.168.0.21
Host is up (0.00s latency).
MAC Address: D8:5E:D3:DA:AE:14 (Giga-byte Technology)
Nmap scan report for 192.168.0.41
Host is up (0.00s latency).
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)
Nmap scan report for 192.168.0.59
Host is up (0.0010s latency).
MAC Address: 50:2B:73:B1:AF:50 (Tenda Technology,Ltd.Dongguan branch)
Nmap scan report for 192.168.0.101
Host is up (0.00s latency).
MAC Address: 74:56:3C:54:EE:04 (Giga-byte Technology)
Nmap scan report for 192.168.0.104
Host is up (0.00s latency).
MAC Address: 74:56:3C:54:EE:08 (Giga-byte Technology)
Nmap scan report for 192.168.0.105
Host is up (0.00s latency).
MAC Address: 18:C0:4D:99:31:BB (Giga-byte Technology)
Nmap scan report for 192.168.0.110
Host is up (0.00s latency).
MAC Address: 18:C0:4D:99:3F:EA (Giga-byte Technology)
Nmap scan report for 192.168.0.111
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D3:C5:15 (Giga-byte Technology)
Nmap scan report for 192.168.0.112
Host is up (0.00s latency).
MAC Address: D8:5E:D3:DB:02:60 (Giga-byte Technology)
Nmap scan report for 192.168.0.125
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D0:72:E5 (Giga-byte Technology)
Nmap scan report for 192.168.0.130
Host is up (0.0010s latency).
MAC Address: 14:07:08:BA:1F:E0 (CP Plus Gmbh & KG)
Nmap scan report for 192.168.0.142
Host is up (0.00s latency).
MAC Address: 74:56:3C:54:EE:0F (Giga-byte Technology)
Nmap scan report for 192.168.0.144
Host is up (0.0010s latency).
MAC Address: D8:5E:D3:D3:C4:68 (Giga-byte Technology)
Nmap scan report for 192.168.0.145
Host is up (0.0010s latency).
MAC Address: D8:5E:D3:24:30:4F (Giga-byte Technology)
Nmap scan report for 192.168.0.175
Host is up (0.0020s latency).
MAC Address: 08:00:27:D1:F8:5D (Oracle VirtualBox virtual NIC)
Nmap scan report for 192.168.0.178
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D3:C4:22 (Giga-byte Technology)
Nmap scan report for 192.168.0.187
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D3:CE:3F (Giga-byte Technology)
Nmap scan report for 192.168.0.190
Host is up (0.00s latency).
MAC Address: D8:5E:D3:D3:C4:00 (Giga-byte Technology)
Nmap scan report for 192.168.0.195
Host is up (0.0010s latency).
MAC Address: C8:A3:62:CC:12:45 (Asix Electronics)
Nmap scan report for 192.168.0.196
Host is up (0.00s latency).
MAC Address: D8:5E:D3:8E:3B:E8 (Giga-byte Technology)
Nmap scan report for 192.168.0.197
Host is up (0.027s latency).
MAC Address: 00:17:7C:9E:33:75 (Smartlink Network Systems Limited)
Nmap scan report for 192.168.0.209
Host is up (0.00s latency).
MAC Address: D8:5E:D3:30:09:A9 (Giga-byte Technology)
Nmap scan report for 192.168.0.219
Host is up (0.00s latency).
MAC Address: D8:5E:D3:DB:01:C5 (Giga-byte Technology)
Nmap scan report for 192.168.0.241
Host is up (0.00044s latency).
MAC Address: 08:BF:B8:76:CD:A5 (ASUSTek Computer)
Nmap scan report for 192.168.0.25
Host is up.
Nmap scan report for 192.168.0.141
Host is up.
Nmap done: 256 IP addresses (29 hosts up) scanned in 17.57 seconds
```

## 🛡️ Vulnerability Scanning

**Vulnerability Scanning** is the systematic process of identifying, quantifying, and prioritizing security vulnerabilities in network systems and services.
    
### Vulnerability Scan Example
```bash
nmap -sV -p5001 --script=vulners.nse 192.168.0.41
```

**Critical Findings:**
```
PORT     STATE SERVICE VERSION
5001/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.9.13)

High-Risk Vulnerabilities:
├── CVE-2022-37454 (9.8) - Critical Python vulnerability
├── CVE-2007-4559  (9.8) - Tar extraction vulnerability  
├── CVE-2015-20107 (8.0) - Python mailcap module issue
└── CVE-2024-9287  (7.8) - Recent Python security flaw

⚠️  Multiple exploits available for identified vulnerabilities
|       DA7CD4B2-2AD0-5735-A5DE-26D392D51DDA    7.5     https://vulners.com/githubexploit/DA7CD4B2-2AD0-5735-A5DE-26D392D51DDA  *EXPLOIT*
|       CVE-2024-7592   7.5     https://vulners.com/cve/CVE-2024-7592
|       CVE-2024-6232   7.5     https://vulners.com/cve/CVE-2024-6232
|       CVE-2023-36632  7.5     https://vulners.com/cve/CVE-2023-36632
|       CVE-2023-24329  7.5     https://vulners.com/cve/CVE-2023-24329
|       CVE-2022-45061  7.5     https://vulners.com/cve/CVE-2022-45061
|       CVE-2022-0391   7.5     https://vulners.com/cve/CVE-2022-0391
|       CVE-2021-3737   7.5     https://vulners.com/cve/CVE-2021-3737
|       CVE-2020-10735  7.5     https://vulners.com/cve/CVE-2020-10735
|       CVE-2021-28861  7.4     https://vulners.com/cve/CVE-2021-28861
|       VERACODE:43715  5.9     https://vulners.com/veracode/VERACODE:43715
|       CVE-2021-3426   5.7     https://vulners.com/cve/CVE-2021-3426
|       VERACODE:43798  5.3     https://vulners.com/veracode/VERACODE:43798
|       CVE-2023-40217  5.3     https://vulners.com/cve/CVE-2023-40217
|       CVE-2023-27043  5.3     https://vulners.com/cve/CVE-2023-27043
|_      CVE-2021-4189   5.3     https://vulners.com/cve/CVE-2021-4189
|_http-server-header: Werkzeug/3.1.3 Python/3.9.13
MAC Address: D8:5E:D3:DA:B0:0D (Giga-byte Technology)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.97 seconds
```

## 🔗 Integration with Security Tools

### Metasploit Integration
NMAP reconnaissance data can be imported directly into Metasploit for exploitation:
```bash
# Export NMAP results to XML
nmap -A -oX scan_results.xml target.com

# Import into Metasploit
msf> db_import scan_results.xml
```

## 🥷 Advanced Evasion Techniques

### MAC Address Spoofing
**Purpose**: Change network interface MAC address for privacy or bypassing restrictions
```bash
nmap --spoof-mac 00:11:22:33:44:55 target.com
nmap --spoof-mac random target.com
nmap --spoof-mac apple target.com    # Use Apple OUI
```

### Idle/Zombie Scan
**Purpose**: Ultra-stealthy scanning using third-party "zombie" host
```bash
nmap -sI zombie_host:port target.com
```
- Packets appear to originate from zombie host
- Scanner's IP address remains hidden
- Requires predictable IP ID sequence from zombie

### Firewall Evasion Techniques

| Technique | NMAP Flag | Description |
|-----------|-----------|-------------|
| **Fragmentation** | `-f`, `--mtu` | Split packets into fragments |
| **Decoy Scanning** | `-D` | Use decoy IP addresses |
| **Source Port** | `--source-port` | Spoof source port number |
| **Timing Templates** | `-T0` to `-T5` | Adjust scan timing (slower = stealthier) |
| **Randomization** | `--randomize-hosts` | Randomize target order |

#### Fragmentation Examples
```bash
# Fragment packets
nmap -f target.com

# Custom MTU size
nmap --mtu 24 target.com

# Maximum fragmentation
nmap -f -f target.com
```

#### Decoy Scanning
```bash
# Use decoy IP addresses
nmap -D 192.168.1.100,192.168.1.101,ME target.com

# Random decoys
nmap -D RND:10 target.com
```

#### Timing and Stealth
```bash
# Paranoid timing (very slow, stealthy)
nmap -T0 target.com

# Sneaky timing
nmap -T1 target.com

# Normal timing (default)
nmap -T3 target.com

# Aggressive timing
nmap -T4 target.com
```

## ⚠️ Legal and Ethical Considerations

> **Important**: These techniques should only be used for:
> - Authorized penetration testing
> - Security research on your own systems
> - Educational purposes in controlled environments
> 
> Unauthorized scanning can be illegal and unethical. Always obtain proper permission before testing systems you don't own.

## 📚 Additional Resources

- **Official Documentation**: [nmap.org](https://nmap.org)
- **NSE Script Database**: [nmap.org/nsedoc](https://nmap.org/nsedoc/)
- **NMAP Book**: "Nmap Network Scanning" by Gordon Lyon

## 📜 Course Certificate

🎓 **[View Course Completion Certificate](NMAP%20Mastery%20-%20Ultimate%20Guide%20to%20Network%20Scanning.pdf)**

---
*This README covers the essential concepts from the NMAP Mastery Udemy course with practical examples and advanced techniques for network security professionals.*