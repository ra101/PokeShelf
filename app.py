import os, json, sys
import tkinter as tk
from functools import partial

from PIL import Image
from pyo import SfPlayer, Server as SfServer
from pystray import Icon as Tray, MenuItem as TrayCmd

import frames, utils
from form_wids import DialogBox


class ShelfApp(tk.Tk):

  def __new__(cls):
    if utils.is_already_running():
      return cls._already_running_error()
    return super().__new__(cls)

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
    self.music_server.stop()

    if self.ST and self.icon_path:
      if not self.system_tray:
        self.start_tray()
        self.music_server.start()
        return
      else:
        self.stop_tray()

    if self.asset_dir:
      for file in os.listdir(self.asset_dir):
        if file.endswith('.ttf'):
          utils.load_unload_font(
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
    self.init_music_server(self.MV)

    self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT = 512, 384
    self.RES = dict(S=0.5, M=1, L=1.5, XL=2, FS=2.5)
    self.RES['FS'] = self.winfo_screenheight()/self.DEFAULT_HEIGHT

  def init_music_server(self, MV=100):
    self.music_server = SfServer().boot()
    self.music_server.start()
    self.music_server.setAmp(MV/100)

    if not self.asset_dir:
      return

    for file in os.listdir(self.asset_dir):
      if file.endswith('.ogg'):
        self.default_music = SfPlayer(
          path=os.path.join(self.asset_dir, file), loop=True
        )
        self.default_music.out()
        return


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

    self._check_and_fix_order()

  def save_config(self):
    self.config_file = os.path.join(self.base_dir, 'config.json')

    self._check_and_fix_order()

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
    self.title('Pok??Shelf')
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
      {"lbl": "???? Pok??Shelf", 'func': 'toggle_frame', 'func_arg': ['shelf'], 'con':'s'}, {'sep': True},
      {"lbl": "??? Add Game", 'func': 'toggle_frame', 'func_arg': ['gamesettings'], 'con':'a'},
      {"lbl": "???? Edit Game", 'func': 'toggle_frame', 'func_arg': ['gamesettings', {'edit':True}], 'con':'e'},
      {"lbl": "??? Remove Game", 'func': 'remove_game', 'con':'r'},
      {'sep': True}, {"lbl": "??? Close Menu"},
    ]

    for data in game_menu_data:
      is_sep, command = data.get('sep', False), data.get('func', None)

      if is_sep:
        game_menu.add_separator()
        continue

      command = partial(getattr(self, command), *data.get('func_arg', [])) if command else None

      game_menu.add_command(label=data['lbl'], command=command)

      if command:
        func = partial(self._shortcut_event, menu=game_menu, lbl=data['lbl'], cmd=command)
        self.bind(f'<Control-{data["con"].lower()}>', func)
        self.bind(f'<Control-{data["con"].upper()}>', func)

    menu_bar.add_cascade(label="???? Game", menu=game_menu)

    label, command = "?????? Options", partial(self.toggle_frame, "options")
    menu_bar.add_command(label=label, command=command)
    self.bind(f'<Alt-s>', partial(self._shortcut_event, menu=menu_bar, lbl=label, cmd=command))
    self.bind(f'<Alt-S>', partial(self._shortcut_event, menu=menu_bar, lbl=label, cmd=command))

    label, command = "???? About", partial(self.toggle_frame, "about")
    menu_bar.add_command(label=label, command=command)
    self.bind(f'<Alt-a>', partial(self._shortcut_event, menu=menu_bar, lbl=label, cmd=command))
    self.bind(f'<Alt-A>', partial(self._shortcut_event, menu=menu_bar, lbl=label, cmd=command))

    self.config(menu=menu_bar)

  def init_tray(self):
    self.system_tray = Tray(
      name="Pok??Shelf : Tray", title="Pok??Shelf",
      icon=Image.open(self.icon_path),
      menu=(
        TrayCmd('Pok??Shelf', partial(self.stop_tray, fr="splash")),
        TrayCmd('Options', partial(self.stop_tray, fr="options")),
        TrayCmd('About', partial(self.stop_tray, fr="about")),
        TrayCmd('Quit', self.destroy))
    )

  def set_resolution(self, SS):
    width = int(self.DEFAULT_WIDTH * self.RES[SS])
    height = int(self.DEFAULT_HEIGHT * self.RES[SS])

    self.is_fs, self.SS = bool(SS=='FS'), SS
    self.geometry(f'{width}x{height}')
    self.attributes('-fullscreen', self.is_fs)
    cavas_width = int(
      (self.winfo_width() - (self.winfo_height()/0.75))/2
    ) if self.is_fs else 0

    for child in self.children.values():
      if getattr(child, 'l_canvas', None):
        child.l_canvas.config(width=cavas_width)
      if getattr(child, 'r_canvas', None):
        child.r_canvas.config(width=cavas_width)

  def setup_screen(self, frame_name="splash"):
    self.set_resolution(self.SS)
    self.toggle_frame(frame_name)

  def load_fonts(self):

    if not self.asset_dir:
      return

    for file in os.listdir(self.asset_dir):
      if file.endswith('.ttf'):
        utils.load_unload_font(os.path.join(self.asset_dir, file))

  def create_frame(self, name, pre=None, post=None):
    frame = tk.Frame(
      self, bg="black", highlightthickness=5, name=str.lower(name),
      highlightbackground="black", highlightcolor="black"
    )
    frame.pack(expand=True, fill='both')
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1000)
    frame.grid_columnconfigure(2, weight=1)
    frame.display_name = name
    frame.pre_pack = pre if pre else lambda _: None
    frame.post_forget = post if post else lambda _: None

    frame.l_canvas = tk.Canvas(frame, width=0, background="black", highlightthickness=0)
    frame.l_canvas.grid(column=0, row=0, rowspan=100, sticky=tk.NS)

    frame.r_canvas = tk.Canvas(frame, width=0, background="black", highlightthickness=0)
    frame.r_canvas.grid(column=2, row=0, rowspan=100, sticky=tk.NS)

    return frame

  def frame_resize(self, widget, event=None):
    for wid in getattr(widget, 'winfo_children', lambda : [])():
      resize = getattr(wid, "resize", None)
      if resize:
        resize(event)

      self.frame_resize(wid, event)

  def toggle_frame(self, frame_name, pre_pack_args=None):
    nxt_fr = self.children[frame_name]

    for child in self.winfo_children():
      if not isinstance(child, tk.Frame) or nxt_fr == frame_name:
        continue
      child.pack_forget()
      if getattr(self, 'cur_fr', None) and child == self.cur_fr:
        child.post_forget(child)

    self.frame_resize(nxt_fr)
    self.cur_fr = nxt_fr
    nxt_fr.pre_pack(nxt_fr, **(pre_pack_args or {}))
    nxt_fr.pack(fill='both', expand=True)

    display_name, title = self.cur_fr.display_name, 'Pok??Shelf'
    title += f" : {display_name}" if display_name != "Shelf" else ""
    self.title(title)

  def bind_keys(self):

    for i in ['Escape', 'X', 'x']:
      self.bind(f"<{i}>", self._escape_event)

    controls = {
      "prv_op": ["Up", "Shift-Tab"], "nxt_op": ["Down", "Tab"],
      "dec_val": ["Left"], "inc_val": ["Right"],
      "run_op": ['Return', 'C', 'c', 'Z', 'z', 'space']
    }

    for func, keys in controls.items():
      for key in keys:
        self.bind(f"<{key}>", partial(self._interaction_event, func_name=func))

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

  def _escape_event(self, event):
    if event.widget.dialog_box:
      return

    if event.widget.cur_fr == event.widget.children["splash"]:
      event.widget.destroy()
    else:
      event.widget.toggle_frame("splash")

  def _shortcut_event(self, event, menu, lbl, cmd):
    if event.widget.dialog_box:
      return

    cmd() if menu.entrycget(lbl, 'state') == "normal" else None

  def _interaction_event(self, event, func_name):

    if event.widget.dialog_box:
      return

    if func_name:
      func = getattr(event.widget.cur_fr, func_name, None)
      func() if func else None

  def _check_and_fix_order(self):
    # uniquify
    unique_g_order = []

    for x in self.GO:
      if x not in unique_g_order:
        unique_g_order.append(x)

    self.GO = unique_g_order

    # maintain 1-to-1 b/w g_order & g_dict
    g_order = set(self.GO)
    g_dict = set(self.GD)

    items_to_be_removed = g_order - g_dict
    items_to_be_added = g_dict - g_order

    for item in items_to_be_removed:
      self.GO.remove(item)

    for item in items_to_be_added:
      self.GO.append(item)

  @classmethod
  def _already_running_error(cls):
    tk.Tk().withdraw()
    tk.messagebox.showerror(
      title='Pok??Shelf : Error', message="Pok??Shelf Already Running!"
    )
