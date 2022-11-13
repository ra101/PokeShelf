import os, json, sys
import tkinter as tk
from functools import partial

from PIL import Image
from pystray import Icon as Tray, MenuItem as TrayCmd

import frames, controllers
from utils import load_unload_font
from form_wids import DialogBox


class ShelfApp(tk.Tk):

  def __init__(
      self, screenName=None, baseName=None,
      className='Tk', useTk=True, sync=False, use=None
    ):
    super().__init__(screenName, baseName, className, useTk, sync, use)

    self.init_vars()
    self.init_frames()

  def mainloop(self, n=0):
    self.init_screen()
    self.bind_keys()
    self.setup_screen()
    return super().mainloop(n)

  def destroy(self):

    if self.ST and self.icon_path:
      if not self.system_tray:
        self.start_tray()
        return
      else:
        self.stop_tray()

    if self.asset_dir:
      for file in os.listdir(self.asset_dir):
        if file.endswith('.ttf'):
          load_unload_font(
            os.path.join(self.asset_dir, file), load=False
          )

    return super().destroy()

  def lift(self):
    super().lift()

    self.attributes('-topmost', 1)
    self.focus_force()
    self.after_idle(self.attributes,'-topmost',False)

  def init_vars(self):
    self.base_dir, self.asset_dir, self.icon_path = None, None, None
    self.dialog_box, self.system_tray = None, None

    if getattr(sys, 'frozen', False):
      self.base_dir = os.path.dirname(sys.executable)
    elif __file__:
      self.base_dir = os.path.dirname(os.path.abspath(__file__))

    if 'Assets' in os.listdir(self.base_dir):
      self.asset_dir = os.path.join(self.base_dir, 'Assets')

    self.init_config()
    self.load_fonts()

    self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT = 512, 384
    self.RES = dict(S=0.5, M=1, L=1.5, XL=2, FS=2.5)
    self.RES['FS'] = self.winfo_screenheight()/self.DEFAULT_HEIGHT

    self.controller = controllers.ShelfController(self)

  def init_config(self):
    self.config_file = os.path.join(self.base_dir, 'config.json')

    if "config.json" not in os.listdir(self.base_dir):
      config_data = {}

      config_data['screenSize'] = self.SS = "M"
      config_data['musicVolume'] = self.MV = 100
      config_data['gameOrder'] = self.GO = []
      config_data['GBEmulator'] = self.GB = ""
      config_data['DSEmulator'] = self.DS = ""
      config_data['systemTray'] = self.ST = False
      config_data['gameList'], self.GD = [], {}

      with open(self.config_file, "w") as f:
        json.dump(config_data, f, indent=4)

    else:

      with open(self.config_file, "r") as config_file:
        config_data = json.load(config_file)

        self.SS = config_data.get("screenSize", "M")
        self.MV = config_data.get("musicVolume", 10)
        self.GO = config_data.get("gameOrder", [])
        self.GB = config_data.get("GBEmulator", "")
        self.DS = config_data.get("DSEmulator", "")
        self.ST = bool(config_data.get("systemTray", False))
        self.GD = { i['oid']: i for i in config_data.get("gameList", []) }

  def save_config(self):
    self.config_file = os.path.join(self.base_dir, 'config.json')

    with open(self.config_file, "w") as f:
      json.dump({
        "screenSize": getattr(self, "SS", "M"),
        "musicVolume": getattr(self, "MV", 100),
        "gameOrder": getattr(self, "GO", []),
        "GBEmulator": getattr(self, "GB", ""),
        "DSEmulator": getattr(self, "DS", ""),
        "systemTray": bool(getattr(self, "ST", False)),
        "gameList": list(getattr(self, "GD", {}).values()),
      }, f, indent=4)

  def init_screen(self):
    self.title('PokéShelf')
    self.resizable(False, False)
    self.configure(background='black')

    self.init_icon()
    self.init_menu()

  def init_icon(self):
    if not self.asset_dir:
      return

    for file in os.listdir(self.asset_dir):
      if file.endswith('.ico'):
        self.icon_path = os.path.join(self.asset_dir, file)
        self.iconbitmap(self.icon_path)
        return

  def init_frames(self):
    frames.OptionsFrame(self)
    frames.AboutFrame(self)
    frames.GameSettingsFrame(self)
    frames.ShelfFrame(self)
    frames.SplashFrame(self)

  def init_menu(self):
    menu_bar = tk.Menu(self, name="menu")
    game_menu = tk.Menu(menu_bar, tearoff=False, name="game")

    game_menu_data = [
      {"lbl": "📚 PokéShelf", 'func': 'toggle_frame', 'func_arg': ['shelf'], 'con':'s'}, {'sep': True},
      {"lbl": "➕ Add Game", 'func': 'toggle_frame', 'func_arg': ['gamesettings'], 'con':'a'},
      {"lbl": "🔧 Edit Game", 'func': 'toggle_frame', 'func_arg': ['gamesettings', {'edit':True}], 'con':'e'},
      {"lbl": "➖ Remove Game", 'func': 'remove_game', 'con':'r'},
      {'sep': True}, {"lbl": "❌ Close Menu"},
    ]

    for data in game_menu_data:
      is_sep, command = data.get('sep', False), data.get('func', None)

      if is_sep:
        game_menu.add_separator()
        continue

      command = partial(getattr(self, command), *data.get('func_arg', [])) if command else None

      game_menu.add_command(label=data['lbl'], command=command)

      if command:
        func = partial(self.controller.shortcut, menu=game_menu, lbl=data['lbl'], cmd=command)
        self.bind(f'<Control-{data["con"].lower()}>', func)
        self.bind(f'<Control-{data["con"].upper()}>', func)

    menu_bar.add_cascade(label="🎮 Game", menu=game_menu)

    label, command = "⚙️ Options", partial(self.toggle_frame, "options")
    menu_bar.add_command(label=label, command=command)
    self.bind(f'<Alt-s>', partial(self.controller.shortcut, menu=menu_bar, lbl=label, cmd=command))
    self.bind(f'<Alt-S>', partial(self.controller.shortcut, menu=menu_bar, lbl=label, cmd=command))

    label, command = "💡 About", partial(self.toggle_frame, "about")
    menu_bar.add_command(label=label, command=command)
    self.bind(f'<Alt-a>', partial(self.controller.shortcut, menu=menu_bar, lbl=label, cmd=command))
    self.bind(f'<Alt-A>', partial(self.controller.shortcut, menu=menu_bar, lbl=label, cmd=command))

    self.config(menu=menu_bar)

  def init_tray(self):
    self.system_tray = Tray(
      name="PokéShelf : Tray", title="PokéShelf",
      icon=Image.open(self.icon_path),
      menu=(
        TrayCmd('PokéShelf', partial(self.stop_tray, fr="splash")),
        TrayCmd('Options', partial(self.stop_tray, fr="options")),
        TrayCmd('About', partial(self.stop_tray, fr="about")),
        TrayCmd('Quit', self.destroy))
    )

  def set_resolution(self, SS):
    width = int(self.DEFAULT_WIDTH * self.RES[SS])
    height = int(self.DEFAULT_HEIGHT * self.RES[SS])

    self.is_fs, self.SS = bool(SS=='FS'), SS
    blank_space = 1 if self.is_fs else 0
    self.attributes('-fullscreen', self.is_fs)
    self.geometry(f'{width}x{height}')

    for child in self.children.values():
      if not isinstance(child, tk.Frame):
        continue

      child.grid_columnconfigure(0, weight=blank_space)
      child.grid_columnconfigure(1, weight=1)
      child.grid_columnconfigure(2, weight=blank_space)

  def setup_screen(self, frame_name="splash"):
    self.set_resolution(self.SS)
    self.toggle_frame(frame_name)

  def load_fonts(self):

    if not self.asset_dir:
      return

    for file in os.listdir(self.asset_dir):
      if file.endswith('.ttf'):
        load_unload_font(os.path.join(self.asset_dir, file))

  def create_frame(self, name, pack_method=None):
    frame = tk.Frame(
      self, bg="black", highlightthickness=5, name=str.lower(name),
      highlightbackground="black", highlightcolor="black"
    )
    frame.pack(expand=True, fill='both')
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)
    frame.display_name = name
    frame.pre_pack = pack_method if pack_method else lambda _: None

    return frame

  def frame_resize(self, widget, event=None):
    for wid in getattr(widget, 'winfo_children', lambda : [])():
      resize = getattr(wid, "resize", None)
      if resize:
        resize(event)

      self.frame_resize(wid, event)

  def toggle_frame(self, frame_name, pre_pack_args=None):
    self.cur_fr = self.children[frame_name]

    for child in self.winfo_children():
      if not isinstance(child, tk.Frame) or self.cur_fr == frame_name:
        continue
      child.pack_forget()

    self.frame_resize(self.cur_fr)
    self.cur_fr.pre_pack(self.cur_fr, **(pre_pack_args or {}))
    self.cur_fr.pack(fill='both', expand=True)

    display_name, title = self.cur_fr.display_name, 'PokéShelf'
    title += f" : {display_name}" if display_name != "Shelf" else ""
    self.title(title)

  def bind_keys(self):

    for i in ['Escape', 'X', 'x']:
      self.bind(f"<{i}>", self.controller.escape)

    controls = {
      "prv_op": ["Up", "Shift-Tab"], "nxt_op": ["Down", "Tab"],
      "dec_val": ["Left"], "inc_val": ["Right"],
      "run_op": ['Return', 'C', 'c', 'Z', 'z', 'space']
    }

    for func, keys in controls.items():
      for key in keys:
        self.bind(f"<{key}>", partial(self.controller.run_func, func_name=func))

  def start_tray(self):
    self.withdraw()
    self.init_tray()
    self.system_tray.run()
    self.system_tray = None

  def stop_tray(self, tray=None, cmd=None, fr=None):
    self.system_tray.stop()
    self.system_tray = None

    if fr:
      self.after(0, lambda: self._win_from_tray(fr))

  def _win_from_tray(self, fr):
    self.deiconify()
    self.lift()
    self.toggle_frame(fr)

  def add_or_update_game(self, exe_val, img_val, mus_val):
    self.cur_game.update({"exe": exe_val, "img": img_val, "mus": mus_val})

    oid_val = self.cur_game.get(
      'oid', (set(range(1, len(self.GD) + 2)) - set(self.GD)).pop()
    )

    self.cur_game['oid'] = oid_val
    self.GD[oid_val] = self.cur_game

    if oid_val not in self.GO:
      self.GO.append(oid_val)

  def remove_game(self):
    self.GO.remove(self.cur_game['oid'])
    self.GD.pop(self.cur_game['oid'])
    self.cur_game = {}

    self.save_config()

    DialogBox(self, "Game Removed!")

    if self.GD:
      self.toggle_frame('shelf')
    else:
      self.toggle_frame('splash')
