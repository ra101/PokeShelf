from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20


def load_unload_font(font_path, private=True, enumerable=False, load=True):
    """
    This function was taken from
    https://github.com/ifwe/digsby/blob/master/digsby/src/gui/native/win/winfonts.py
    and converted from Python 2.x to 3.x by changing
    isinstance checks [to bytes from str] and [to str from unicode]
    """

    func = "Add" if load else "Remove"

    if isinstance(font_path, bytes):
        pathbuf = create_string_buffer(font_path)
        FontResourceEx = getattr(windll.gdi32, f"{func}FontResourceExA")
    elif isinstance(font_path, str):
        pathbuf = create_unicode_buffer(font_path)
        FontResourceEx = getattr(windll.gdi32, f"{func}FontResourceExW")
    else:
        raise TypeError('font path must be a str or unicode')


    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    return bool(FontResourceEx(byref(pathbuf), flags, 0))
