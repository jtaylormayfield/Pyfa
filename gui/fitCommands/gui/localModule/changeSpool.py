import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.changeSpool import CalcChangeModuleSpoolCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalModuleSpoolCommand(wx.Command):

    def __init__(self, fitID, position, spoolType, spoolAmount):
        wx.Command.__init__(self, True, 'Change Local Module Spool')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount

    def Do(self):
        cmd = CalcChangeModuleSpoolCommand(
            fitID=self.fitID,
            projected=False,
            position=self.position,
            spoolType=self.spoolType,
            spoolAmount=self.spoolAmount)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
