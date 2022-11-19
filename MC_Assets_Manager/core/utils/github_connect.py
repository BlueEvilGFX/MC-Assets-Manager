import json
import os
import urllib
from dataclasses import dataclass
from enum import Enum, auto
from threading import Thread

import requests

from MC_Assets_Manager.core.utils import icons, paths

github_reader = None

def connect():
    global github_reader
    github_reader = GitHubReader()

class StatusEnum(Enum):
    INSTALLED = auto()
    UPDATEABLE = auto()
    INSTALLABLE = auto()

@dataclass
class DLCObject:
    name: str
    type: str
    creator: str
    version: str
    download_link: str
    status: StatusEnum

def _creating_reader():
    global github_reader
    github_reader = GitHubReader(True)

def auto_check() -> None:
    Thread(target=_creating_reader).start()
    print("after thread start")

class GitHubReader:
    sta_url = "https://github.com"
    api_url = "https://api.github.com"
    raw_url = "https://raw.githubusercontent.com"
    rep_owner = "BlueEvilGFX"
    repo = "McAM-DLCs"

    def __init__(self, initializing = True) -> None:
        self.dlc_list = []
        self.network_connection = None
        self.news = None

        if not initializing:
            return

        if not self.check_internet_connection():
            self.network_connection = False
            return
        else:
            self.network_connection = True

        self.fetch_data()
        self.check_dlcs()
        self.fetch_icons()        

    def check_internet_connection(self) -> bool:
        try:
            urllib.request.urlopen(self.sta_url)
            return True
        except:
            print("McAM: Wifi connection coul not been found")
            return False

    def fetch_data(self) -> bool:
        raw_url = f'{self.raw_url}/{self.rep_owner}/{self.repo}/main'
        dlc_url = f'{raw_url}/dlc.json'

        self.dlc_list.clear()
        dlc_json = requests.get(dlc_url).json()
        for dlc in dlc_json:
            data_url = f'{raw_url}/{dlc}/data.json'
            data = requests.get(data_url).json()

            self.dlc_list.append(
                DLCObject(
                    dlc,
                    data["type"],
                    data["creator"],
                    data["version"],
                    data["download_link"] if "download_link" in data else None,
                    None
                    ))

    def check_dlcs(self) -> None:
        dlc_json = paths.get_dlc_json()
        
        with open(dlc_json, 'r') as j_data:
            j_data = json.load(j_data)
            
            for dlc in self.dlc_list:
                if not dlc.name in j_data:
                    dlc.status = StatusEnum.INSTALLABLE
                else:
                    i_version = eval(j_data[dlc.name]["version"])
                    g_version = eval(dlc.version)

                    for idx, x  in enumerate(i_version):
                        if x < g_version[idx]:
                            dlc.status = StatusEnum.UPDATEABLE
                            break
                        else:
                            dlc.status = StatusEnum.INSTALLED
            
            self.news = any(
                dlc.status is not StatusEnum.INSTALLED for dlc in self.dlc_list
                )
    
    def fetch_icons(self) -> None:
        dir_github_icons = os.path.join(paths.RESOURCES_DIR, "github_icons")
        if not os.path.exists(dir_github_icons):
            os.mkdir(dir_github_icons)
        else:
            for files in os.listdir(dir_github_icons):
                os.remove(os.path.join(dir_github_icons, files))
        
        for dlc in self.dlc_list:
            try:
                sta, owner = github_reader.sta_url, github_reader.rep_owner 
                repo, name = github_reader.repo, dlc.name          
                url = f'{sta}/{owner}/{repo}/raw/main/{name}/icon.png'
                save_location = os.path.join(dir_github_icons, f'{dlc.name}.png')
                urllib.request.urlretrieve(url, save_location)
            except:
                pass
        icons.reload_github_dlc_icons()