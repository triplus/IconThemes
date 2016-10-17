# Icon themes for FreeCAD
# Copyright (C) 2016  triplus @ FreeCAD
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


from PySide import QtGui
mw = FreeCADGui.getMainWindow()


def iconThemes():
    """
    Icon themes for FreeCAD.
    """
    import os
    import FreeCADGui as Gui
    import FreeCAD as App
    from PySide import QtGui
    from PySide import QtCore

    mw = Gui.getMainWindow()
    mb = mw.menuBar()

    appliedIcons = []
    defaultIcons = {}

    paramGet = App.ParamGet("User parameter:BaseApp/IconThemes")

    def actionList():
        """
        Create a dictionary of unique actions.
        """
        actions = {}
        duplicates = []

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName() and i.text():
                if i.objectName() in actions:
                    if i.objectName() not in duplicates:
                        duplicates.append(i.objectName())
                    else:
                        pass
                else:
                    actions[i.objectName()] = i
            else:
                pass

        for d in duplicates:
            del actions[d]

        return actions

    def themeFolders():
        """
        Create a list of icon theme folders.
        """
        folders = []
        path = (App.getUserAppDataDir() +
                "Gui" +
                os.path.sep +
                "Icons" +
                os.path.sep)

        if os.path.isdir(path):
            for i in os.listdir(path):
                if os.path.isdir(path + i):
                    folders.append(i.encode("UTF-8"))
                else:
                    pass
        else:
            pass

        return folders

    def currentFolder():
        """
        Current icon theme folder.
        """
        themeFolder = paramGet.GetString("ThemeFolder")

        if themeFolder:

            path = (App.getUserAppDataDir() +
                    "Gui" +
                    os.path.sep +
                    "Icons" +
                    os.path.sep +
                    themeFolder.decode("UTF-8") +
                    os.path.sep)

            if os.path.isdir(path):
                return path
            else:
                return False
        else:
            return False

    def themeIcons():
        """
        Create a list of theme icons.
        """
        icons = []
        path = currentFolder()

        if path:
            for i in os.listdir(path):
                if os.path.isfile(path + i) and i.endswith(".svg"):
                    icons.append(path + i)
                else:
                    pass
        else:
            pass

        return icons

    def resetIcons():
        """
        Set default theme icons.
        """
        actions = actionList()

        for i in actions:
            if i in defaultIcons:
                actions[i].setIcon(defaultIcons[i])
            else:
                pass

    def applyIcons():
        """
        Apply the icons from the currently set icon theme.
        """
        path = currentFolder()
        actions = actionList()

        if path:
            for i in actions:
                name = actions[i].objectName()

                if name not in defaultIcons:
                    defaultIcons[name] = actions[i].icon()
                else:
                    pass

                if name not in appliedIcons:
                    icon = path + name + ".svg"

                    if os.path.isfile(icon):
                        actions[i].setIcon(QtGui.QIcon(icon))
                    else:
                        pass
                    appliedIcons.append(name)
                else:
                    pass
        else:
            pass

    def addMenu():
        """
        Add accessories menu to the menubar.
        """
        toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")

        if toolsMenu:
            toolsMenu.addAction(actionAccessories)
        else:
            pass

    def onPreferences():
        """
        Open the preferences dialog.
        """
        dialog = prefDialog()
        dialog.show()

    def prefDialog():
        """
        Preferences dialog.
        """
        def updateComboBox():
            """
            Update theme folders combobox.
            """
            default = True
            folders = themeFolders()
            current = paramGet.GetString("ThemeFolder").decode("UTF-8")

            comboBox.blockSignals(True)

            comboBox.clear()

            for i in folders:
                comboBox.addItem(i.decode("UTF-8"))

            for count in xrange(comboBox.count()):
                if comboBox.itemText(count) == current:
                    comboBox.setCurrentIndex(count)
                    default = False
                else:
                    pass

            comboBox.insertSeparator(0)
            comboBox.insertItem(0, "Default")

            if default:
                comboBox.setCurrentIndex(0)
            else:
                pass

            comboBox.blockSignals(False)

        def onTheme(index):
            """
            Apply the selected theme.
            """
            if index != 0:
                text = comboBox.currentText()
                paramGet.SetString("ThemeFolder", text.encode("UTF-8"))
            else:
                paramGet.RemString("ThemeFolder")

            del appliedIcons[:]
            resetIcons()

            applyIcons()
            updateListIcons()

        def updateListIcons():
            """
            Update icons in the icon preview area.
            """
            icons = themeIcons()

            iconList.blockSignals(True)

            iconList.clear()

            for i in icons:
                item = QtGui.QListWidgetItem(iconList)
                item.setIcon(QtGui.QIcon(i))

            iconList.blockSignals(False)

        def onAccepted():
            """
            Close dialog on button close.
            """
            dialog.done(1)

        def onFinished():
            """
            Delete dialog on close.
            """
            dialog.deleteLater()

        def prefDefaults():
            """
            Set preferences default values.
            """
            updateComboBox()
            updateListIcons()

        dialog = QtGui.QDialog(mw)
        dialog.resize(800, 450)
        dialog.setWindowTitle("IconThemes")
        dialog.setObjectName("IconThemes")
        layout = QtGui.QVBoxLayout()
        dialog.setLayout(layout)

        comboBox = QtGui.QComboBox(dialog)
        comboBox.setMinimumWidth(220)

        iconList = QtGui.QListWidget(dialog)
        iconList.setParent(dialog)
        iconList.setIconSize(QtCore.QSize(48, 48))
        iconList.setGridSize(QtCore.QSize(108, 96))
        iconList.setViewMode(QtGui.QListView.IconMode)
        iconList.setResizeMode(QtGui.QListView.Adjust)

        buttonClose = QtGui.QPushButton("Close", dialog)
        buttonClose.setDefault(True)

        layoutTop = QtGui.QHBoxLayout()
        layoutTop.addWidget(comboBox)
        layoutTop.addStretch(1)

        layoutBottom = QtGui.QHBoxLayout()
        layoutBottom.addStretch(1)
        layoutBottom.addWidget(buttonClose)

        layout.insertLayout(0, layoutTop)
        layout.insertWidget(1, iconList)
        layout.insertLayout(2, layoutBottom)

        prefDefaults()

        dialog.finished.connect(onFinished)
        buttonClose.clicked.connect(onAccepted)
        comboBox.currentIndexChanged.connect(onTheme)

        return dialog

    actionAccessories = QtGui.QAction(mw)
    actionAccessories.setIconText("Accessories")

    actionPref = QtGui.QAction(mw)
    actionPref.setText("IconThemes")
    actionPref.setObjectName("Std_IconThemes")

    menu = QtGui.QMenu(mw)
    actionAccessories.setMenu(menu)
    menu.addAction(actionPref)

    addMenu()
    applyIcons()

    mw.workbenchActivated.connect(addMenu)
    mw.workbenchActivated.connect(applyIcons)
    actionPref.triggered.connect(onPreferences)


# Single instance
if mw.findChild(QtGui.QAction, "Std_IconThemes"):
    pass
else:
    iconThemes()
