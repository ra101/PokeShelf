import os, subprocess
from functools import partial
import tkinter as tk
from tkinter import font

import form_wids, res_wids


class AboutFrame:

  def __init__(self, root):
    self.root = root
    self.frame = self.create_frame()

  def create_frame(self):
    win_frame = self.root.create_frame("About", self.pre_pack)
    self.grid_rowconfigure(win_frame)

    self.create_title(win_frame)
    self.create_desc(win_frame)
    self.create_author(win_frame)

    return win_frame

  @staticmethod
  def pre_pack(cur_fr):

    # Setup Menu
    menu_bar = cur_fr.master.children['menu']
    menu_bar.entryconfig("💡 About", state="disabled")
    menu_bar.entryconfig("⚙️ Options", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig(
      "📚 PokéShelf", state="normal" if cur_fr.master.GD else "disabled"
    )
    game_menu.entryconfig("➕ Add Game", state="normal")
    game_menu.entryconfig("🔧 Edit Game", state="disabled")
    game_menu.entryconfig("➖ Remove Game", state="disabled")

  def grid_rowconfigure(self, win_frame):
    win_frame.grid_rowconfigure(0, weight=3)
    win_frame.grid_rowconfigure(1, weight=4)
    win_frame.grid_rowconfigure(2, weight=4)

  def create_title(self, win_frame):
    res_wids.ResponsiveLabel(
      win_frame, fg="#f33", bg="black", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=45),
      text="PokéShelf"
    ).grid(column=1, row=0, sticky=tk.S)

    res_wids.ResponsiveLabel(
      win_frame, fg="#fff", bg="black", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=15),
      text="Gotta Play 'em All !",
    ).grid(column=1, row=1, sticky=tk.N)

  def create_desc(self, win_frame):
    res_wids.ResponsiveLabel(
      win_frame, fg="#3d3", bg="black", root=self.root,
      font=font.Font(family="Power Green", weight=font.BOLD, size=15),
      text="Quick Access Interface\nfor All of Your Pokémon Games",
    ).grid(column=1, row=2, sticky=tk.N)

    res_wids.ResponsiveLabel(
      win_frame, fg="#ddd", bg="black", root=self.root,
      font=font.Font(family="Power Green", size=15),
      text="Version: v1.0.0  •  Licence: GPL 3.0\n\n",
    ).grid(column=1, row=3, sticky=tk.N)

  def create_author(self, win_frame):
    res_wids.ResponsiveLabel(
      win_frame, fg="#ddd", bg="black", root=self.root, text="~ 〈 RA 〉",
      font=font.Font(family="Power Green", weight=font.BOLD, size=15),
    ).grid(column=1, row=4, sticky=tk.SE)


