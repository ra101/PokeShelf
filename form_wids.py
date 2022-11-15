import os
import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfilename as select_file
from functools import partial

from pyo import SfPlayer
from tkVideoPlayer import TkinterVideo

from res_wids import ResponsiveEntry, ResponsiveFrame, ResponsiveLabel

class BaseFormWidget:
  OFF_COLOR = "#639"
  ON_COLOR = "#f63"
  FIX_COLOR = "#333"
  SAVE_COLOR = "#060"
  CANCEL_COLOR = "#900"
  BG_COLOR = "#fd9"

  def __init__(self, master, heading, font_):
    master.grid_columnconfigure(0, weight=0)
    master.grid_columnconfigure(1, weight=10)
    master.grid_columnconfigure(2, weight=1)

    self.cursor = ResponsiveLabel(
      master, fg=master['bg'], bg=master['bg'],
      root=master.root, font=font.Font(size=20), text="‣"
    )
    self.cursor.select = partial(self.cursor_select, self.cursor)
    self.cursor.unselect = partial(self.cursor_unselect, self.cursor)

    self.heading = ResponsiveLabel(
      master, fg=self.OFF_COLOR, bg=master['bg'],
      root=master.root, font=font_, text=heading
    )
    self.heading.select = partial(self.heading_select, self.heading)
    self.heading.unselect = partial(self.heading_unselect, self.heading)

    self.input_frame = ResponsiveFrame(
      master, bg=master['bg'], root=master.root,
    )
    self.input_frame.grid_rowconfigure(0, weight=1)
    self.input_frame.select = lambda :None
    self.input_frame.unselect = lambda :None

  @staticmethod
  def cursor_select(cursor):
    cursor.config({"fg": BaseFormWidget.FIX_COLOR})

  @staticmethod
  def cursor_unselect(cursor):
    cursor.config({"fg": cursor.master['bg']})

  @staticmethod
  def heading_select(heading):
    heading.config({"fg": BaseFormWidget.ON_COLOR})

  @staticmethod
  def heading_unselect(heading):
    heading.config({"fg": BaseFormWidget.OFF_COLOR})


  def grid(self, row):
    self.cursor.grid(column=0, row=row, sticky=tk.NS+tk.E, padx=5, pady=1)
    self.heading.grid(column=1, row=row, sticky=tk.NS+tk.W, pady=1)
    self.input_frame.grid(column=2, row=row, sticky=tk.NSEW, pady=1)


