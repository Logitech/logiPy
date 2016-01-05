import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# LED snippets
##############

# Set all device lighting to red
from logipy import logi_led
import time
import ctypes

print ('Setting all device lighting to red...')
logi_led.logi_led_init()
time.sleep(1) # Give the SDK a second to initialize
logi_led.logi_led_set_lighting(100, 0, 0)
raw_input('Press enter to shutdown SDK...')
logi_led.logi_led_shutdown()

# If you prefer the c/c++ style you can use the DLL directly
print ('Setting all device lighting to green...')
logi_led.led_dll.LogiLedInit()
time.sleep(1) # Give the SDK a second to initialize
logi_led.led_dll.LogiLedSetLighting(ctypes.c_int(0), ctypes.c_int(100), ctypes.c_int(0))
raw_input('Press enter to shutdown SDK...')
logi_led.led_dll.LogiLedShutdown()


# Arx snippets
##############

# Show a simple applet with the default callback
# note: will not work if a callback has already been defined by the process
from logipy import logi_arx
import time
print 'Setting up a simple applet...'
index = """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, target-densityDpi=device-dpi, user-scalable=no" />
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <img id="splash-icon" src="http://gaming.logitech.com/images/logos/gamingLogo-lg.png" />
    </body>
    </html>
    """
css = """
    body {
        background-color: black;
    }
    img {
	    position: absolute;
	    top: 50%;
	    left: 50%;
	    width: 118px;
	    height: 118px;
	    margin-top: -59px;
	    margin-left: -59px;
    }
    """
logi_arx.logi_arx_init('com.logitech.gaming.logipy', 'LogiPy')
time.sleep(1)
logi_arx.logi_arx_add_utf8_string_as(index, 'index.html', 'text/html')
logi_arx.logi_arx_add_utf8_string_as(css, 'style.css', 'text/css')
logi_arx.logi_arx_set_index('index.html')
raw_input('Press enter to shutdown SDK...')
logi_arx.logi_arx_shutdown()

# Show a simple applet with a custom callback
from logipy import logi_arx
import time
import ctypes

print 'Setting up a simple applet with custom callback...'
index = """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, target-densityDpi=device-dpi, user-scalable=no" />
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <img id="splash-icon" src="http://gaming.logitech.com/images/logos/gamingLogo-lg.png" />
    </body>
    </html>
    """
css = """
    body {
        background-color: black;
    }
    img {
	    position: absolute;
	    top: 50%;
	    left: 50%;
	    width: 118px;
	    height: 118px;
	    margin-top: -59px;
	    margin-left: -59px;
    }
    """
def custom_callback(event_type, event_value, event_arg, context):
    if event_arg and event_arg == 'splash-icon':
        print '\nNo wonder Logitech is called Logicool in Japan! They are so cool!'

logi_arx.logi_arx_init('com.logitech.gaming.logipy', 'LogiPy', custom_callback)
time.sleep(1)
logi_arx.logi_arx_add_utf8_string_as(index, 'index.html', 'text/html')
logi_arx.logi_arx_add_utf8_string_as(css, 'style.css', 'text/css')
logi_arx.logi_arx_set_index('index.html')
raw_input('Press enter to shutdown SDK...')
logi_arx.logi_arx_shutdown()