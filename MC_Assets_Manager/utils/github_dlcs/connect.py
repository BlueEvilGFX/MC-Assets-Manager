import requests, os, json, urllib
from enum import Enum, auto

from . import operators
from .. import utils
from .icons import read_github_dlc_icons

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class StatusEnum(Enum):
    INSTALLED = auto()
    UPDATEABLE = auto()
    INSTALLABLE = auto()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLCObject:
    def __init__(self, data, dlc) -> None:
        self.name = dlc
        self.type = data["type"]
        self.creator = data["creator"]
        self.version = data["version"]
        self.download_link = data["download_link"] if "download_link" in data else None
        self.status = None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GithubReader:
    sta_url = "https://github.com"
    api_url = "https://api.github.com"
    raw_url = "https://raw.githubusercontent.com"
    rep_owner = "BlueEvilGFX"
    repo = "McAM-DLCs"

    def __init__(self) -> None:
        self.dlc_list = []
        self.network_error = None

        self.check_internet_connection()
        if self.network_error: return
        self.fetch_data()
        self.check_dlcs()
        self.fetch_icons()

    def check_internet_connection(self) -> bool:
        try:
            urllib.request.urlopen("https://github.com")
            self.network_error = False
            return True
        except:
            print("McAM: Wifi connection could not been found")
            self.network_error = True
            return False

    def fetch_data(self) -> None:
        if self.network_error: return

        raw_url = "%s/%s/%s/main" % (self.raw_url, self.rep_owner, self.repo)
        dlc_url = "%s/dlc.json" % raw_url

        self.dlc_list.clear()
        dlc_json = requests.get(dlc_url).json()
        
        for dlc in dlc_json:
            data_url = "%s/%s/data.json" % (raw_url, dlc)
            data = requests.get(data_url).json()
            self.dlc_list.append(DLCObject(data, dlc))

    def check_dlcs(self) -> None:
        if self.network_error: return

        file_path = os.path.realpath(__file__)
        utils_path = os.path.dirname(file_path)
        path = os.path.dirname(os.path.dirname(utils_path))
        path = os.path.join(path, "files", "dlcs.json")

        with open(path, "r") as jFile:
            jData = json.load(jFile)

        for dlc in self.dlc_list:
            if not dlc.name in jData:
                dlc.status = StatusEnum.INSTALLABLE
            else:
                i_version = eval(jData[dlc.name]["version"])
                g_version = eval(dlc.version)

                for idx, x  in enumerate(i_version):
                    if x < g_version[idx]:
                        dlc.status = StatusEnum.UPDATEABLE
                        break
                    else:
                        dlc.status = StatusEnum.INSTALLED
        operators.set_news(False)

    def fetch_icons(self) -> None:
        addon_path = utils.AddonPathManagement.getAddonPath()
        icons_dir = os.path.join(addon_path, "utils", "github_dlcs", "icons")
        if os.path.exists(icons_dir):
            for files in os.listdir(icons_dir):
                os.remove(os.path.join(icons_dir, files))
        else:
            os.mkdir(icons_dir)

        for dlc in self.dlc_list:
            try:
                url = "%s/%s/%s/raw/main/%s/icon.png" % (self.sta_url, self.rep_owner, self.repo, dlc.name)
                save_location = os.path.join(icons_dir, "%s.png" % dlc.name)
                urllib.request.urlretrieve(url, save_location)
            except:
                pass

        read_github_dlc_icons()