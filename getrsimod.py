import sys
import shutil
from time import sleep
from pathlib import Path
from getpass import getpass
from datetime import datetime
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP
from bs4 import BeautifulSoup as Soup
from jnpr.junos.utils.start_shell import StartShell

#rpcreply = '<rpc-reply xmlns:junos="http://xml.juniper.net/junos/12.1X46/junos"><directory-list root-path="/var/crash/*core*" seconds="1549057102" style="verbose"><output>/var/crash/*core*: No such file or directory</output><directory name=""><file-information><file-name>/var/tmp/rpd.core.0.gz</file-name><file-permissions format="-rw-rw----">660</file-permissions><file-owner>root</file-owner><file-group>wheel</file-group><file-links>1</file-links><file-size>3556567</file-size><file-date format="Feb 1  21:37">1549057078</file-date></file-information><output>/var/tmp/pics/*core*: No such file or directory</output><output>/var/crash/kernel.*: No such file or directory</output><output>/tftpboot/corefiles/*core*: No such file or directory</output><total-files>1</total-files></directory></directory-list>'
#[filename, coredump, corefiles]


def getRSI(hostname, username, password, _dir, rsi, varlog, both):
    """
    1. Create a directory
    2. Download the files to the directory
    3. Compress files
    4. Send file to the 
    """
    try:
        dev = Device(host=hostname, user=username,
                     passwd=password, gather_facts=False)

        dev.open()
        now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        _dir = _dir + "/"
        rsidirectory = _dir + dev.facts['hostname'] + "_" + now
        Path(rsidirectory).mkdir(parents=True, exist_ok=True)
        rsifile = dev.facts['hostname'] + '_rsi_' + now
        varlogs = dev.facts['hostname'] + '_varlogs_' + now + '.tgz'
        shl = StartShell(dev)
        shl.open()
        if rsi is True:
            print("Running RSI..")
            shl.run('cli -c "request support information | save /var/tmp/' + rsifile + '"', timeout=1800)
            with SCP(dev) as scp:
                print("SCP Transferring files")
                scp.get("/var/tmp/" + rsifile, local_path=rsidirectory)
            print("SCP Completed")
            shl.close()
            filename = dev.facts['hostname'] + "_" + now + "/" + rsifile
        elif varlog is True:
            print("Running archive..")
            shl.run('cli -c "file archive compress source /var/log/* destination /var/tmp/' + varlogs + '"', timeout=1800)
            with SCP(dev) as scp:
                print("SCP Transferring files")
                scp.get("/var/tmp/" + varlogs, local_path=rsidirectory)
            print("SCP Completed")
            shl.close()
            filename = dev.facts['hostname'] + "_" + now + "/" + varlogs
        else:
            print("Running RSI..")
            shl.run('cli -c "request support information | save /var/tmp/' + rsifile + '"', timeout=1800)
            print("Running archive..")
            shl.run('cli -c "file archive compress source /var/log/* destination /var/tmp/' + varlogs + '"', timeout=1800)
            with SCP(dev) as scp:
                print("SCP Transferring files")
                scp.get("/var/tmp/" + rsifile, local_path=rsidirectory)
                scp.get("/var/tmp/" + varlogs, local_path=rsidirectory)
            print("SCP Completed")
            shl.close()
            # Archive everything
            archivedfile = dev.facts['hostname'] + "_support_info_" + now
            shutil.make_archive(_dir + archivedfile, 'zip', rsidirectory)
            archivedfile += ".zip"
            print("Archive file name: " + archivedfile)
            filename = archivedfile
        # Check for Core Dumps by requsting RPC
        rpcjson = []
        rpcreply = "blah"  # <-- This is where you'll call the core dump rpc
        if 'total-files' in rpcreply:
            coredump = True
            # make the soup
            soup = Soup(rpcreply, 'xml')
            rpcdata = soup.select("file-information")
            for num, file in enumerate(rpcdata):
                epochtime = int(file.select("file-date")[0].get_text())
                timestr = datetime.datetime.utcfromtimestamp(
                    epochtime).strftime('%b-%d-%Y %H:%M:%S')

                rpcjson.append({"filename": file.select(
                    "file-name")[0].get_text(), "time": timestr})
            print(rpcjson)
        else:
            coredump = False

    except Exception as err:
        dev.close()
        print ("ERROR Caught!")
        print (err)
        return err

    dev.close()
    return filename, coredump, rpcjson


"""
def getRSI(hostname):
    sleep(8)
    if hostname == "error":
        raise Exception("This is an error msg")
        return False
    if 'total-files' in rpcreply:
        coredump = True
        # make the soup
        soup = Soup(rpcreply, 'xml')
        rpcjson = []
        rpcdata = soup.select("file-information")
        for num, file in enumerate(rpcdata):
            epochtime = int(file.select("file-date")[0].get_text())
            timestr = datetime.datetime.utcfromtimestamp(
                epochtime).strftime('%b-%d-%Y %H:%M:%S')

            rpcjson.append({"filename": file.select(
                "file-name")[0].get_text(), "time": timestr})
    else:
        coredump = False
    return coredump, rpcjson
"""
