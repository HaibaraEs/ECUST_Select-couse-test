import win32api
import os


def PlayDejavu():
    os.system('dejavu.aac')
    WM_APPCOMMAND = 0x319

    APPCOMMAND_VOLUME_MAX = 0x0a
    APPCOMMAND_VOLUME_MIN = 0x09

    win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MAX * 0x10000)
