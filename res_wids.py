
import tkinter as tk
from tkinter import font


class ResponsiveFrame(tk.Frame):

  def resize(self, event):
    multipler = self.root.RES[self.root.SS]
    border_size = int(self.border_size*multipler)
    self.config(highlightthickness = border_size)

    if self.winfo_manager() == 'grid':
      self.grid_configure({
        i: int(self.grid_config[i] * multipler) for i in ['ipadx', 'ipady', 'padx', 'pady']
      })


  def grid(self, cnf={}, **kw):
    super().grid(cnf={}, **kw)
    self.grid_config = self.grid_info()

  def __init__(self, master=None, cnf={}, **kw):
    self.root, self.border_size = kw.pop('root'), kw.get('highlightthickness', 0)
    super().__init__(master, cnf, **kw)
    self.bind('<Configure>', self.resize)


class ResponsiveLabel(tk.Label):

  def resize(self, event):
    multipler = self.root.RES[self.root.SS]
    font_data = {
      **self.font, 'size': int(self.font['size']*multipler)
    }
    self.config(font = font.Font(**font_data))

    if self.winfo_manager() == 'grid':
      self.grid_configure({
        i: int(self.grid_config[i] * multipler) for i in ['ipadx', 'ipady', 'padx', 'pady']
      })

  def grid(self, cnf={}, **kw):
    super().grid(cnf={}, **kw)
    self.grid_config = self.grid_info()

  def __init__(self, master=None, cnf={}, **kw):
    self.root, self.font = kw.pop('root'), kw.pop('font').actual()
    super().__init__(master, cnf, **kw)
    self.bind('<Configure>', self.resize)


class ResponsiveEntry(tk.Entry):

  def resize(self, event):
    multipler = self.root.RES[self.root.SS]
    font_data = {
      **self.font, 'size': int(self.font['size']*multipler)
    }
    self.config(font = font.Font(**font_data))

    if self.winfo_manager() == 'grid':
      self.grid_configure({
        i: int(self.grid_config[i] * multipler) for i in ['ipadx', 'ipady', 'padx', 'pady']
      })

  def set_value(self, value):
    self.config(state="normal")
    self.delete(0, "end")
    self.insert(0, value)
    self.config(state="disabled")

  def grid(self, cnf={}, **kw):
    super().grid(cnf={}, **kw)
    self.grid_config = self.grid_info()

  def __init__(self, master=None, cnf={}, **kw):
    self.root, self.font = kw.pop('root'), kw.pop('font').actual()
    super().__init__(master, cnf, **kw)
    self.bind('<Configure>', self.resize)
