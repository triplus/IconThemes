# Icon themes for FreeCAD
# Copyright (C) 2016, 2017, 2018, 2019 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Icon themes for FreeCAD."""


import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from PySide import QtCore

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/IconThemes")


def iconThemesPath():
    """Folder containing icon themes."""
    path = (App.getUserAppDataDir() +
            "Gui" +
            os.path.sep +
            "Icons" +
            os.path.sep)
    return path


def iconThemesFiles():
    """Create a list of icon theme files."""
    files = []
    path = iconThemesPath()

    for f in os.listdir(path):
        if f.endswith(".rcc"):
            files.append(f)
    return files


def registerResource(name, mode=True):
    """Register or unregister external binary resource."""
    path = iconThemesPath()

    if os.path.isfile(os.path.join(path, name)):
        if mode:
            QtCore.QResource.registerResource(os.path.join(path, name))
            text = "Icon themes: registered external resource"
            App.Console.PrintLog(text +
                                 " " +
                                 name +
                                 ".\n")
        else:
            n = 10
            unregister = True
            while unregister and n:
                unregister = (QtCore.QResource.unregisterResource(
                    os.path.join(path, name)))
                n -= 1
            text = "Icon themes: unregistered external resource"
            App.Console.PrintLog(text +
                                 " " +
                                 name +
                                 ".\n")
    else:
        App.Console.PrintLog("Icon themes: external resource" +
                             name +
                             " not found" +
                             ".\n")


def iconThemesNames():
    """Extract icon themes names from registered resources."""
    files = []
    names = []
    it = QtCore.QDirIterator(":", QtCore.QDirIterator.Subdirectories)

    while it.hasNext():
        f = it.next()
        if "index.theme" in f:
            files.append(f)

    for f in files:
        name = None
        text = QtCore.QFile(f)
        text.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)
        while not text.atEnd():
            line = text.readLine()
            if "Name=" in str(line):
                name = str(line)
                name = name.replace("\n", "")
                name = name.replace("Name=", "")
        text.close()
        folder = f.split("/")
        folder = folder[-2]
        names.append([name, folder])

    return names


def setThemeName(name):
    """Set icon theme name."""
    QtGui.QIcon.setThemeName(name)
    App.Console.PrintLog("Icon themes: set theme name" +
                         " " +
                         name +
                         ".\n")


