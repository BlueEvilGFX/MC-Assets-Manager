import json
import os
import urllib
from dataclasses import dataclass
from enum import Enum, auto
from threading import Thread

import requests

from MC_Assets_Manager.core.utils import icons, paths

class StatusEnum(Enum):
    INSTALLED = auto()
    UPDATEABLE = auto()
    INSTALLABLE = auto()

@dataclass
class DLCObject:
    name: str
    type: str
    creator: str
    installed_version: str
    online_version : str
    download_link: str
    status: StatusEnum

# Singleton
class GitHubReader:
    """
    Singleton class for GitHubReader
    """

    _instance = None

    _sta_url = "https://github.com"
    _api_url = "https://api.github.com"
    _raw_url = "https://raw.githubusercontent.com"
    _rep_owner = "BlueEvilGFX"
    _repo = "McAM-DLCs"

    _dlc_list = []
    _connection = None
    _news = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GitHubReader, cls).__new__(cls)
            # initialization
        return cls._instance
    
    #getter
    @property
    def url(self) -> str:
        return self._sta_url
    
    @property
    def api_url(self) -> str:
        return self._api_url
    
    @property
    def raw_url(self) -> str:
        return self._raw_url
    
    @property
    def rep_owner(self) -> str:
        return self._rep_owner
    
    @property
    def repo(self) -> str:
        return self._repo
       
    @property
    def dlc_list(self) -> list:
        return self._dlc_list
    
    @property
    def connection(self) -> bool:
        return self._connection
    
    @property
    def news(self) -> bool:
        return self._news
    
    #functions
    def _check_connection(self, timeout=5) -> bool:
        try:
            with urllib.request.urlopen(self._sta_url, timeout=timeout):
                return True
        except urllib.request.URLError as e:
            print(f"McAM: GitHub connection could not be established due to {str(e)}")
        except Exception as e:
            print(f"McAM: An unexpected error occurred: {str(e)}")
        return False
    
    def connect(self) -> bool:
        self._connection = self._check_connection()
        if not self._connection:
            print("McAM: Connection check failed")
            return False
        
        if not self._fetch_data():
            print("McAM: Data fetch failed")
            return
        
        if not self._check_dlc_updates():
            print("McAM: DLC update check failed")
            return
        
        if not self._fetch_icons():
            print("McAM: Icon fetch failed")
            return
        
        print("McAM: Successfull connection to GitHub")
        return True

    def connect_threaded(self):
        Thread(target=self.connect).start()

    def _fetch_data(self) -> bool:
        raw_url = f'{self._raw_url}/{self._rep_owner}/{self._repo}/main'
        dlc_url = f'{raw_url}/dlc.json'

        try:
            dlc_json = requests.get(dlc_url).json()
        except requests.exceptions.RequestException as e:
            print(f"McAM: Error fetching DLC list: {e}")
            return False

        self._dlc_list.clear()
        for dlc in dlc_json:
            data_url = f'{raw_url}/{dlc}/data.json'
            try:
                data = requests.get(data_url).json()
            except requests.exceptions.RequestException as e:
                print(f"McAM: Error fetching data for {dlc}: {e}")
                continue

            dlc_object_data = {
                'name': dlc,
                'type': data.get('type'),
                'creator': data.get('creator'),
                'installed_version': None,
                'online_version': data.get('version'),
                'download_link': data.get('download_link'),
                'status': None
            }
            self._dlc_list.append(DLCObject(**dlc_object_data))

        return True
    
    def _check_dlc_updates(self) -> bool:
        if not self._dlc_list:
            self._news = False
            return False

        dlc_json = paths.McAM.get_dlc_main_json()

        try:
            with open(dlc_json, 'r') as j_data:
                j_data = json.load(j_data)
        except FileNotFoundError:
            print(f"McAM: File {dlc_json} not found.")
            return
        except json.JSONDecodeError:
            print(f"McAM: Error decoding JSON from {dlc_json}.")
            return

        for dlc in self._dlc_list:
            if dlc.name not in j_data:
                dlc.status = StatusEnum.INSTALLABLE
            else:
                dlc.installed_version = j_data[dlc.name]["version"]
                if any(x < y for x, y in zip(dlc.installed_version, dlc.online_version)):
                    dlc.status = StatusEnum.UPDATEABLE
                else:
                    dlc.status = StatusEnum.INSTALLED

        self._news = any(dlc.status is not StatusEnum.INSTALLED for dlc in self._dlc_list)
        return True
    
    def _fetch_icons(self) -> None:
        dir_github_icons = paths.McAM.get_github_icon_directory()
        if not os.path.exists(dir_github_icons):
            os.makedir(dir_github_icons)

        for file in os.listdir(dir_github_icons):
            os.remove(os.path.join(dir_github_icons, file))

        success = True
        for dlc in self._dlc_list:
            try:
                sta, owner = self._sta_url, self._rep_owner 
                url = f'{sta}/{owner}/{self._repo}/raw/main/{dlc.name}/icon.png'
                save_location = os.path.join(dir_github_icons, f'{dlc.name}.png')
                urllib.request.urlretrieve(url, save_location)
            except urllib.error.URLError as e:
                pass
                # dlc just has no name icon to fetch -> no error
                # print(f"McAM: Error fetching icon for {dlc.name}: {e}")
                # success = False
            except Exception as e:
                print(f"McAM: Unexpected error occurred: {e}")
                success = False
                continue
        icons.reload_github_dlc_icons()
        return success