class OptionsFrame:

  def __init__(self, root):
    self.root = root
    self.frame = self.create_frame()

  def create_frame(self):
    win_frame = self.root.create_frame("Options", self.pre_pack)
    self.grid_rowconfigure(win_frame)

    self.create_header(win_frame)
    self.create_settings(win_frame)

    return win_frame

  @staticmethod
  def pre_pack(cur_fr):

    # Setup Menu
    menu_bar = cur_fr.master.children['menu']
    menu_bar.entryconfig("⚙️ Options", state="disabled")
    menu_bar.entryconfig("💡 About", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig(
      "📚 PokéShelf", state="normal" if cur_fr.master.GD else "disabled"
    )
    game_menu.entryconfig("➕ Add Game", state="normal")
    game_menu.entryconfig("🔧 Edit Game", state="disabled")
    game_menu.entryconfig("➖ Remove Game", state="disabled")

    # Setup Current Frame
    cur_fr.op_frs, cur_fr.selected_op = OptionsFrame.split_children(cur_fr), 0
    cur_fr.select = partial(OptionsFrame.select, cur_fr)
    cur_fr.unselect = partial(OptionsFrame.unselect, cur_fr)
    cur_fr.unselect_all  = partial(OptionsFrame.unselect_all, cur_fr)
    cur_fr.nxt_op = partial(OptionsFrame.nxt_op, cur_fr)
    cur_fr.prv_op = partial(OptionsFrame.prv_op, cur_fr)
    cur_fr.inc_val = partial(OptionsFrame.inc_val, cur_fr)
    cur_fr.dec_val = partial(OptionsFrame.dec_val, cur_fr)
    cur_fr.run_op = partial(OptionsFrame.run_op, cur_fr)

    for idx, key in enumerate(['GO', 'GB', 'DS']):
      cur_fr.op_frs[ 2 + idx ][-1].children['!responsiveentry'].set_value(
        getattr(cur_fr.master, key)
      )

    cur_fr.unselect_all()
    cur_fr.select(0)



  @staticmethod
  def run_op(frame):
    if 1 < frame.selected_op < len(frame.op_frs):
      frame.op_frs[frame.selected_op][-1].cmd()


  @staticmethod
  def inc_val(frame):
    if frame.selected_op in [0, 1, (len(frame.op_frs) - 4), (len(frame.op_frs) - 2)]:
      frame.op_frs[frame.selected_op][-1].inc_val()

  @staticmethod
  def dec_val(frame):
    if frame.selected_op in [0, 1, (len(frame.op_frs) - 4), (len(frame.op_frs) - 1)]:
      frame.op_frs[frame.selected_op][-1].dec_val()


  @staticmethod
  def nxt_op(frame):
    frame.unselect(frame.selected_op)
    frame.selected_op = (frame.selected_op + 1) % len(frame.op_frs)
    if frame.selected_op == (len(frame.op_frs) - 3):
      frame.selected_op +=1
    frame.select(frame.selected_op)

  @staticmethod
  def prv_op(frame):
    frame.unselect(frame.selected_op)
    frame.selected_op = (frame.selected_op - 1) % len(frame.op_frs)
    if frame.selected_op == (len(frame.op_frs) - 3):
      frame.selected_op -=1
    frame.select(frame.selected_op)

  @staticmethod
  def split_children(frame):
    children = list(reversed(frame.children['body'].grid_slaves()))
    op_frs = []

    for i in range(0, len(children), 3):
      op_frs.append(children[i: i+3])

    op_frs.append([children[-2]])
    op_frs.append([children[-1]])

    return op_frs

  @staticmethod
  def select(frame, op):
    for fr in frame.op_frs[op]:
      fr.select()

  @staticmethod
  def unselect(frame, op):
    for fr in frame.op_frs[op]:
      fr.unselect()

  @staticmethod
  def unselect_all(frame):
    for op in frame.op_frs:
      for fr in op:
        fr.unselect()

  def grid_rowconfigure(self, win_frame):
    win_frame.grid_rowconfigure(0, weight=0)
    win_frame.grid_rowconfigure(1, weight=1)

  def create_header(self, win_frame):
    # <head>
    head_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5,
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )

    # <h1>
    res_wids.ResponsiveLabel(
      head_frame, fg="#333", bg="#ddd", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=25),
      text="Options..."
    ).grid(column=0, row=0, sticky=tk.W, padx=3, pady=3)
    # </h1>

    #</head>
    head_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=3, pady=3)

  def create_settings(self, win_frame):
    # <body />
    form_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5, name='body',
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )
    form_frame.grid(column=1, row=1, sticky=tk.NSEW, padx=3, pady=3)

    self.create_music_setting(form_frame)
    self.create_size_setting(form_frame)
    self.create_order_setting(form_frame)
    self.create_gb_setting(form_frame)
    self.create_ds_setting(form_frame)
    self.create_tray_setting(form_frame)
    self.create_save_button(form_frame)
    self.create_cancel_button(form_frame)

  def create_music_setting(self, body_frame):
    form_wids.Slider(
      body_frame, heading="Music Volume", value=self.root.MV,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    ).grid(row=0)

  def create_size_setting(self, body_frame):
    form_wids.RadioButton(
      body_frame, heading="Screen Size", value=self.root.SS, radiology=self.root.RES,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    ).grid(row=1)

  def create_order_setting(self, body_frame):
    frame = form_wids.InputField(
      body_frame, heading="Game Order", value=self.root.GO,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    )
    frame.grid(row=2)
    frame.input_frame.cmd = partial(
      form_wids.DialogBox, self.root, "Edit config.json to\nupdate Game Order"
    )

  def create_gb_setting(self, body_frame):
    heading, ft ="GB Emulator", [['GB Emulator', '.exe']]
    frame = form_wids.InputFieldV2(
      body_frame, value=self.root.GB, heading=heading, ft=ft,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    )
    frame.grid(row=3)
    frame.input_frame.cmd = partial(
      self.gb_cmd, self.root, frame, heading, ft
    )

  @staticmethod
  def gb_cmd(root, frame, heading, ft):
    root.GB = frame.set_value(heading, ft)

  def create_ds_setting(self, body_frame):
    heading, ft ="DS Emulator", [['DS Emulator', '.exe']]
    frame = form_wids.InputFieldV2(
      body_frame, value=self.root.DS, heading=heading, ft=ft,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    )
    frame.grid(row=4)
    frame.input_frame.cmd = partial(
      self.ds_cmd, self.root, frame, heading, ft
    )

  @staticmethod
  def ds_cmd(root, frame, heading, ft):
    root.DS = frame.set_value(heading, ft)

  def create_tray_setting(self, body_frame):
    form_wids.RadioButtonV2(
      body_frame, heading="System Tray", value=self.root.ST,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=18)
    ).grid(row=5)

  def create_save_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.OFF_COLOR,
      highlightcolor=form_wids.BaseFormWidget.OFF_COLOR, highlightthickness=3
    )
    button_frame.grid(column=0, pady=2, columnspan=2,  row=6, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 💾 Save ", fg=form_wids.BaseFormWidget.FIX_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=18)
    )
    button_label.grid(column=0, row=0, sticky=tk.NSEW)

    button_frame.select = partial(self.button_on_off, button_label, True, True)
    button_frame.unselect = partial(self.button_on_off, button_label, False, True)
    button_frame.inc_val = lambda: button_frame.master.master.nxt_op()
    button_frame.cmd = partial(self.save_cmd, self.root)

  @staticmethod
  def save_cmd(root):
    root.save_config()
    root.setup_screen()

  def create_cancel_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.OFF_COLOR,
      highlightcolor=form_wids.BaseFormWidget.OFF_COLOR, highlightthickness=3
    )
    button_frame.grid(column=2, pady=2, row=6, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 🚫 Cancel ", fg=form_wids.BaseFormWidget.ON_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=18)
    )
    button_label.grid(column=0, row=0, sticky=tk.NSEW)

    button_frame.select = partial(self.button_on_off, button_label, True, False)
    button_frame.unselect = partial(self.button_on_off, button_label, False, False)
    button_frame.dec_val = lambda: button_frame.master.master.prv_op()
    button_frame.cmd = partial(self.cancel_cmd, self.root)

  @staticmethod
  def cancel_cmd(root):
    root.init_config()
    root.setup_screen()

  @staticmethod
  def button_on_off(label, selected=True, save=False):
    text_color, border_color, bg_color = [
      [form_wids.BaseFormWidget.FIX_COLOR, form_wids.BaseFormWidget.OFF_COLOR, label.master['bg']],
      [
        [form_wids.BaseFormWidget.CANCEL_COLOR, form_wids.BaseFormWidget.SAVE_COLOR][save],
        form_wids.BaseFormWidget.ON_COLOR, form_wids.BaseFormWidget.BG_COLOR
      ]
    ][selected]

    label.config({"fg": text_color, "bg":bg_color})
    label.master.config({
      "highlightbackground": border_color, "highlightcolor": border_color
    })


