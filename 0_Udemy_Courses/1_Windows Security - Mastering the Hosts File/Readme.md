# Notes taken from the Course

- Save using Notepad as Administrator, saving through VScode did not work

- either use `ping example.com` or go to `https://www.example.com/` to check if the website is blocked

- Hosts file:

    - The default path of the `hosts` file is `C:\Windows\System32\drivers\etc\hosts`
    - The `hosts` file is a text file that maps IP addresses to domain names.
    - The `hosts` file is used to speed up the DNS lookup process.
    - The `hosts` file is used to block ads and other unwanted content.
    - The `hosts` file is used to redirect to a local server.
    - The `hosts` file is used to redirect to a local server.

- Blocking Websites:

    - Add the following to the `hosts` file:
        
        - IP address followed by 2 tabs and then the domain name

        - `0.0.0.0 facebook.com`
        - `0.0.0.0 www.facebook.com`
        - `0.0.0.0 instagram.com`
        - `0.0.0.0 www.instagram.com`
        - `0.0.0.0 twitter.com` 
    
    - Save the `hosts` file
    - Restart the DNS client
    
        - `ipconfig /flushdns`

    - Check the DNS settings

        - `ipconfig /displaydns`

- Wild Card DNS:

    - Add the following to the `hosts` file:

        - `0.0.0.0        *`
        - `0.0.0.0        *.example.com` # Wildcard DNS, will block all subdomains of example.com

    - Save the `hosts` file
    - Restart the DNS client
    
        - `ipconfig /flushdns`

    - Check the DNS settings

        - `ipconfig /displaydns`

- Block Malware Domains:

    - Add the following to the `hosts` file:

        - `0.0.0.0        *.malware.com`

    - Save the `hosts` file
    - Restart the DNS client
    
        - `ipconfig /flushdns`

    - Check the DNS settings

        - `ipconfig /displaydns`

    - For reference, look into the repository `https://github.com/StevenBlack/hosts`


- Finding Lists:

    - use `https://filterlists.com/` to find lists of hosts files

- Custom Domains:

    - Add the following to the `hosts` file:

        - `127.0.0.1        aira.aramis.ai_dev`
        - `127.0.0.1        aira`
        
    - Save the `hosts` file
    
- GUI 

    - refer `https://hostsfileeditor.com/` for a GUI to edit the `hosts` file

- Linux:
    - `cd /etc` to navigate to the `etc` directory where the `hosts` file is located
    - `sudo nano /etc/hosts` to edit the `hosts` file

## Summary

### Key Points
1. File Location and Access
   - Hosts file is located at `C:\Windows\System32\drivers\etc\hosts`
   - Must be edited with administrator privileges (use Notepad as admin)

2. Basic Usage
   - Maps IP addresses to domain names
   - Speeds up DNS lookup process
   - Used for blocking content and local server redirection
   - Format: IP address + two tabs + domain name

3. Website Blocking
   - Use `0.0.0.0` as IP address for blocking
   - Must include both domain and www subdomain versions
   - After changes, flush DNS with `ipconfig /flushdns`
   - Verify with `ipconfig /displaydns`

4. Advanced Features
   - Wildcard DNS blocking: `0.0.0.0 *.example.com`
   - Can block all subdomains of a domain
   - Useful for blocking malware domains
   - Reference: StevenBlack/hosts repository

5. Custom Domain Configuration
   - Use `127.0.0.1` for local development
   - Can set up custom local domains

6. Tools and Resources
   - filterlists.com for finding host lists
   - hostsfileeditor.com for GUI editing
   - Linux path: `/etc/hosts`

### Quick Commands
- Check if site is blocked: `ping example.com` or visit the website
- Flush DNS cache: `ipconfig /flushdns`
- Display DNS cache: `ipconfig /displaydns`







