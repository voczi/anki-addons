from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from aqt.browser import Browser
from anki.notes import Note
from anki.decks import DeckId
from .ui.config import ConfigDialog
from .model.config import AddonConfig
from anki.collection import Collection, OpChanges

config = AddonConfig(__name__)
currentBrowsers: set[Browser] = set()

def openConfig():
    configDialog = ConfigDialog(config)
    configDialog.exec()

def browser_init(browser: Browser):
    global currentBrowsers
    currentBrowsers.add(browser)
    
def setup_hooks():
    # TODO Restore original functions after user disables the addon

    Collection._add_note = Collection.add_note
    Collection.add_note = on_add_note

def on_add_note(self: Collection, note: Note, deck_id: DeckId) -> OpChanges:
    ret: OpChanges = Collection._add_note(self, note, deck_id)
    mw.taskman.run_on_main(lambda: new_note(note))
    return ret

def new_note(note: Note):
    global currentBrowsers

    deletedBrowsers: set[Browser] = set()
    
    for currentBrowser in currentBrowsers:
        if currentBrowser is None or sip.isdeleted(currentBrowser):
            deletedBrowsers.add(currentBrowser)
            continue
        
        if config.getAutoRefresh():
            currentBrowser.search()
                
        if config.getAutoSelect() and note.id in currentBrowser.table._model._items:
            cards = note.card_ids()
            if len(cards) > 0:
                currentBrowser.table.select_single_card(cards[0])
    
    currentBrowsers = currentBrowsers.difference(deletedBrowsers)
    
mw.addonManager.setConfigAction(__name__, openConfig)

gui_hooks.browser_menus_did_init.append(browser_init)
setup_hooks()