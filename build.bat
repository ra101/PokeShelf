@RD /S /Q .\Dist

pyinstaller -y -F -w --clean -i ./Assets/PokeShelf.ico^
 --collect-submodules tkinter --collect-submodules ctypes^
 --collect-submodules json --collect-submodules os^
 --collect-submodules functools^
 --add-data __init__.py;. --add-data app.py;. --add-data controllers.py;.^
 --add-data form_wids.py;. --add-data frames.py;. --add-data res_wids.py;.^
 --add-data utils.py;.^
 --add-data LICENSE;. --workpath .\Build --distpath .\Dist\PokeShelf^
 -n PokeShelf __main__.py

python post_build.py

@RD /S /Q .\Build
