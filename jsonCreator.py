import os
import json
import webbrowser

# Vars
path = os.path.dirname(os.path.abspath(__file__))
data = {}


def createJSON():
    return


def openFolder():
    webbrowser.open('file:' + path)
