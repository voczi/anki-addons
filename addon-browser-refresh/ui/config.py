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

        layout.addWidget(autoRefresh)
        layout.addWidget(autoSelect)
        
        self.setLayout(layout)