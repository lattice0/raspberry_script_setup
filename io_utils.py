import os
import sys
import re #regex
import requests
import shutil

#INPUT/OUTPUT TOOLS -------------------------------------
def log(message):
    print(message + "...")

def read_file(path):
    f = open(path,'r')
    filedata = f.read()
    f.close()
    return filedata

def touch(path): #https://stackoverflow.com/a/6222692
    if os.path.exists(path):
        os.utime(path, None)
    else:
        open(path, 'a').close()

def remove_file(path, do_backup=False):
    if do_backup:
        backup_file(path)
    log("Removing file " + path)
    try:
        os.remove(path)
    except:
        log("Something went wrong or file doesn't exist anymore")

#https://stackoverflow.com/a/22876912
def backup_file(path): #Todo: do backup of symlinks. Actually, modify read_file() to always follow symlinks
    log("Creating backup of " + path)
    f = open(path,'r')
    filedata = f.read()
    f.close()
    f = open(path+".backup",'w')
    f.write(newdata)
    f.close()

def file_exists(path):
    return os.path.isfile(fname)

def is_symlink(path):
    return os.path.islink(path)
      
def list_files(path):
    listOfFiles = [f for f in os.listdir(path) if is_symlink(path.rpartition("/")[0]+"/"+f)]
    return listOfFiles

def modify_file_permissions(file, new_permission):
    log("Modifying permissions of " + file + " to " + oct(new_permission))
    #Read about python permissions nomenclature: https://docs.python.org/3/library/stat.html#stat.S_IRWXU
    os.chmod(file, new_permission)

def modify_ownership(file, root_dir, user, group):
    log("Modifying ownership of " + file + " to user " + user + " and group " + group)
    regex = "\w+:\w+:\d+:\d+:[\w\d\s,@()]*:[\w\d\s\/]*:[\d\s\w\/]*"
    passwd_file = read_file(root_dir + "/etc/passwd")
    passwd_regex_user = "(" + user + "):(\w+):(\d+):(\d+):([\w\d\s,@()]*):([\w\d\s\/]*):([\d\s\w\/]*)"
    passwd_search_user = re.search(passwd_regex_user, passwd_file)
    uid = passwd_search_user.group(3)
    passwd_regex_group = "(" + group + "):(\w+):(\d+):(\d+):([\w\d\s,@()]*):([\w\d\s\/]*):([\d\s\w\/]*)"
    passwd_search_group = re.search(passwd_regex_group, passwd_file)
    gid = passwd_search_group.group(4)
    os.chown(file, int(uid), int(gid))
'''
Usage: 
rename_file("path/to/my/old_file_name", "new_file_name") will change path/to/my/old_file_name to path/to/my/new_file_name
or
rename_file("old_file_name", "new_file_name") will change old_file_name to new_file_name (locally)
'''
def rename_file(file, new_name):
    log("Renaming " + file + " to " + new_name)
    partition = file.rpartition("/") #https://docs.python.org/3/library/stdtypes.html#str.rpartition
    new_file = partition[0] + partition[1] + new_name
    os.rename(file, new_file)
    #print("should rename " + file + " to " + new_file) #https://docs.python.org/3/library/os.html#os.rename

#Creates OR rewrites a file if it exists
def create_file(path, content, permission=None):
    log("Creating " + path)    
    make_path(path)
    f = open(path,'w')
    f.write(content)
    f.close()
    if permission:
        modify_file_permissions(path, permission)

#Creates OR rewrites a file if it exists
def create_or_append_to_file(path, content, permission=None):
    log("Creating or appending to  " + path)    
    make_path(path)
    f = open(path,'a')
    f.write(content)
    f.close()
    if permission:
        modify_file_permissions(path, permission)


def edit_file(path, rules, backup=True):
    log("Editing " + path)    
    backup_file(path)
    content = replace(read_file(path), rules)
    create_file(path, content)

#https://stackoverflow.com/a/12517490
def make_path(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def replace(content, rules):
    for rule in rules:
	#https://stackoverflow.com/a/1687663
        content = re.sub(re.compile(rule[0], re.MULTILINE), rule[1], content, 0)
    return content

def add_quotation(string):
    return "\"" + string + "\""

def copy(source, destination):
    shutil.copy(source, destination)

def copy_with_permissions(source, destination):
    shutil.copy2(source, destination)

#https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url):
    log("Downloading " + path)    
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return local_filename