class Slider(BaseFormWidget):

  def __init__(self, master, heading, font_, value=0):
    super().__init__(master, heading, font_)

    value = min(max(value, 0), 100)

    self.input_frame.grid_columnconfigure(0, weight=1)
    self.input_frame.grid_columnconfigure(1, weight=0)

    self.slider = ResponsiveLabel(
      self.input_frame, fg=self.OFF_COLOR, bg=master['bg'], root=master.root,
      font=font.Font(size=10),
      text=(("─"*(value//5))+'█'+("─"*(20-(value//5))))
    )
    self.slider.value = 5 * (value//5)

    self.counter = ResponsiveLabel(
      self.input_frame, fg=self.FIX_COLOR, bg=master['bg'], root=master.root,
      font=font_,
      text=f'{"0"*(3-len(f"{value}"))}{value}%'
    )
    self.counter.value = value

    self.music_server = getattr(master.root, 'music_server', None)

    self.input_frame.select = partial(self.on_off, True)
    self.input_frame.unselect = partial(self.on_off, False)
    self.input_frame.inc_val = partial(self.change_value, 5)
    self.input_frame.dec_val = partial(self.change_value, -5)

  def on_off(self, selected=True):
    color = Slider.ON_COLOR if selected else Slider.FIX_COLOR
    value = self.counter.root.MV
    self.counter.config({"fg": color, "text": f'{"0"*(3-len(f"{value}"))}{value}%'})

  def change_value(self, val):
    value = min(max(self.slider.value + val, 0), 100)

    if value == self.counter.value:
      return

    self.counter.root.MV = self.slider.value = self.counter.value = value

    self.slider.config({"text": (("─"*(value//5))+'█'+("─"*(20-(value//5))))})
    self.counter.config({"text": f'{"0"*(3-len(f"{value}"))}{value}%'})

    if self.music_server:
      self.music_server.setAmp(self.counter.value/100)

  def grid(self, row):
    super().grid(row)
    self.slider.grid(column=0, row=0, sticky=tk.NS + tk.W)
    self.counter.grid(column=1, row=0, sticky=tk.W, padx=10)


class RadioButton(BaseFormWidget):

  def __init__(self, master, heading, font_, radiology, value="M"):
    super().__init__(master, heading, font_)

    value = value if value in master.root.RES else "M"
    self.input_frame.value_olist = ["S", "M", "L", "XL", "FS"]

    for i in range(len(radiology)):
      self.input_frame.grid_columnconfigure(i, weight=1)

    for key, command in radiology.items():
      fg = self.FIX_COLOR if key == value else self.OFF_COLOR

      radio = ResponsiveLabel(
        self.input_frame, fg=fg, bg=master['bg'],
        root=master.root, font=font_, text=key
      )
      radio.value = key
      radio.command = command

    children = list(self.input_frame.children.values())
    self.input_frame.select = partial(self.on_off, children, True)
    self.input_frame.unselect = partial(self.on_off, children, False)
    self.input_frame.inc_val = partial(self.change_value, children, 1)
    self.input_frame.dec_val = partial(self.change_value, children, -1)

  @staticmethod
  def on_off(children, selected=True):
    on_color = RadioButton.ON_COLOR if selected else RadioButton.FIX_COLOR
    for child in children:
      color = on_color if child.value == child.root.SS else RadioButton.OFF_COLOR
      child.config({"fg": color})

  @staticmethod
  def change_value(children, val):
    for child in children:
      if child.value == child.root.SS:
        child.config({"fg":  RadioButton.OFF_COLOR})
        break

    value_olist, root = children[0].master.value_olist, children[0].root
    cur_idx = value_olist.index(root.SS)
    root.set_resolution(value_olist[(cur_idx + val) % len(value_olist)])

    RadioButton.on_off(children, True)


  def grid(self, row):
    super().grid(row)
    for i, radio in enumerate(self.input_frame.children.values()):
      radio.grid(column=i, row=0, sticky=tk.NS, pady=3)


class RadioButtonV2(BaseFormWidget):

  def __init__(self, master, heading, font_, value="M"):
    super().__init__(master, heading, font_)

    value = "ON" if master.root.ST else "OFF"
    self.input_frame.value_olist = ["ON", "OFF"]

    self.input_frame.grid_columnconfigure(0, weight=1)
    self.input_frame.grid_columnconfigure(1, weight=1)

    for key in self.input_frame.value_olist:
      fg = self.FIX_COLOR if key == value else self.OFF_COLOR

      radio = ResponsiveLabel(
        self.input_frame, fg=fg, bg=master['bg'],
        root=master.root, font=font_, text=key
      )
      radio.value = bool(key == "ON")

    children = list(self.input_frame.children.values())
    self.input_frame.select = partial(self.on_off, children, master.root, True)
    self.input_frame.unselect = partial(self.on_off, children, master.root, False)
    self.input_frame.inc_val = partial(self.change_value, children, master.root)
    self.input_frame.dec_val = partial(self.change_value, children, master.root)

  @staticmethod
  def on_off(children, root, selected=True):
    on_color = RadioButton.ON_COLOR if selected else RadioButton.FIX_COLOR
    children[root.ST].config({"fg":  RadioButton.OFF_COLOR})
    children[~root.ST].config({"fg":  on_color })

  @staticmethod
  def change_value(children, root):
    root.ST = ~root.ST
    children[root.ST].config({"fg":  RadioButton.OFF_COLOR})
    children[~root.ST].config({"fg":  RadioButton.ON_COLOR})


  def grid(self, row):
    super().grid(row)
    for i, radio in enumerate(self.input_frame.children.values()):
      radio.grid(column=i, row=0, sticky=tk.NS, pady=3)



class InputField(BaseFormWidget):

  def __init__(self, master, heading, font_, value='N/A'):
    super().__init__(master, heading, font_)

    self.value = value

    self.input_frame.grid_columnconfigure(0, weight=1)

    self.textbox = ResponsiveEntry(
      self.input_frame, font=font_, root=master.root, width=22
    )
    self.textbox.set_value(value)


  def grid(self, row):
    super().grid(row)
    self.textbox.grid(column=0, row=0, sticky=tk.NS + tk.W)


class InputFieldV2(InputField):

  def __init__(self, master, heading, font_, ft, value='N/A'):
    super().__init__(master, heading, font_, value)

    self.input_frame.grid_columnconfigure(1, weight=1)
    self.textbox.configure({'width': 15})

    self.browse_frame = ResponsiveFrame(
      self.input_frame, bg=master['bg'], root=master.root,
      highlightbackground=self.OFF_COLOR, highlightcolor=self.OFF_COLOR, highlightthickness=3
    )
    self.browse_label = ResponsiveLabel(
      self.browse_frame, font=font.Font(size=15), root=master.root,
      bg=master['bg'], text=" ... ", fg=self.ON_COLOR
    )

    self.input_frame.cmd = partial(self.set_value, heading, ft)
    self.input_frame.select = partial(self.on_off,  True)
    self.input_frame.unselect = partial(self.on_off, False)

  def set_value(self, heading, ft):
    dir = os.path.dirname(self.textbox.get()) or os.getcwd()
    file_path = select_file(
      title=f'Select File :: {heading}', initialdir=dir, filetypes=ft
    )
    self.textbox.set_value(file_path)
    return file_path

  def on_off(self, selected=True):
    text_color, border_color, bg_color = [
      [InputFieldV2.FIX_COLOR, InputFieldV2.OFF_COLOR, "#ddd"],
      [InputFieldV2.OFF_COLOR, InputFieldV2.ON_COLOR, InputFieldV2.BG_COLOR]
    ][selected]


    self.browse_label.config({"fg": text_color, "bg": bg_color})
    self.browse_label.master.config({
      "bg": bg_color, "highlightcolor": border_color,
      "highlightbackground": border_color
    })

  def grid(self, row):
    super().grid(row)
    self.browse_label.grid(column=0, row=0, sticky=tk.NSEW,ipadx=5)
    self.browse_frame.grid(column=1, row=0, sticky=tk.NS)


class DialogBox:

  def __init__(self, root, text, time=1000):

    if root.dialog_box:
      return

    root.dialog_box = ResponsiveFrame(
      root.cur_fr, bg="#ddd", root=root, highlightbackground="#333",
      highlightcolor="#333", highlightthickness=3
    )
    root.dialog_box.label = ResponsiveLabel(
      root.dialog_box, root=root, bg=root.dialog_box['bg'],
      text=text, fg=BaseFormWidget.FIX_COLOR,
      font=font.Font(family="Power Green",weight=font.BOLD, size=15)
    )
    root.dialog_box.label.grid(sticky=tk.NSEW, ipadx=10, ipady=5)
    root.dialog_box.place(relx=0.5, rely=0.5, anchor="center")

    root.dialog_box.after(time, self.destroy, root)

  @staticmethod
  def destroy(root):
    root.dialog_box.label.destroy()
    root.dialog_box.destroy()
    root.dialog_box = None


class GamePreviewer(TkinterVideo):
  GAME_COLOR = {
    ".gb": "#3d3",
    ".gbc": "#FA0",
    ".gba": "#90f",
    ".nds": "#ddd",
    ".exe": "#f33"
  }

  def _resize_event(self, event):
    multipler = self.root.RES[self.root.SS]
    font_data = {
      **self.font, 'size': int(self.font['size']*multipler)
    }
    self.config(font = font.Font(**font_data))
    return super()._resize_event(event)

  def _loop_event(self, event):
    if int(event.widget.current_duration()):
        self.play()

  def __init__(self, master, scaled=True, consistant_frame_rate=True, keep_aspect=False, *args, **kwargs):
    self.root, self.font = kwargs.pop('root'), kwargs.pop('font').actual()
    super().__init__(master, scaled, consistant_frame_rate, keep_aspect, *args, **kwargs)
    self.bind("<<Ended>>", self._loop_event)

  def set_title(self, file_path):
    full_name, title, file_ext = '', '', os.path.splitext(file_path)[-1]

    if file_ext == '.exe':
      full_name = os.path.basename(os.path.dirname(file_path))
    elif file_ext in ['.gb', '.gba', '.gbc', '.nds']:
      full_name = os.path.splitext(os.path.basename(file_path))[0]

    for i in full_name.split(' '):
      if len(title.split('\n')[-1]) + len(i) > 16:
        title += ('\n' + i) if title else i
      else:
        title += ' ' + i

    self.config({"text": title, "fg": self.GAME_COLOR.get(file_ext)})

  def run_video(self, path, alt):

    for _, _, files in os.walk(os.path.dirname(path)):
      if os.path.basename(path) in files:
        if os.path.splitext(path)[-1] in [
          '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.mkv', '.webm', '.avi', '.mov'
        ]:
          self.load(path)
          self.play()
          alt = ''
          break

    self.set_title(alt)

  def play_default_music(self):
    music = getattr(self.root, 'default_music', None)
    music.out() if music else None

  def stop_default_music(self):
    music = getattr(self.root, 'default_music', None)
    music.stop() if music else None

  def play_music(self, path):
    try:
      self.music = SfPlayer(path=path, loop=True)
      self.music.out()
    except Exception:
      self.play_default_music()

  def stop_music(self):
    music = getattr(self ,'music', None)
    music.stop() if music else None

  def remove_all(self):
    self.stop()
    self.stop_music()
    self.stop_default_music()

  def preview(self, game):
    self.remove_all()

    if game['img']:
      self.run_video(game['img'], game['exe'])
    else:
      self.set_title(game['exe'])

    if game['mus']:
      self.play_music(game['mus'])
    else:
      self.play_default_music()
