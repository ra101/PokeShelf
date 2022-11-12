from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def load_font(font_path, private=True, enumerable=False):
    """
    This function was taken from
    https://github.com/ifwe/digsby/blob/master/digsby/src/gui/native/win/winfonts.py
    and converted from Python 2.x to 3.x by changing
    isinstance checks [to bytes from str] and [to str from unicode]
    """
    if isinstance(font_path, bytes):
        pathbuf = create_string_buffer(font_path)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(font_path, str):
        pathbuf = create_unicode_buffer(font_path)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('font path must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

def unload_font(font_path, private = True, enumerable = False):
    """
    This function was taken from
    https://github.com/ifwe/digsby/blob/master/digsby/src/gui/native/win/winfonts.py
    and converted from Python 2.x to 3.x by changing
    isinstance checks [to bytes from str] and [to str from unicode]
    """

    if isinstance(font_path, bytes):
        pathbuf = create_string_buffer(font_path)
        RemoveFontResourceEx = windll.gdi32.RemoveFontResourceExA
    elif isinstance(font_path, str):
        pathbuf = create_unicode_buffer(font_path)
        RemoveFontResourceEx = windll.gdi32.RemoveFontResourceExW
    else:
        raise TypeError('fontpath must be a str or unicode')


    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    return bool(RemoveFontResourceEx(byref(pathbuf), flags, 0))
