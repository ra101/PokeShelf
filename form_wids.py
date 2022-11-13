import os
import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfilename as select_file
from functools import partial

import res_wids

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

    self.cursor = res_wids.ResponsiveLabel(
      master, fg=master['bg'], bg=master['bg'],
      root=master.root, font=font.Font(size=20), text="‣"
    )
    self.cursor.select = partial(self.cursor_select, self.cursor)
    self.cursor.unselect = partial(self.cursor_unselect, self.cursor)

    self.heading = res_wids.ResponsiveLabel(
      master, fg=self.OFF_COLOR, bg=master['bg'],
      root=master.root, font=font_, text=heading
    )
    self.heading.select = partial(self.heading_select, self.heading)
    self.heading.unselect = partial(self.heading_unselect, self.heading)

    self.input_frame = res_wids.ResponsiveFrame(
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

    self.slider = res_wids.ResponsiveLabel(
      self.input_frame, fg=self.OFF_COLOR, bg=master['bg'], root=master.root,
      font=font.Font(size=10),
      text=(("─"*(value//5))+'█'+("─"*(20-(value//5))))
    )
    self.slider.value = 5 * (value//5)

    self.counter = res_wids.ResponsiveLabel(
      self.input_frame, fg=self.FIX_COLOR, bg=master['bg'], root=master.root,
      font=font_,
      text=f'{"0"*(3-len(f"{value}"))}{value}%'
    )
    self.counter.value = value

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

      radio = res_wids.ResponsiveLabel(
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
      radio.grid(column=i, row=0, sticky=tk.NS)


class InputField(BaseFormWidget):

  def __init__(self, master, heading, font_, value='N/A'):
    super().__init__(master, heading, font_)

    self.value = value

    self.input_frame.grid_columnconfigure(0, weight=1)

    self.textbox = res_wids.ResponsiveEntry(
      self.input_frame, font=font_, root=master.root, width=18
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

    self.browse_frame = res_wids.ResponsiveFrame(
      self.input_frame, bg=master['bg'], root=master.root,
      highlightbackground=self.OFF_COLOR, highlightcolor=self.OFF_COLOR, highlightthickness=3
    )
    self.browse_label = res_wids.ResponsiveLabel(
      self.browse_frame, font=font.Font(size=20), root=master.root,
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
      [InputFieldV2.FIX_COLOR, InputFieldV2.OFF_COLOR, self.browse_label.master['bg']],
      [InputFieldV2.OFF_COLOR, InputFieldV2.ON_COLOR, InputFieldV2.BG_COLOR]
    ][selected]


    self.browse_label.config({"fg": text_color, "bg": bg_color})
    self.browse_label.master.config({
      "highlightbackground": border_color, "highlightcolor": border_color
    })

  def grid(self, row):
    super().grid(row)
    self.browse_label.grid(column=0, row=0, sticky=tk.NSEW)
    self.browse_frame.grid(column=1, row=0, sticky=tk.NS)


class DialogBox:

  def __init__(self, root, text, time=1000):

    if root.dialog_box:
      return

    root.dialog_box = res_wids.ResponsiveFrame(
      root.cur_fr, bg="#ddd", root=root, highlightbackground="#333",
      highlightcolor="#333", highlightthickness=3
    )
    root.dialog_box.label = res_wids.ResponsiveLabel(
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