from aqt import QCheckBox, QDialog, QVBoxLayout
from ..model.config import AddonConfig

class ConfigDialog(QDialog):
    def __init__(self, config: AddonConfig):
        super().__init__()

        self.setWindowTitle("Browser refresh options")

        layout = QVBoxLayout(self)

        autoRefresh = QCheckBox("Enable browser auto-refresh", self)
        autoRefresh.stateChanged.connect(config.setAutoRefresh)
        autoRefresh.setChecked(config.getAutoRefresh())
        
        autoSelect = QCheckBox("Auto-select new cards", self)
        autoSelect.stateChanged.connect(config.setAutoSelect)
        autoSelect.setChecked(config.getAutoSelect())
        
        dirtyHook = QCheckBox("Enable dirty hook", self)
        dirtyHook.toolTip = "Used for compatability with third party plugins (e.g., AnkiConnect). Proceed with caution."
        dirtyHook.stateChanged.connect(config.setDirtyHook)
        dirtyHook.setChecked(config.getDirtyHook())

        layout.addWidget(autoRefresh)
        layout.addWidget(autoSelect)
        layout.addWidget(dirtyHook)
        
        self.setLayout(layout)