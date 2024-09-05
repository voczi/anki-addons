from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from aqt.utils import showInfo, qconnect
from anki.notes import Note
from aqt.browser import Browser

config = mw.addonManager.getConfig(__name__)
if config is None:
    config = {"enable_refresh": ""}
    mw.addonManager.writeConfig(__name__, config)

currentBrowser: Browser = None

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Browser refresh options")

        layout = QVBoxLayout(self)
        enableRefresh = QCheckBox("Enable browser auto-refresh", self)
        enableRefresh.stateChanged.connect(self.state_changed)
        enableRefresh.setChecked(bool(config["enable_refresh"]))
        layout.addWidget(enableRefresh)

        self.setLayout(layout)

    def state_changed(self, value):
        if value:
            config["enable_refresh"] = True
        else:
            config["enable_refresh"] = ""
        
        mw.addonManager.writeConfig(__name__, config)

def openConfig():
    configDialog = ConfigDialog()
    configDialog.exec()

def browser_init(browser: Browser):
    global currentBrowser
    currentBrowser = browser

def update_browser(note: Note):
    if currentBrowser is not None and not sip.isdeleted(currentBrowser):
        if config["enable_refresh"]:
            currentBrowser.search()


mw.addonManager.setConfigAction(__name__, openConfig)
gui_hooks.browser_menus_did_init.append(browser_init)
gui_hooks.add_cards_did_add_note.append(update_browser)