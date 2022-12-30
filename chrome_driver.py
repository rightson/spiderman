import os
import sys
import requests
import zipfile
from pathlib import Path
from win32com.client import Dispatch


LOCAL_CHROME_PATHS = [r'C:/Program Files/Google/Chrome/Application/chrome.exe',
                      r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe']
DRIVER_URL = 'http://chromedriver.storage.googleapis.com'


def getVersionViaCom(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def getChromeVersion():
    return list(filter(None, [getVersionViaCom(p) for p in LOCAL_CHROME_PATHS]))[0]


def downloadFile(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    return local_filename


def unzipFile(zip_path, directory_to_extract_to='.'):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def downloadInstallChromeDriver(chrome_version, major_version, chromedriver_path):
    try:
        print('Auto downloading chromedriver for Chrome version %s' %
              chrome_version)
        r = requests.get('%s/LATEST_RELEASE_%s' % (DRIVER_URL, major_version))
        r.raise_for_status()
        tarball_name = 'chromedriver_win32.zip'
        url = '%s/%s/%s' % (DRIVER_URL, r.text, tarball_name)
        print('Installing chromedriver for Chrome version %s' % chrome_version)
        unzipFile(downloadFile(url))
        filename = Path('chromedriver.exe')
        if not os.path.exists(chromedriver_path):
            Path(chromedriver_path).parent.mkdir(parents=True, exist_ok=True)
            filename.rename(chromedriver_path)
        else:
            os.unlink(filename)
        if os.path.exists(tarball_name):
            os.unlink(tarball_name)
        return chromedriver_path
    except Exception as e:
        print('Error: chromedriver not found in $PATH (%s)' % e)
        input('Press Enter to continue')
        sys.exit(-1)


def getChromeDriver(force=False, version_uniquify=True):
    try:
        chrome_version = getChromeVersion()
        major_version = chrome_version.split('.')[0]
        if version_uniquify:
            chromedriver_path = './bin/chromedriver-%s.exe' % major_version
        else:
            chromedriver_path = './bin/chromedriver.exe'
        if os.path.exists(chromedriver_path) and not force:
            return chromedriver_path
        print('Warning: chromedriver for Chrome version %s not found' %
              chrome_version)
        return downloadInstallChromeDriver(chrome_version, major_version, chromedriver_path)
    except Exception as e:
        print('Error: unable to detect chrome version! (%s)' % e)
        input('Press Enter to continue')
        sys.exit(-1)