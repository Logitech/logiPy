"""
logi_arx.py : Defines the exported functions for the API

Logitech Gaming Arx Control SDK

Copyright (C) 2011-2015 Logitech. All rights reserved.
Author: Tom Lambert
Email: devtechsupport@logitech.com
"""

import ctypes
import os
import platform

# DLL Definitions
#
LOGI_ARX_ORIENTATION_PORTRAIT  = 0x01
LOGI_ARX_ORIENTATION_LANDSCAPE = 0x10

LOGI_ARX_EVENT_FOCUS_ACTIVE         = 0x01
LOGI_ARX_EVENT_FOCUS_INACTIVE       = 0x02
LOGI_ARX_EVENT_TAP_ON_TAG           = 0x04
LOGI_ARX_EVENT_MOBILEDEVICE_ARRIVAL = 0x08
LOGI_ARX_EVENT_MOBILEDEVICE_REMOVAL = 0x10

LOGI_ARX_DEVICETYPE_IPHONE         = 0x01
LOGI_ARX_DEVICETYPE_IPAD           = 0x02
LOGI_ARX_DEVICETYPE_ANDROID_SMALL  = 0x03
LOGI_ARX_DEVICETYPE_ANDROID_NORMAL = 0x04
LOGI_ARX_DEVICETYPE_ANDROID_LARGE  = 0x05
LOGI_ARX_DEVICETYPE_ANDROID_XLARGE = 0x06
LOGI_ARX_DEVICETYPE_ANDROID_OTHER  = 0x07

CALLBACK_DEFINITION = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_void_p)

class arxAppCallbackMessage(ctypes.Structure):
    """ creates a struct to match arxAppCallbackMessage. """
    _fields_ = [
        ('eventType', ctypes.c_int),
        ('eventValue', ctypes.c_int),
        ('eventArg', ctypes.c_wchar * 120)
    ]

class logiArxCbContext(ctypes.Structure):
    """ creates a struct to match logiArxCbContext. """
    _fields_ = [
        ('arxCallBack', CALLBACK_DEFINITION),
        ('arxContext', ctypes.c_void_p)
    ]

def callback_wrapper(event_type, event_value, event_arg, context):
    on_callback(event_type, event_value, event_arg, context)

def default_callback(event_type, event_value, event_arg, context):
    print '\n[Arx] default_callback called with: event_type = {event_type}, event_value = {event_value}, event_arg = {event_arg}, context = {context}'.format(
        event_type = event_type, event_value = event_value, event_arg = event_arg, context = context)

# Required Globals
#
class SDKNotFoundException:
    pass

def load_dll(path_dll = None):
    if not path_dll:
        bitness = 'x86' if platform.architecture()[0] == '32bit' else 'x64'
        subpath_dll = r'/Logitech Gaming Software/SDK/Arx Control/{}/LogitechGArxControl.dll'.format(bitness)
        subpath_lgs = os.environ['ProgramW6432'] if os.environ['ProgramW6432'] else os.environ['ProgramFiles']
        path_dll = subpath_lgs + subpath_dll
    if os.path.exists(path_dll):
        return ctypes.cdll.LoadLibrary(path_dll)
    else:
        raise SDKNotFoundException('The SDK DLL was not found.')

try:
    arx_dll = load_dll()
except SDKNotFoundException as exception_sdk:
    arx_dll = None
on_callback = None


# Wrapped SDK Functions
#
def logi_arx_init(identifier, friendly_name, py_callback_function = None):
    """ initializes the applet on the app with the given friendly_name. """
    if arx_dll:
        global on_callback
        global callback_ref
        on_callback   = py_callback_function if py_callback_function else default_callback
        callback_ref  = ctypes.byref(CALLBACK_DEFINITION(callback_wrapper))
        identifier    = ctypes.c_wchar_p(identifier)
        friendly_name = ctypes.c_wchar_p(friendly_name)
        return bool(arx_dll.LogiArxInit(identifier, friendly_name, callback_ref))
    else:
        return False

def logi_arx_add_file_as(file_path, file_name, mime_type = None):
    """ sends a file to the device from local a file_path and assigns a file_name to it. mime_type, if assigned, specifies the MIME type of the file. """
    if arx_dll:
        file_path = ctypes.c_wchar_p(file_path)
        file_name = ctypes.c_wchar_p(file_name)
        mime_type = ctypes.c_wchar_p(mime_type) if mime_type else ctypes.c_wchar_p('')
        return bool(arx_dll.LogiArxAddFileAs(file_path, file_name, mime_type))
    else:
        return False

