import tkinter as tk
from tkinter import font
from functools import partial

import res_wids, form_wids


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
    if frame.selected_op in [0, 1, (len(frame.op_frs) - 2)]:
      frame.op_frs[frame.selected_op][-1].inc_val()

  @staticmethod
  def dec_val(frame):
    if frame.selected_op in [0, 1, (len(frame.op_frs) - 1)]:
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
      font=font.Font(family="Power Green",weight=font.BOLD, size=30),
      text="Options..."
    ).grid(column=0, row=0, sticky=tk.W, padx=20, pady=3)
    # </h1>

    #</head>
    head_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=3)

  def create_settings(self, win_frame):
    # <body />
    form_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5, name='body',
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )
    form_frame.grid(column=1, row=1, sticky=tk.NSEW, padx=5, pady=3)

    self.create_music_setting(form_frame)
    self.create_size_setting(form_frame)
    self.create_order_setting(form_frame)
    self.create_gb_setting(form_frame)
    self.create_ds_setting(form_frame)
    self.create_save_button(form_frame)
    self.create_cancel_button(form_frame)

  def create_music_setting(self, body_frame):
    form_wids.Slider(
      body_frame, heading="Music Volume", value=self.root.MV,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    ).grid(row=0)

  def create_size_setting(self, body_frame):
    form_wids.RadioButton(
      body_frame, heading="Screen Size", value=self.root.SS, radiology=self.root.RES,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    ).grid(row=1)

  def create_order_setting(self, body_frame):
    frame = form_wids.InputField(
      body_frame, heading="Game Order", value=self.root.GO,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    frame.grid(row=2)
    frame.input_frame.cmd = partial(
      form_wids.DialogBox, self.root, "Edit config.json to\nupdate Game Order"
    )

  def create_gb_setting(self, body_frame):
    heading, ft ="GB Emulator", [['GB Emulator', '.exe']]
    frame = form_wids.InputFieldV2(
      body_frame, value=self.root.GB, heading=heading, ft=ft,
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
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
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    frame.grid(row=4)
    frame.input_frame.cmd = partial(
      self.ds_cmd, self.root, frame, heading, ft
    )

  @staticmethod
  def ds_cmd(root, frame, heading, ft):
    root.DS = frame.set_value(heading, ft)

  def create_save_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.OFF_COLOR,
      highlightcolor=form_wids.BaseFormWidget.OFF_COLOR, highlightthickness=3
    )
    button_frame.grid(column=0, pady=2, columnspan=2,  row=5, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 💾 Save ", fg=form_wids.BaseFormWidget.FIX_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=20)
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
    button_frame.grid(column=2, pady=2, row=5, sticky=tk.NS)

    button_label = res_wids.ResponsiveLabel(
      button_frame, root=self.root, bg=body_frame['bg'],
      text=" 🚫 Cancel ", fg=form_wids.BaseFormWidget.ON_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=20)
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
      font=font.Font(family="Power Green",weight=font.BOLD, size=30),
    )
    win_frame.header.grid(column=0, row=0, sticky=tk.W, padx=20, pady=3)
    # </h1>

    #</head>
    head_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=3)

  def create_settings(self, win_frame):
    # <body />
    form_frame = res_wids.ResponsiveFrame(
      win_frame, bg="#ddd", highlightthickness=5, name="body",
      highlightbackground="#639", root=self.root, highlightcolor="#639"
    )
    form_frame.grid(column=1, row=1, sticky=tk.NSEW, padx=5, pady=3)

    self.create_game_title(form_frame)
    self.create_game_settings(form_frame)
    self.create_save_button(form_frame)
    self.create_cancel_button(form_frame)

  def create_game_title(self, form_frame):
    res_wids.ResponsiveLabel(
      form_frame, fg=form_wids.BaseFormWidget.ON_COLOR, bg=form_frame['bg'],
      root=self.root, font=font.Font(family="Power Green",weight=font.BOLD, size=20),
    ).grid(column=1, row=0, sticky=tk.W, pady=3)

  def create_game_settings(self, body_frame):
    game_exe = form_wids.InputFieldV2(
      body_frame, heading=".exe/.gbx/.nds", value="", ft=[
        ['Exe/ROM', '.exe .gb .gbc .gba .nds'], ['Executable', '.exe'],
        ['DS ROM', '.nds'], ['GB ROM', '.gb .gbc .gba'],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_exe, i).grid_configure({"pady":2})
    game_exe.grid(row=1)
    self.exe_textbox = game_exe.textbox

    game_image = form_wids.InputFieldV2(
      body_frame, heading="BG Img/Vid", value="", ft=[
        ['Img/Vid', '.png .jpg .jpeg .bmp .gif .mp4 .mkv .mpg .flv .mov .wmv .avi'],
        ['Image', '.png .jpg .jpeg .bmp .gif'], ['Video', '.mp4 .mkv .mpg .flv .mov .wmv .avi'],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_image, i).grid_configure({"pady":2})
    game_image.grid(row=2)
    self.img_textbox = game_image.textbox

    game_music = form_wids.InputFieldV2(
      body_frame, heading="BG Music", value="", ft= [
        ['Music', '.mp3 .ogg .wav .aac .wma'],
      ],
      font_=font.Font(family="Power Green",weight=font.BOLD, size=20)
    )
    for i in ['cursor', 'heading', 'textbox', 'browse_frame']:
      getattr(game_music, i).grid_configure({"pady":2})
    game_music.grid(row=3)
    self.mus_textbox = game_music.textbox

  def create_save_button(self, body_frame):
    button_frame = res_wids.ResponsiveFrame(
      body_frame, bg=body_frame['bg'], root=self.root,
      highlightbackground=form_wids.BaseFormWidget.OFF_COLOR,
      highlightcolor=form_wids.BaseFormWidget.OFF_COLOR, highlightthickness=3
    )
    button_frame.grid(column=0, pady=2, columnspan=2,  row=5, sticky=tk.NS)

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

    exe_val, img_val, mus_val = [
      self.exe_textbox.get(), self.mus_textbox.get(), self.mus_textbox.get()
    ]
    is_new = not bool(self.root.cur_game)

    if not exe_val:
      form_wids.DialogBox(self.root, "Game not Selected!")
      return

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
    button_frame.grid(column=2, pady=2, row=5, sticky=tk.NS)

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
      [form_wids.BaseFormWidget.OFF_COLOR, form_wids.BaseFormWidget.FIX_COLOR, label.master['bg']],
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
    text = "Add Your First Game to Get Started"

    if self.root.GD:
      text = "Press Enter to Browse Shelf"

    res_wids.ResponsiveLabel(
      win_frame, fg="#3d3", bg="black", root=self.root,
      font=font.Font(family="Power Green", weight=font.BOLD, size=15),
      text=text,
    ).grid(column=0, row=2, sticky=tk.N)

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
    win_frame = self.root.create_frame("Shelf", self.pre_pack)

    return win_frame


  @staticmethod
  def pre_pack(cur_fr):

    # Setup Menu
    menu_bar = cur_fr.master.children['menu']
    menu_bar.entryconfig("💡 About", state="normal")
    menu_bar.entryconfig("⚙️ Options", state="normal")

    game_menu = menu_bar.children['game']
    game_menu.entryconfig("📚 PokéShelf", state="disabled")
    game_menu.entryconfig("➕ Add Game", state="normal")
    game_menu.entryconfig(
      "🔧 Edit Game", state="normal" if cur_fr.master.GD else "disabled"
    )
    game_menu.entryconfig(
      "➖ Remove Game", state="normal" if cur_fr.master.GD else "disabled"
    )