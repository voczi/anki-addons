from typing import Sequence, cast
from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from anki.notes import Note
from aqt.browser import Browser
from aqt.browser.table import ItemId

config = mw.addonManager.getConfig(__name__)
if config is None:
    config = {"enable_refresh": "True", "auto_select": "True"}
    mw.addonManager.writeConfig(__name__, config)

currentBrowser: Browser = None

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Browser refresh options")

        layout = QVBoxLayout(self)

        enableRefresh = QCheckBox("Enable browser auto-refresh", self)
        enableRefresh.stateChanged.connect(self.refresh_toggled)
        enableRefresh.setChecked(bool(config["enable_refresh"]))
        
        enableAutoSelect = QCheckBox("Auto-select new cards", self)
        enableAutoSelect.stateChanged.connect(self.autoselect_toggled)
        enableAutoSelect.setChecked(bool(config["auto_select"]))

        layout.addWidget(enableRefresh)
        layout.addWidget(enableAutoSelect)
        self.setLayout(layout)

    def refresh_toggled(self, value):
        if value:
            config["enable_refresh"] = True
        else:
            config["enable_refresh"] = ""
        
        mw.addonManager.writeConfig(__name__, config)
    
    def autoselect_toggled(self, value):
        if value:
            config["auto_select"] = True
        else:
            config["auto_select"] = ""
        
        mw.addonManager.writeConfig(__name__, config)

def openConfig():
    configDialog = ConfigDialog()
    configDialog.exec()

def browser_init(browser: Browser):
    global currentBrowser
    currentBrowser = browser

def new_note(note: Note):
    if currentBrowser is not None and not sip.isdeleted(currentBrowser):
        if config["enable_refresh"]:
            currentBrowser.search()
            
            if config["auto_select"] and note.id in currentBrowser.table._model._items:
                cards = note.card_ids()
                if len(cards) > 0:
                    currentBrowser.table.select_single_card(cards[0])

mw.addonManager.setConfigAction(__name__, openConfig)
gui_hooks.browser_menus_did_init.append(browser_init)
gui_hooks.add_cards_did_add_note.append(new_note)