httpclip

Httpclip is a simple, small Flask application that provides an API to your
system's clipboard. It also provides a web interface for easy use of the API.

Currently it relies on the xsel command line utility, as this was the only
program I could find that could reliably persist the contents of the clipboard
in the event that the httpclip process was terminated.


The application defaults to only being available on the loopback device, and
running on port 5000 (the defaults of the underlying Flask library). To change
this, you will need to create a configuration file following this format:

  HTTPCLIP_HOST="0.0.0.0"
  HTTPCLIP_PORT=8080

You'll need to point the application at this file using the HTTPCLIP_SETTINGS
environment variable. You can use this to configure other Flask configuration
settings. See here for a full list: http://flask.pocoo.org/docs/latest/config/

To run the application, use the following command:

  /usr/bin/env HTTPCLIP_SETTINGS=$HOME/.config/httpclip.cfg \
    PYTHONPATH=/path/to/httpclip /usr/bin/python /path/to/httpclip/httpclip.py


There are currently three HTTP endpoints provided by the application:

Index ("/")
This returns a webpage that lets you interact with the API using AJAX. It uses
the new fetch API. If your browser does not support the fetch API, a polyfill
will be loaded automatically.

Clipboard Get ("/clipboard/get")
Returns a text/plain response with the current contents of the clipboard.

Clipboard Set ("/clipboard/set")
Post a text/plain request body to set the contents of the clipboard.


This repository is MIT licensed. I own the copyright to all code except the
fetch polyfill.