@RD /S /Q .\Dist
@RD /S /Q .\__pycache__

pyinstaller -y -F -w --clean -i ./Assets/PokeShelf.ico^
 --collect-submodules tkinter.font --collect-submodules tkinter.filedialog^
 --collect-submodules tkinter.messagebox --collect-submodules psutil.__init__^
 --collect-submodules ctypes.windll --collect-submodules json^
 --collect-submodules pyo.__init__ --collect-submodules pyo.server --collect-submodules pyo.players^
 --collect-submodules PIL.Image --collect-submodules PIL.ImageTk^
 --exclude-module PIL.ImageFilter --collect-submodules PIL.ImageOps^
 --collect-submodules av --collect-submodules tkVideoPlayer^
 --collect-submodules pystray^
 --add-data __init__.py;. --add-data app.py;. --add-data utils.py;.^
 --add-data form_wids.py;. --add-data frames.py;. --add-data res_wids.py;.^
 --workpath .\Build --distpath .\Dist\PokeShelf --add-data LICENSE;.^
 -n PokeShelf __main__.py

python post_build.py

@RD /S /Q .\Build
@RD /S /Q .\..build
@RD /S /Q .\__main__.build
