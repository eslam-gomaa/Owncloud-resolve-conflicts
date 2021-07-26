#!/usr/bin/python
import re
import os
import requests
import urllib3



########################################
data_dir =  ""  # Example: "/var/www/html/owncloud/data/<account name>/files"
webdav = ""  # Example:  'https://<owncloud address>/remote.php/dav/files/<account name>/'
conflict_search = "*conflicted copy*"
usrename = '*****'
passowrd = '*****'
debug = True
########################################


def runcommand(cmd):
    import subprocess
    info = {}
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    info['cmd'] = cmd
    info['rc'] = proc.returncode
    info['stdout'] = std_out.rstrip()
    info['stderr'] = std_err.rstrip()
    ## Python's rstrip() method
    # strips all kinds of trailing whitespace by default, not just one newline
    return info



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = "\033[1;30;40m"


def get_file(url, user, password, verify=False):
    if not verify:
      urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'content-type': 'application/json'}
    request = requests.get(url, headers=headers, verify=verify, auth=requests.auth.HTTPBasicAuth(user, password))
    info = {}
    info['text'] = request.text
    info['status_code'] = int(request.status_code) # should return 200
    #print(request.reason)
    return info

def delete_file(url, user, password, verify=False):
    if not verify:
      urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'content-type': 'application/json'}
    request = requests.delete(url, headers=headers, verify=verify, auth=requests.auth.HTTPBasicAuth(user, password))
    info = {}
    info['text'] = request.text
    info['status_code'] = int(request.status_code)  # should return 204
    #print(request.reason)
    return info

def rename_file(file1_url, file2_url, user, password, verify=False):
    """
    Rename file1 to file2
    :param file1_url:
    :param file2_url:
    :param user:
    :param password:
    :param verify:
    :return:
    """
    if not verify:
      urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'content-type': 'application/json', 'Destination': file2_url}
    request = requests.move(file1_url, headers=headers, verify=verify, auth=requests.auth.HTTPBasicAuth(user, password))
    info = {}
    info['text'] = request.text
    info['status_code'] = int(request.status_code)  # should return 204
    #print(request.reason)
    return info


# Test
#get_file('https://<ip : port>/remote.php/dav/files/<account name>/<directory>/TEST%201.txt', usrename, passowrd)

conflicted = runcommand("""
cd {};
find  -name '{}'
""".format(data_dir, conflict_search))


if conflicted['stdout'].split("\n") == ['']:
    print("INFO -- No duplicates found")
    exit(0)

cnt_skipped = 0
cnt_resolved = 0
for f in conflicted['stdout'].split("\n"):
    print("INFO -- Found: {}".format(data_dir + re.sub('^\.', '', f)))
    original = re.sub(r'^\.', '', f)
    original = re.sub(r'\s+\(conflicted copy\s.*\d+-\d+-\d+\s\d+\)','', original)
    conflicted_mtime = os.path.getmtime(data_dir + re.sub('^\.', '', f))
    original_mtime = 0

    if os.path.isfile(data_dir + original):
        original_mtime = os.path.getmtime(data_dir + original)

    if original_mtime >= conflicted_mtime:
        if debug:
            print("INFO [ DEBUG ] -- Deleting the (conflicted file) --> The Original file is the newer (Latest modified)")

        print("INFO -- Deleting {}".format(f))
        if not os.path.isdir("/tmp/owncloud-tmp"):
            os.mkdir("/tmp/owncloud-tmp")

        remote_f = re.sub('^\.', '', f)
        remote_f = re.sub("\s", '%20', remote_f)
        remote_f = webdav + remote_f

        delete = delete_file(remote_f, usrename, passowrd)
        if debug:
            if delete['status_code'] == 204:
                print("INFO [ DEBUG ] -- File {} deleted successfully".format(remote_f))
            else:
                print("ERROR [ DEBUG ] -- could NOT delete the file {}".format(remote_f))
                print(delete)

    # delete the original and rename the duplicate
    elif conflicted_mtime > original_mtime:
        print("INFO -- Deleting the (Original file) --> The conflicted file is the newer (latest modified)")
        remote_f = re.sub('^\.', '', f)
        remote_f = re.sub("\s", '%20', remote_f)
        remote_f = webdav + remote_f

        remote_original = re.sub('^\.', '', original)
        remote_original = re.sub("\s", '%20', remote_original)
        remote_original = webdav + remote_original

        if debug:
            print("INFO [ DEBUG ] -- Deleting: '{}'".format(data_dir + original))
        check = get_file(remote_original, usrename, passowrd)
        if check['status_code'] == 404:
            if debug:
                print("WARN [ DEBUG ] -- File: {} does NOT exist, skiping deletion.".format(remote_original))
        elif check['status_code'] == 200:
            delete = delete_file(remote_original, usrename, passowrd)
            if debug:
                if delete['status_code']:
                    print("INFO [ DEBUG ] -- File {} deleted successfully".format(data_dir + original))
                else:
                    print("ERROR [ DEBUG ] -- failed to delete {}".format(data_dir + original))
                    if debug:
                        if delete['status_code'] != 200:
                            print(delete['text'])
                    print("INFO -- Skipping: {}".format(data_dir + original))
                    cnt_skipped += 1
                    continue
                    # exit(1)

        if debug:
            print("INFO [ DEBUG ] -- Renaming: '{}' to '{}'".format(data_dir +f, data_dir + original))
        rename = runcommand("curl -I -k -u {}:{} -X MOVE --header 'Destination:{}' '{}'".format(usrename, passowrd, remote_original, remote_f))
        if debug:
            if len(re.findall("200 OK", rename['stdout'])) > 0:
                print("INFO [ DEBUG ] -- File '{}' Renamed successfully to '{}'".format(data_dir + re.sub('^\.', '', f), data_dir + original))
            elif len(re.findall("403 Forbidden", rename['stdout'])) > 0:
                print("ERROR [ DEBUG ] -- Failed to rename the file\n")
                print("-" * 25)
                print("CMD: " + rename['cmd'])
                print("STDOUT: " + bcolors.OKGREEN + runcommand("curl -k -u {}:{} -X MOVE --header 'Destination:{}' '{}'".format(usrename, passowrd, remote_original, remote_f))['stdout'] + bcolors.ENDC)
                print("-" * 25)

#print("")
#print("Skipped: " + str(cnt_skipped))
#print("Resolved: "+ str(cnt_resolved))