def logi_arx_add_content_as(content, size, file_name, mime_type = None):
    """ sends content to the device and saves it to a virtual file called file_name. mime_type, if assigned, specifies the MIME type of the file. """
    if arx_dll:
        content   = ctypes.c_void_p(content)
        size      = ctypes.c_int(size)
        file_name = ctypes.c_wchar_p(file_name)
        mime_type = ctypes.c_wchar_p(mime_type) if mime_type else ctypes.c_wchar_p('')
        return bool(arx_dll.LogiArxAddContentAs(content, size, file_name, mime_type))
    else:
        return False

def logi_arx_add_utf8_string_as(string_content, file_name, mime_type = None):
    """ sends a UTF8 string to the device and saves it to a virtual file called file_name. mime_type, if assigned, specifies the MIME type of the file. """
    if arx_dll:
        string_content = ctypes.c_wchar_p(string_content)
        file_name      = ctypes.c_wchar_p(file_name)
        mime_type      = ctypes.c_wchar_p(mime_type) if mime_type else ctypes.c_wchar_p('')
        return bool(arx_dll.LogiArxAddUTF8StringAs(string_content, file_name, mime_type))
    else:
        return False

def logi_arx_add_image_from_bitmap(bitmap, width, height, file_name):
    """ compresses the image specified by the BGRA byte array bitmap (interpretting the array using width and height) into a png file with the name specified by file_name,
    then sends it over to the the device. note that the color bit order is BGRA rather than standard RGBA bit order. """
    if arx_dll:
        bitmap    = ctypes.c_char_p(bitmap)
        width     = ctypes.c_int(width)
        height    = ctypes.c_int(height)
        file_name = ctypes.c_wchar_p(file_name)
        return bool(arx_dll.LogiArxAddImageFromBitmap(bitmap, width, height, file_name))
    else:
        return False

def logi_arx_set_index(file_name):
    """ sets which of the sent files is the index. (first one to be displayed in the applet) """
    if arx_dll:
        file_name = ctypes.c_wchar_p(file_name)
        return bool(arx_dll.LogiArxSetIndex(file_name))
    else:
        return False

def logi_arx_set_tag_property_by_id(tag_id, prop, new_value):
    """ change at runtime a prop (property) on the tag with the id tag_id from the old value to the new_value. """
    if arx_dll:
        tag_id    = ctypes.c_wchar_p(tag_id)
        prop      = ctypes.c_wchar_p(prop)
        new_value = ctypes.c_wchar_p(new_value)
        return bool(arx_dll.LogiArxSetTagPropertyById(tag_id, prop, new_value))
    else:
        return False

def logi_arx_set_tags_property_by_class(tag_class, prop, new_value):
    """ change at runtime a prop (property) on the tag with the class tag_class from the old value to the new_value. """
    if arx_dll:
        tag_class = ctypes.c_wchar_p(tag_class)
        prop      = ctypes.c_wchar_p(prop)
        new_value = ctypes.c_wchar_p(new_value)
        return bool(arx_dll.LogiArxSetTagsPropertyByClass(tag_class, prop, new_value))
    else:
        return False

def logi_arx_set_tag_content_by_id(tag_id, new_content):
    """ change at runtime the content (innerHTML) of a tag with the id tag_id from the old content to the new_content. """
    if arx_dll:
        tag_id      = ctypes.c_wchar_p(tag_id)
        new_content = ctypes.c_wchar_p(new_content)
        return bool(arx_dll.LogiArxSetTagContentById(tag_id, new_content))
    else:
        return False

def logi_arx_set_tags_content_by_class(tag_class, new_content):
    """ change at runtime the content (innerHTML) of a tag with the class tag_class from the old content to the new_content. """
    if arx_dll:
        tag_class   = ctypes.c_wchar_p(tag_class)
        new_content = ctypes.c_wchar_p(new_content)
        return bool(arx_dll.LogiArxSetTagsPropertyByClass(tag_class, new_content))
    else:
        return False

def logi_arx_get_last_error():
    """ each function returns a bool. to get detailed info on the last error code, call this function. """
    if arx_dll:
        return int(arx_dll.LogiArxGetLastError())
    else:
        return False

def logi_arx_shutdown():
    """ shuts down the applet on the app. """
    if arx_dll:
        arx_dll.LogiArxShutdown()
        return True
    else:
        return False