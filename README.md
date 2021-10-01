# Owncloud-resolve-conflicts
A Python script to resolve OwnCloud conflicted files. (From the server side)


### Approach

When the script is executed (usually periodically via `crontab`) it looks if there are any conflicted files, If a conflicted file found it gets compared with its original file and the last modification wins

**Note:** I've been using this script for months and works like a charm, if you faced an error please let me know

---


## Prerequisites

1. Get the WebDav address of your owncloud 


<details>
    <summary>
        <b style="font-size:10px"><mark style="background-color: #fffccd">
            Can be found at the bottom left of the owncloud home page
            </mark></b>
    </summary>
  
  <img src="https://user-images.githubusercontent.com/33789516/126978695-edbfdecd-eaae-4882-8fb7-27c76c479ead.png">
  
</details>


---


2. Install the required libraries

```bash
pip install requests
```

---

3. Configure Owncloud to upload the conflicted files

<details>
    <summary>
        <b style="font-size:20px"><mark style="background-color: #fffccd">
            On Windows
            </mark></b>
    </summary>
  
  <img src="https://user-images.githubusercontent.com/33789516/135644695-f086fa7b-95a3-437b-b525-4188cb322ba9.png">
   <br>
   <br>
   Variable: <code>OWNCLOUD_UPLOAD_CONFLICT_FILES</code>
   <br>
   Value: <code>1</code>
   <br>
   <br>
  <img src="https://user-images.githubusercontent.com/33789516/135644351-346afb3d-039d-4f43-bf85-c4b605f5bfd5.png">
  
</details>


<details>
    <summary>
        <b style="font-size:20px"><mark style="background-color: #fffccd">
            On Linux
            </mark></b>
    </summary>
  
  ```bash
  export OWNCLOUD_UPLOAD_CONFLICT_FILES=1
  ```
  
</details>


---


## Usage

### Configure the script

Open the script and provide the needed parameters

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

**Note:** The script tested with `python2` but should be working with `python3` as well.

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

