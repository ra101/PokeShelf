import os, json, shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(os.path.join(base_dir, 'Dist'), 'PokeShelf')

base_adir = os.path.join(base_dir, 'Assets')
dist_adir = os.path.join(dist_dir, 'Assets')

req_assets = ['pkmnem.ttf', 'PokeShelf.ico', 'default.ogg']


with open(os.path.join(dist_dir, 'config.json'), "w") as f:
    json.dump({
        "screenSize": "M", "musicVolume": 100, "gameOrder": [],
        "GBEmulator": "", "DSEmulator": "", "systemTray": False, "gameList": []
    }, f, indent=4)

os.mkdir(dist_adir)

for file in req_assets:
    shutil.copy(os.path.join(base_adir, file), dist_adir)

shutil.make_archive(dist_dir, 'zip', dist_dir)
