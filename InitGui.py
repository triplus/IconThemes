# Icon themes for FreeCAD
# Copyright (C) 2016, 2017 triplus @ FreeCAD
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


def iconThemes():
    """Icon themes for FreeCAD."""

    import os
    import FreeCADGui as Gui
    import FreeCAD as App
    from PySide import QtGui
    from PySide import QtCore
    import IconThemesLocator

    mw = Gui.getMainWindow()
    timer = IconThemesLocator.delayTimer()

    appliedIcons = []
    defaultIcons = {}

    noneSvg = """<svg
        xmlns="http://www.w3.org/2000/svg" height="64" width="64">
         <rect height="64" width="64" fill="none" />
        </svg>"""

    nonePix = QtGui.QPixmap()
    nonePix.loadFromData(noneSvg)

    noneIcon = QtGui.QIcon(nonePix)

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
            try:
                folder = themeFolder.decode("UTF-8")
            except AttributeError:
                folder = themeFolder

            path = (App.getUserAppDataDir() +
                    "Gui" +
                    os.path.sep +
                    "Icons" +
                    os.path.sep +
                    folder +
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
            try:
                current = paramGet.GetString("ThemeFolder").decode("UTF-8")
            except AttributeError:
                current = paramGet.GetString("ThemeFolder")

            comboBox.blockSignals(True)

            comboBox.clear()

            for i in folders:
                try:
                    comboBox.addItem(i.decode("UTF-8"))
                except AttributeError:
                    comboBox.addItem(i)

            for count in range(comboBox.count()):
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
                try:
                    paramGet.SetString("ThemeFolder", text.encode("UTF-8"))
                except TypeError:
                    paramGet.SetString("ThemeFolder", text)
            else:
                paramGet.RemString("ThemeFolder")

            del appliedIcons[:]
            resetIcons()

            applyIcons()
            updateIconArea()

        def updateIconArea():
            """
            Update icons in the icon preview area.
            """
            iconArea.blockSignals(True)
            iconArea.clear()

            if paramGet.GetBool("DesignerMode"):

                actions = actionList()

                for i in actions:
                    item = QtGui.QListWidgetItem()
                    item.setToolTip(actions[i].toolTip())
                    item.setData(33, actions[i].objectName())
                    item.setText(actions[i].text().replace("&", ""))

                    if actions[i].icon():
                        item.setIcon(actions[i].icon())
                    else:
                        item.setIcon(noneIcon)

                    iconArea.addItem(item)

            else:
                icons = themeIcons()

                for i in icons:
                    item = QtGui.QListWidgetItem(iconArea)
                    item.setIcon(QtGui.QIcon(i))

            iconArea.sortItems(QtCore.Qt.AscendingOrder)

            iconArea.blockSignals(False)

        def onSelected():
            """
            Update icon file name on selection.
            """
            if paramGet.GetBool("DesignerMode"):
                item = iconArea.currentItem()
                if item:
                    labelIconName.setText(item.data(33) + ".svg")
                else:
                    pass
            else:
                pass

        def onDesignerMode():
            """
            Enable or disable the designer mode.
            """
            if paramGet.GetBool("DesignerMode"):
                paramGet.SetBool("DesignerMode", 0)
                labelIconName.setVisible(False)
                buttonDesignerMode.setChecked(False)
            else:
                paramGet.SetBool("DesignerMode", 1)
                labelIconName.setVisible(True)
                buttonDesignerMode.setChecked(True)

            updateIconArea()

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

            if paramGet.GetBool("DesignerMode"):
                labelIconName.setVisible(True)
                buttonDesignerMode.setChecked(True)
            else:
                labelIconName.setVisible(False)
                buttonDesignerMode.setChecked(False)

            updateComboBox()
            updateIconArea()

        dialog = QtGui.QDialog(mw)
        dialog.resize(800, 450)
        dialog.setWindowTitle("IconThemes")
        dialog.setObjectName("IconThemes")
        layout = QtGui.QVBoxLayout()
        dialog.setLayout(layout)

        comboBox = QtGui.QComboBox(dialog)
        comboBox.setMinimumWidth(220)

        labelIconName = QtGui.QLabel(dialog)
        labelIconName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        iconArea = QtGui.QListWidget(dialog)
        iconArea.setParent(dialog)
        iconArea.setIconSize(QtCore.QSize(48, 48))
        iconArea.setGridSize(QtCore.QSize(108, 96))
        iconArea.sortItems(QtCore.Qt.AscendingOrder)
        iconArea.setViewMode(QtGui.QListView.IconMode)
        iconArea.setResizeMode(QtGui.QListView.Adjust)

        buttonDesignerMode = QtGui.QPushButton("D", dialog)
        buttonDesignerMode.setToolTip("Designer mode")
        buttonDesignerMode.setMaximumWidth(40)
        buttonDesignerMode.setCheckable(True)

        buttonClose = QtGui.QPushButton("Close", dialog)
        buttonClose.setDefault(True)

        layoutTop = QtGui.QHBoxLayout()
        layoutTop.addWidget(comboBox)
        layoutTop.addStretch(1)
        layoutTop.addWidget(labelIconName)

        layoutBottom = QtGui.QHBoxLayout()
        layoutBottom.addWidget(buttonDesignerMode)
        layoutBottom.addStretch(1)
        layoutBottom.addWidget(buttonClose)

        layout.insertLayout(0, layoutTop)
        layout.insertWidget(1, iconArea)
        layout.insertLayout(2, layoutBottom)

        prefDefaults()

        dialog.finished.connect(onFinished)
        buttonClose.clicked.connect(onAccepted)
        comboBox.currentIndexChanged.connect(onTheme)
        iconArea.itemSelectionChanged.connect(onSelected)
        buttonDesignerMode.clicked.connect(onDesignerMode)

        return dialog

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
                actionAccessories = QtGui.QAction(mw)
                actionAccessories.setObjectName("AccessoriesMenu")
                actionAccessories.setIconText("Accessories")
                menu = QtGui.QMenu(mw)
                actionAccessories.setMenu(menu)
                menu.addAction(pref)

                def addMenu():
                    """Add accessories menu to the menubar."""

                    mb = mw.menuBar()

                    toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")

                    if toolsMenu:
                        toolsMenu.addAction(actionAccessories)
                    else:
                        pass

                addMenu()
                mw.workbenchActivated.connect(addMenu)

    def onStart():
        """Start icon themes."""

        start = False
        try:
            mw.workbenchActivated
            start = True
        except AttributeError:
            pass

        if start:
            timer.stop()
            timer.deleteLater()
            accessoriesMenu()
            applyIcons()
            mw.workbenchActivated.connect(applyIcons)

    timer.timeout.connect(onStart)
    timer.start(500)


iconThemes()
