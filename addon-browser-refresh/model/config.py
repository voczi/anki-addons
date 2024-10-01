from typing import Any
from aqt import mw

class AddonConfig():
    def __init__(self, moduleName: str) -> None:
        self._moduleName = moduleName
        self._initConfig()
    
    def _initConfig(self):
        configDefaults = { "enable_refresh": "True", "auto_select": "True", "dirty_hook": "False" }
        
        self._ankiConfig = mw.addonManager.getConfig(self._moduleName)
        for config_name, config_default in configDefaults.items():
            if config_name not in self._ankiConfig:
                self._ankiConfig[config_name] = config_default
        
        self._saveConfig()
    
    def _saveConfig(self):
        mw.addonManager.writeConfig(self._moduleName, self._ankiConfig)
    
    def getAutoRefresh(self) -> bool:
        return self._ankiConfig["enable_refresh"] == "True"
    
    def setAutoRefresh(self, value: bool):
        self._ankiConfig["enable_refresh"] = str(value == 2)
        self._saveConfig()
    
    def getAutoSelect(self) -> bool:
        return self._ankiConfig["auto_select"] == "True"
    
    def setAutoSelect(self, value: bool):
        self._ankiConfig["auto_select"] = str(value == 2)
        self._saveConfig()
        
    def getDirtyHook(self) -> bool:
        return self._ankiConfig["dirty_hook"] == "True"
    
    def setDirtyHook(self, value: bool):
        self._ankiConfig["dirty_hook"] = str(value == 2)
        self._saveConfig()
    