def prefDialog():
    """Preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dialog.done(1)

    def onFinished():
        """Delete dialog on close."""
        dialog.deleteLater()

    dialog = QtGui.QDialog(mw)
    dialog.resize(800, 450)
    dialog.setWindowTitle("Icon themes")
    dialog.setObjectName("IconThemes")
    layout = QtGui.QVBoxLayout()
    dialog.setLayout(layout)

    register = QtGui.QListWidget(dialog)
    register.setParent(dialog)
    register.setSortingEnabled(True)
    register.sortItems(QtCore.Qt.AscendingOrder)

    setTheme = QtGui.QListWidget(dialog)
    setTheme.setParent(dialog)
    setTheme.setSortingEnabled(True)
    setTheme.sortItems(QtCore.Qt.AscendingOrder)

    labelRegister = QtGui.QLabel(dialog)
    labelRegister.setText("Register a resource:")
    labelSet = QtGui.QLabel(dialog)
    labelSet.setText("Set the icon theme:")

    layoutCenter = QtGui.QHBoxLayout()

    layoutCenterRegister = QtGui.QVBoxLayout()
    layoutCenterRegister.addWidget(labelRegister)
    layoutCenterRegister.addWidget(register)

    layoutCenterSet = QtGui.QVBoxLayout()
    layoutCenterSet.addWidget(labelSet)
    layoutCenterSet.addWidget(setTheme)

    layoutCenter.insertLayout(0, layoutCenterRegister)
    layoutCenter.insertLayout(1, layoutCenterSet)

    buttonClose = QtGui.QPushButton("&Close", dialog)
    buttonClose.setDefault(True)

    layoutBottom = QtGui.QHBoxLayout()
    layoutBottom.addStretch(1)
    layoutBottom.addWidget(buttonClose)

    layout.insertLayout(0, layoutCenter)
    layout.insertLayout(1, layoutBottom)

    dialog.finished.connect(onFinished)
    buttonClose.clicked.connect(onAccepted)

    def updateRegister():
        """Update register list widget."""
        files = iconThemesFiles()
        enabled = p.GetString("Registered")
        enabled = enabled.split(",")

        register.blockSignals(True)
        register.clear()

        for f in files:
            item = QtGui.QListWidgetItem(register)
            item.setText(f)
            item.setData(32, f)
            if f in enabled:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        register.blockSignals(False)

    updateRegister()

    def onRegister(item):
        """Register or unregister resource."""
        enabled = []

        if item.checkState() == QtCore.Qt.Checked:
            registerResource(item.data(32))
        else:
            registerResource(item.data(32), False)

        for index in range(register.count()):
            if register.item(index).checkState() == QtCore.Qt.Checked:
                enabled.append(register.item(index).data(32))

        p.SetString("Registered", ",".join(enabled))
        updateSetTheme()

    register.itemChanged.connect(onRegister)

    def updateSetTheme():
        """Update icon themes list widget."""
        names = iconThemesNames()

        setTheme.blockSignals(True)
        setTheme.clear()

        for n in names:
            item = QtGui.QListWidgetItem(setTheme)
            item.setText(n[0])
            item.setData(32, n[1])
            item.setCheckState(QtCore.Qt.Unchecked)

        checked = False
        name = p.GetString("Theme", "FreeCAD-default")
        for index in range(setTheme.count()):
            if setTheme.item(index).data(32) == name:
                setTheme.item(index).setCheckState(QtCore.Qt.Checked)
                checked = True

        if not checked:
            for index in range(setTheme.count()):
                if setTheme.item(index).data(32) == "FreeCAD-default":
                    setTheme.item(index).setCheckState(QtCore.Qt.Checked)
                    p.SetString("Theme", "FreeCAD-default")
                    setThemeName("FreeCAD-default")

        setTheme.blockSignals(False)

    updateSetTheme()

    def onSetTheme(item):
        """Set the icon theme."""
        if item.checkState() == QtCore.Qt.Checked:
            name = item.data(32)
        else:
            name = None

        setTheme.blockSignals(True)

        for index in range(setTheme.count()):
            setTheme.item(index).setCheckState(QtCore.Qt.Unchecked)
        if name:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            name = "FreeCAD-default"
            for index in range(setTheme.count()):
                if setTheme.item(index).data(32) == name:
                    setTheme.item(index).setCheckState(QtCore.Qt.Checked)

        setTheme.blockSignals(False)

        if name:
            p.SetString("Theme", name)
        else:
            p.RemString("Theme")

        setThemeName(name)

    setTheme.itemChanged.connect(onSetTheme)

    return dialog


def onPreferences():
    """Open the preferences dialog."""
    dialog = prefDialog()
    dialog.show()


def registerOnStart():
    """Register enabled resources on FreeCAD start."""
    files = iconThemesFiles()
    enabled = p.GetString("Registered")
    enabled = enabled.split(",")

    for f in files:
        if f in enabled:
            registerResource(f)


def setThemeOnStart():
    """Set enabled icon theme on FreeCAD start."""
    name = p.GetString("Theme", "FreeCAD-default")
    setThemeName(name)


def accessoriesMenu():
    """Add icon themes preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Icon themes")
    pref.setObjectName("IconThemes")
    pref.triggered.connect(onPreferences)

    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("IconThemes")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")

        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu(mw)
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menubar."""
                mb.addAction(action)
                action.setVisible(True)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onStart():
    """Start the icon themes."""
    timer.stop()
    timer.deleteLater()
    accessoriesMenu()


def onPreStart():
    """Improve start reliability and maintain FreeCAD 0.16 support."""
    if App.Version()[1] < "17":
        onStart()
    else:
        if mw.property("eventLoop"):
            onStart()


registerOnStart()
setThemeOnStart()

timer = QtCore.QTimer()
timer.timeout.connect(onPreStart)
timer.start(500)
