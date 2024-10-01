from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from aqt.browser import Browser
from anki.notes import Note
from anki.decks import DeckId
from .ui.config import ConfigDialog
from .model.config import AddonConfig
from anki.collection import Collection, OpChanges
from aqt.operations import QueryOp

config = AddonConfig(__name__)
currentBrowser: Browser = None

def openConfig():
    configDialog = ConfigDialog(config)
    configDialog.exec()

def browser_init(browser: Browser):
    global currentBrowser
    currentBrowser = browser
    
def dirty_hook():
    Collection._add_note = Collection.add_note
    Collection.add_note = dirty_add_note

def dirty_add_note(self: Collection, note: Note, deck_id: DeckId) -> OpChanges:
    ret: OpChanges = Collection._add_note(self, note, deck_id)
    mw.taskman.run_on_main(lambda: new_note(note))
    return ret

def new_note(note: Note):
    if currentBrowser is not None and not sip.isdeleted(currentBrowser):
        if config.getAutoRefresh():
            currentBrowser.search()
            
            if config.getAutoSelect() and note.id in currentBrowser.table._model._items:
                cards = note.card_ids()
                if len(cards) > 0:
                    currentBrowser.table.select_single_card(cards[0])
    
mw.addonManager.setConfigAction(__name__, openConfig)

gui_hooks.browser_menus_did_init.append(browser_init)
if not config.getDirtyHook():
    gui_hooks.add_cards_did_add_note.append(new_note)
else:
    dirty_hook()