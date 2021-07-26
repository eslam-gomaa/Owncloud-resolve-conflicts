# Owncloud-cesolve-conflicts
A Python script to resolve OwnCloud conflicted files. (From the server side)


## Prerequisites

1. Get the WebDav address of your owncloud 

Can be found at the bottom left of the owncloud home page

![image](https://user-images.githubusercontent.com/33789516/126978695-edbfdecd-eaae-4882-8fb7-27c76c479ead.png)


---


2. Install the required libraries

```bash
pip install requests
```



## Usage

### Configure the script

Open the script and provided the needed parameters

![image](https://user-images.githubusercontent.com/33789516/126977861-4ea57a00-918f-4da8-9ca5-ecbf088d0cd3.png)


| Variable | Description                         |
| ---------- | ------------------------------------- |
| data_dir | Owncloud data directory (on the OS) |
| webdav   | your Owncloud webdav link           |
| usrename | Owncloud account username           |
| passowrd | Owncloud account password           |

---

Run the script

```bash
python owncloud-solve-conflicts.py
```

Or

```bash
chmod +x owncloud-solve-conflicts.py
./owncloud-solve-conflicts.py
```

Note: The script tested with `python2` but should be working with `python3` as well.

### Prefered way to use it

```bash
crontab -e
```

```bash
*/5 * * * * /root/owncloud-solve-conflicts.py >> /var/log/messages
```
* Make sure you modify the script directory if different.
This will run the script every 5 minutes, anse send the output to `/var/log/messages`


---

.

### Please leave a ⭐ if you found it useful

.

Thank you

Maintainer: [Eslam Gomaa](https://www.linkedin.com/in/eslam-gomaa)

