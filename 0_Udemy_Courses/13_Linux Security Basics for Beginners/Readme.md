- Course [Link](https://www.udemy.com/course/basic-linux-security/)

- From Course: Linux Security Basics for Beginners

    - Trust: Make sure you are downloading from a trusted source.

    - Users
        - Add a new user: `sudo adduser username`
        - Delete a user: `sudo deluser username`
        - Change a user's password: `sudo passwd username`
        - List all users: `cut -d: -f1 /etc/passwd`
        - Check user groups: `groups username`
        - Add a user to a group: `sudo usermod -aG groupname username`
        - Remove a user from a group: `sudo gpasswd -d username groupname`
        - Check who is logged in: `who`
        - whoami: `whoami`

    - Home

        - Home directory: `/home/username`
        - Change home directory: `usermod -d /new/home/directory username`
        - Change ownership of home directory: `sudo chown username:groupname /home/username`
        - To view user information :
            - `cat /etc/passwd` # Contains user account information
            - `cat /etc/shadow` # Contains user password information
            - `cat /etc/group` # Contains group information
            - `cat /etc/gshadow` # Contains group password information 

            - `sudo cat /etc/passwd | grep username` # To view information for a specific user
            - `sudo cat /etc/shadow | grep /bin/bash` # To view users with bash shell
            - `sudo cat /etc/group | grep groupname` # To view information for a specific group
    - Permissions
        - Change file permissions: `chmod 755 filename`
        - Change file ownership: `chown username:groupname filename`
        - Check file permissions: `ls -l filename`
        - Set default permissions for new files: `umask 022`
        - Set sticky bit on a directory: `chmod +t /path/to/directory`
        - Set setuid and setgid bits: `chmod u+s filename` or `chmod g+s filename`


    - Firewall
        - Install UFW (Uncomplicated Firewall): `sudo apt-get install ufw`
        - Check firewall status: `sudo ufw status`
        - Enable firewall: `sudo ufw enable`
        - Disable firewall: `sudo ufw disable`
        - Allow a port: `sudo ufw allow 22/tcp` # Replace 22 with the desired port number
        - Deny a port: `sudo ufw deny 22/tcp`
        - Delete a rule: `sudo ufw delete allow 22/tcp`

    - Update system
        - Update package list: `sudo apt-get update`
        - Upgrade installed packages: `sudo apt-get upgrade`
        - Full upgrade (including kernel): `sudo apt-get dist-upgrade`
        - Remove unused packages: `sudo apt-get autoremove`
        - Clean up package cache: `sudo apt-get clean`

    - Official Sources

        - Official Ubuntu Security Notices: [link](https://ubuntu.com/security/notices)
        - Debian Security Advisories: [link](https://www.debian.org/security/)
        - Red Hat Security Advisories: [link](https://access.redhat.com/security/advisories)
        - CentOS Security Announcements: [link](https://lists.centos.org/pipermail/centos-announce/)
        - Arch Linux Security Advisories: [link](https://archlinux.org/security/)

    - Anti-Virus

        - Install ClamAV: `sudo apt-get install clamav`
        - Update ClamAV database: `sudo freshclam`
        - Scan a directory: `clamscan -r /path/to/directory`
        - Scan a file: `clamscan /path/to/file`
        - Remove infected files: `clamscan --remove=yes /path/to/directory`

    - Why Passwords?

        - Passwords are essential for securing user accounts and protecting sensitive information.
        - Strong passwords help prevent unauthorized access to systems and data.
        - Passwords should be unique, complex, and changed regularly to enhance security.

    - SSH (Secure Shell)

        - Install OpenSSH server: `sudo apt-get install openssh-server`
        - Start SSH service: `sudo systemctl start ssh`
        - Enable SSH service on boot: `sudo systemctl enable ssh`
        - Check SSH status: `sudo systemctl status ssh`
        - Connect to a remote server: `ssh username@remote_ip_address`
        - Change SSH port: Edit `/etc/ssh/sshd_config` and change the `Port` directive, then restart SSH service.
        - Disable root login via SSH: Edit `/etc/ssh/sshd_config` and set `PermitRootLogin no`, then restart SSH service.