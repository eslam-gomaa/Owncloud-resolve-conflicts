# Owncloud-cesolve-conflicts
A Python script to resolve OwnCloud conflicted files. (From the server side)


## Prerequisites

1. Get the WebDav address of your owncloud


---


2. Install the required libraries

```bash
pip install requests
```



## Usage


Run the script

```bash
python owncloud-solve-conflicts.py
```

Or

```bash
chmod +x owncloud-solve-conflicts.py
./owncloud-solve-conflicts.py
```


### Prefered way to use it

```bash
crontab -e
```

```bash
*/5 * * * * /root/conflict.py >> /var/log/messages
```
This will run the script every 5 minutes, anse send the output to `/var/log/messages`


---

.

### Please leave a ⭐ if you found it useful

.

Thank you

Maintainer: [Eslam Gomaa](https://www.linkedin.com/in/eslam-gomaa)

