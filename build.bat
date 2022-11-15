@RD /S /Q .\Dist

pyinstaller -y -F -w --clean -i ./Assets/PokeShelf.ico^
 --collect-submodules tkinter.font --collect-submodules tkinter.filedialog^
 --collect-submodules ctypes.windll --collect-submodules json^
 --collect-submodules tkVideoPlayer^
 --collect-submodules pystray^
 --add-data __init__.py;. --add-data app.py;. --add-data utils.py;.^
 --add-data form_wids.py;. --add-data frames.py;. --add-data res_wids.py;.^
 --workpath .\Build --distpath .\Dist\PokeShelf --add-data LICENSE;.^
 -n PokeShelf __main__.py --key %SHELF_KEY%

python post_build.py

@RD /S /Q .\Build
