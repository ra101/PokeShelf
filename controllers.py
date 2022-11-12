
class ShelfController:

  def __init__(self, root):
    self.root = root

  def escape(self, event):

    if self.pause:
      return

    if self.cur_fr == self.root.children["splash"]:
      self.root.destroy()
    else:
      self.root.toggle_frame("splash")

  def shortcut(self, event, menu, lbl, cmd):

    if self.pause:
      return

    cmd() if menu.entrycget(lbl, 'state') == "normal" else None

  def run_func(self, event, func_name):

    if self.pause:
      return

    func = getattr(self.cur_fr, func_name, None) if func_name else None
    func() if func else None

  @property
  def cur_fr(self):
    return self.root.cur_fr

  @property
  def pause(self):
    return bool(self.root.dialog_box)