class GameSettingsFrame:

  IMG_EXTS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
  MOV_EXTS = ['.mp4', '.mkv', '.webm', '.avi', '.mov']
  DIS_EXTS = [*IMG_EXTS, *MOV_EXTS]
  MUS_EXTS = [".wav", ".ogg", ".flac"]

  def __init__(self, root):
    self.root = root
    self.frame = self.create_frame()

  def create_frame(self):
    win_frame = self.root.create_frame("GameSettings", self.pre_pack)
    self.grid_rowconfigure(win_frame)

    self.create_header(win_frame)
    self.create_settings(win_frame)

    return win_frame

  @staticmethod
  def pre_pack(cur_fr, edit=False):

    cur_game = cur_fr.master.cur_game = cur_fr.master.cur_game if edit else {}

    # Setup Menu
    menu_bar = cur_fr.master.children['menu']
    menu_bar.entryconfig("⚙️ Options", state="normal")
    menu_bar.entryconfig("💡 About", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig(
      "📚 PokéShelf", state="normal" if cur_fr.master.GD else "disabled"
    )
    game_menu.entryconfig(
      "➕ Add Game", state="normal" if edit else "disabled"
    )
    game_menu.entryconfig("🔧 Edit Game", state="disabled")
    game_menu.entryconfig(
      "➖ Remove Game", state="normal" if edit else "disabled"
    )

    # Set Header
    header_text = f'{"Edit" if edit else "Add"} Game'
    cur_fr.header.config({"text":header_text})

    # Key Bindings
    cur_fr.op_frs, cur_fr.selected_op  = GameSettingsFrame.split_children(cur_fr), 0
    cur_fr.select = partial(GameSettingsFrame.select, cur_fr)
    cur_fr.unselect = partial(GameSettingsFrame.unselect, cur_fr)
    cur_fr.unselect_all = partial(GameSettingsFrame.unselect_all, cur_fr)
    cur_fr.nxt_op = partial(GameSettingsFrame.nxt_op, cur_fr)
    cur_fr.prv_op = partial(GameSettingsFrame.prv_op, cur_fr)
    cur_fr.inc_val = partial(GameSettingsFrame.inc_val, cur_fr)
    cur_fr.dec_val = partial(GameSettingsFrame.dec_val, cur_fr)
    cur_fr.run_op = partial(GameSettingsFrame.run_op, cur_fr)

    for idx, key in enumerate(['exe', 'img', 'mus']):
      cur_fr.op_frs[idx][-1].children[
        '!responsiveentry'
      ].set_value(cur_game.get(key, ''))

    GameSettingsFrame.exe_cmd(lambda: cur_game.get('exe',''), cur_fr.lbl)

    # Select 0th
    cur_fr.unselect_all()
    cur_fr.select(0)


  @staticmethod
  def run_op(frame):
    frame.op_frs[frame.selected_op][-1].cmd()

  @staticmethod
  def inc_val(frame):
    if frame.selected_op == (len(frame.op_frs) - 2):
      frame.nxt_op()

  @staticmethod
  def dec_val(frame):
    if frame.selected_op == (len(frame.op_frs) - 1):
      frame.prv_op()

  @staticmethod
  def nxt_op(frame):
    frame.unselect(frame.selected_op)
    frame.selected_op = (frame.selected_op + 1) % len(frame.op_frs)
    if frame.selected_op == (len(frame.op_frs) - 3):
      frame.selected_op +=1
    frame.select(frame.selected_op)

  @staticmethod
  def prv_op(frame):
    frame.unselect(frame.selected_op)
    frame.selected_op = (frame.selected_op - 1) % len(frame.op_frs)
    if frame.selected_op == (len(frame.op_frs) - 3):
      frame.selected_op -= 1
    frame.select(frame.selected_op)

  @staticmethod
  def split_children(frame):
    children = list(reversed(frame.children['body'].grid_slaves()))
    op_frs = []

    for i in range(1, len(children), 3):
      op_frs.append(children[i: i+3])

    op_frs.append([children[-2]])
    op_frs.append([children[-1]])

    return op_frs

  @staticmethod
  def select(frame, op):
    for fr in frame.op_frs[op]:
      fr.select()

  @staticmethod
  def unselect(frame, op):
    for fr in frame.op_frs[op]:
      fr.unselect()

  @staticmethod
  def unselect_all(frame):
    for op in frame.op_frs:
      for fr in op:
        fr.unselect()

  def grid_rowconfigure(self, win_frame):
    win_frame.grid_rowconfigure(0, weight=0)
    win_frame.grid_rowconfigure(1, weight=1)

  def create_header(self, win_frame):
    # <head>
    head_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5,
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )

    # <h1>
    win_frame.header =  res_wids.ResponsiveLabel(
      head_frame, fg="#333", bg="#ddd", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=25),
    )
    win_frame.header.grid(column=0, row=0, sticky=tk.W, padx=3, pady=3)
    # </h1>

    #</head>
    head_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=3, pady=3)

  def create_settings(self, win_frame):
    # <body />
    form_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5, name="body",
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )
    form_frame.grid(column=1, row=1, sticky=tk.NSEW, padx=3, pady=3)

    self.create_game_title(form_frame)
    self.create_game_settings(form_frame)
    self.create_save_button(form_frame)
    self.create_cancel_button(form_frame)

  def create_game_title(self, form_frame):
    form_frame.master.lbl = res_wids.ResponsiveLabel(
      form_frame, fg="#999", bg=form_frame['bg'],
      root=self.root, font=font.Font(family="Power Green",weight=font.BOLD, size=20),
    )
    form_frame.master.lbl.grid(
      column=1, row=0, sticky=tk.W, pady=3, columnspan=2,
    )

  @staticmethod
  def exe_cmd(set_value_func, game_label, img_textbox=None, mus_textbox=None):
    file_path = set_value_func()
    if file_path.endswith('exe'):
      text = os.path.basename(os.path.dirname(file_path))
      name = text
    else:
      text = os.path.basename(file_path)
      name = os.path.splitext(text)[0]

    game_label.config({"text": text[:32]})

    if img_textbox:
      GameSettingsFrame.auto_add_values(
        textbox=img_textbox, exts=GameSettingsFrame.DIS_EXTS,
        name=name, data_dir=os.path.join(
          os.path.join(os.path.dirname(file_path), 'Graphics'), 'Titles'
        )
      )

    if mus_textbox:
      GameSettingsFrame.auto_add_values(
        textbox=mus_textbox, exts=GameSettingsFrame.MUS_EXTS,
        name=name, data_dir=os.path.join(
          os.path.join(os.path.dirname(file_path), 'Audio'), 'BGM'
        )
      )

  @staticmethod
  def auto_add_values(textbox, exts, name, data_dir):
    for _, _, files in os.walk(data_dir):
      f_d = {}
      for f in files:
        n, e = os.path.splitext(f)
        if e in exts:
          f_d[n.lower()] = f

      shelf_f, name_f, title_f, splash_f = None, None, None, None

      for i in set(f_d.keys()):

        if not shelf_f and i == 'shelf':
          shelf_f = i

        if not name_f and i == name:
          name_f = i

        if not title_f and i.startswith('title'):
          title_f = i

        if not splash_f and i.startswith('splash'):
          splash_f = i

      if shelf_f:
        textbox.set_value(os.path.join(data_dir, f_d[shelf_f]))

      elif name_f:
        textbox.set_value(os.path.join(data_dir, f_d[shelf_f]))

      elif title_f:
        textbox.set_value(os.path.join(data_dir, f_d[title_f]))

      elif splash_f:
        textbox.set_value(os.path.join(data_dir, f_d[splash_f]))


  def create_game_settings(self, body_frame):
    game_exe = form_wids.InputFieldV2(
      body_frame, heading=".exe/.gbx/.nds", value="", ft=[
        ['Exe/ROM', '.exe .gb .gbc .gba .nds'], ['Executable', '.exe'],
        ['DS ROM', '.nds'], ['GB ROM', '.gb .gbc .gba'],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_exe, i).grid_configure({"pady":0})
    game_exe.grid(row=1)
    self.exe_textbox = game_exe.textbox

    game_image = form_wids.InputFieldV2(
      body_frame, heading="BG Img/Vid", value="", ft=[
        ['Img/Vid', ' '.join(self.DIS_EXTS)],
        ['Image', ' '.join(self.IMG_EXTS)], ['Video', ' '.join(self.MOV_EXTS)],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_image, i).grid_configure({"pady":11})
    game_image.grid(row=2)
    self.img_textbox = game_image.textbox

    game_music = form_wids.InputFieldV2(
      body_frame, heading="BG Music", value="", ft= [
        ['Music', ' '.join(self.MUS_EXTS)],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_music, i).grid_configure({"pady":11})
    game_music.grid(row=3)
    self.mus_textbox = game_music.textbox

    game_exe.input_frame.cmd = partial(
      self.exe_cmd, set_value_func=game_exe.input_frame.cmd,
      game_label=body_frame.master.lbl,
      img_textbox=game_image.textbox, mus_textbox=game_music.textbox
    )

  def create_save_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.OFF_COLOR,
      highlightcolor=form_wids.BaseFormWidget.OFF_COLOR, highlightthickness=3
    )
    button_frame.grid(column=0, pady=11, columnspan=2,  row=5, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 💾 Save ", fg=form_wids.BaseFormWidget.FIX_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    button_label.grid(column=0, row=0, sticky=tk.NSEW)

    button_frame.select = partial(self.button_on_off, button_label, True, True)
    button_frame.unselect = partial(self.button_on_off, button_label, False, True)
    button_frame.cmd = partial(self.save_cmd)

  def save_cmd(self):

    exe_val = self.exe_textbox.get()

    if not exe_val:
      form_wids.DialogBox(self.root, "Game not Selected!")
      return

    if not self.root.DS and exe_val.endswith('.nds'):
      form_wids.DialogBox(
        self.root, "Select `DS Emulator`\nin Options <Alt+S>\n" \
        "before adding NDS ROM!", time=2000)
      return

    if not self.root.GB and (exe_val.endswith('.gb') \
      or exe_val.endswith('.gbc') or exe_val.endswith('.gba')):
      form_wids.DialogBox(
        self.root, "Select `GB Emulator`\nin Options <Alt+S>\n" \
          "before adding GBx ROM!", time=2000)
      return

    img_val, mus_val = self.img_textbox.get(), self.mus_textbox.get()
    is_new = not bool(self.root.cur_game)

    self.root.add_or_update_game(exe_val, img_val, mus_val)
    self.root.save_config()
    self.root.setup_screen("shelf" if self.root.GD else "splash")

    form_wids.DialogBox(
      self.root, f'Game {"Added" if is_new else "Updated"}!'
    )

  def create_cancel_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.FIX_COLOR,
      highlightcolor=form_wids.BaseFormWidget.FIX_COLOR, highlightthickness=3
    )
    button_frame.grid(column=2, pady=11, row=5, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 🚫 Cancel ", fg=form_wids.BaseFormWidget.OFF_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    button_label.grid(column=0, row=0, sticky=tk.NSEW)

    button_frame.select = partial(self.button_on_off, button_label, True, False)
    button_frame.unselect = partial(self.button_on_off, button_label, False, False)
    button_frame.cmd = partial(self.cancel_cmd, self.root)

  @staticmethod
  def cancel_cmd(root):
    root.init_config()
    root.setup_screen("shelf" if root.GD else "splash")


  @staticmethod
  def button_on_off(label, selected=True, save=False):
    text_color, border_color, bg_color = [
      [form_wids.BaseFormWidget.FIX_COLOR, form_wids.BaseFormWidget.OFF_COLOR, label.master['bg']],
      [
        [form_wids.BaseFormWidget.CANCEL_COLOR, form_wids.BaseFormWidget.SAVE_COLOR][save],
        form_wids.BaseFormWidget.ON_COLOR, form_wids.BaseFormWidget.BG_COLOR
      ]
    ][selected]

    label.config({"fg": text_color, "bg":bg_color})
    label.master.config({
      "highlightbackground": border_color, "highlightcolor": border_color
    })


class SplashFrame:

  def __init__(self, root):
    self.root = root
    self.frame = self.create_frame()

  def create_frame(self):
    win_frame = self.root.create_frame("Splash", self.pre_pack)

    self.create_splash_frame(win_frame)

    return win_frame

  def create_splash_frame(self, win_frame):
    default_frame = tk.Frame(
      win_frame, bg="black", highlightthickness=5, name="default",
      highlightbackground="black", highlightcolor="black"
    )

    win_frame.grid_rowconfigure(0, weight=1)

    default_frame.grid_columnconfigure(0, weight=1)
    default_frame.grid_rowconfigure(0, weight=4)
    default_frame.grid_rowconfigure(1, weight=4)
    default_frame.grid_rowconfigure(2, weight=4)


    default_frame.grid(column=1, row=0, sticky=tk.NSEW)

    self.create_title(default_frame)
    self.create_headline(default_frame)
    self.create_desc(default_frame)

    return default_frame

  @staticmethod
  def pre_pack(cur_fr):

    # Setup Menu
    menu_bar = cur_fr.master.children['menu']
    menu_bar.entryconfig("💡 About", state="normal")
    menu_bar.entryconfig("⚙️ Options", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig(
      "📚 PokéShelf", state="normal" if cur_fr.master.GD else "disabled"
    )
    game_menu.entryconfig("➕ Add Game", state="normal")
    game_menu.entryconfig("🔧 Edit Game", state="disabled")
    game_menu.entryconfig("➖ Remove Game", state="disabled")

    headline = "Add Your First Game to Get Started"
    if cur_fr.master.GD:
      headline = "Press Enter to Browse Shelf"

    cur_fr.headlabel.config({"text": headline})

    cur_fr.run_op = partial(SplashFrame.run_op, cur_fr)


  @staticmethod
  def run_op(frame):
    if frame.master.GD:
      frame.master.toggle_frame('shelf')

  def create_title(self, win_frame):
    res_wids.ResponsiveLabel(
      win_frame, fg="#f33", bg="black", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=45),
      text="PokéShelf"
    ).grid(column=0, row=0, sticky=tk.S)

    res_wids.ResponsiveLabel(
      win_frame, fg="#fff", bg="black", root=self.root,
      font=font.Font(family="Power Green",weight=font.BOLD, size=15),
      text="Gotta Play 'em All !",
    ).grid(column=0, row=1, sticky=tk.N)

  def create_headline(self, win_frame):

    win_frame.master.headlabel = res_wids.ResponsiveLabel(
      win_frame, fg="#3d3", bg="black", root=self.root,
      font=font.Font(family="Power Green", weight=font.BOLD, size=15), text="",
    )
    win_frame.master.headlabel.grid(column=0, row=2, sticky=tk.N)

  def create_desc(self, win_frame):
    res_wids.ResponsiveLabel(
      win_frame, fg="#ddd", bg="black", root=self.root,
      font=font.Font(family="Power Green", weight=font.BOLD, size=12),
      text=str(
        "📚 PokéShelf :: Ctrl + S\t➕ Add Game :: Ctrl + A\n\n"
        "🔧 Edit Game :: Ctrl + E\t➖ Remove Game :: Ctrl + R\n\n"
        "💡 About :: Alt + A\t⚙️ Options :: Alt + S\n\n"
        "❌ Exit :: Esc\n"
      ),
    ).grid(column=0, row=3, sticky=tk.N)


class ShelfFrame:

  def __init__(self, root):
    self.root = root
    self.frame = self.create_frame()

  def create_frame(self):
    win_frame = self.root.create_frame("Shelf", self.pre_pack, self.post_forget)
    win_frame.grid_rowconfigure(0, weight=1)

    return win_frame

  @staticmethod
  def post_forget(cur_fr):
    if cur_fr.display:
      cur_fr.display.stop_default_music()
      cur_fr.display.stop_music()
      cur_fr.display.play_default_music()

  @staticmethod
  def create_display(cur_frame):
    display = form_wids.GamePreviewer(
      cur_frame, background="black", root=cur_frame.master,
      font=font.Font(family="Power Green",weight=font.BOLD, size=40),
    )
    display.grid(row=0, column=1, sticky=tk.NSEW)
    display.preview(cur_frame.master.cur_game)
    return display

  @staticmethod
  def destroy_display(display):
    display.remove_all()
    display.destroy()

  @staticmethod
  def pre_pack(cur_fr):

    root, cur_fr.display = cur_fr.master, None

    # Setup Menu
    menu_bar = root.children['menu']
    menu_bar.entryconfig("💡 About", state="normal")
    menu_bar.entryconfig("⚙️ Options", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig("📚 PokéShelf", state="disabled")
    game_menu.entryconfig("➕ Add Game", state="normal")
    game_menu.entryconfig("🔧 Edit Game", state="normal")
    game_menu.entryconfig("➖ Remove Game", state="normal")
    cur_fr.run_op = partial(ShelfFrame.run_op, root)
    cur_fr.inc_val = partial(ShelfFrame.chg_val, cur_fr, root, 1)
    cur_fr.dec_val = partial(ShelfFrame.chg_val, cur_fr, root, -1)

    root.cur_game = getattr(root, "cur_game", {}) or root.GD[root.GO[0]]
    cur_fr.display = ShelfFrame.create_display(cur_fr)

  @staticmethod
  def chg_val(cur_fr, root, val):

    old_idx = root.GO.index(root.cur_game['oid'])
    new_idx = (old_idx + val) % len(root.GO)
    if old_idx != new_idx:
      root.cur_game = root.GD[root.GO[new_idx]]

      if cur_fr.display:
        ShelfFrame.destroy_display(cur_fr.display)

      cur_fr.display = ShelfFrame.create_display(cur_fr)

  @staticmethod
  def run_op(root):
    file = root.cur_game['exe']

    if file.endswith(".exe"):
      subprocess.Popen(f'\"{file}\"')

    elif file.endswith(".nds"):
      subprocess.Popen(f'\"{root.DS}\" \"{file}\"')

    elif file.endswith(".gb") or file.endswith(".gba") or file.endswith(".gbc"):
      subprocess.Popen(f'\"{root.GB}\" \"{file}\"')

    else:
      form_wids.DialogBox(root, "Unknown File Type!")
      return

    root.destroy()
