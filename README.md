# IconThemes
Icon themes for FreeCAD

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [About](#about)
- [Installation](#installation)
  - [Via Addon Manager (recommended)](#via-addon-manager-recommended)
  - [Manual installation](#manual-installation)
- [Usage](#usage)
- [Usage (legacy)](#usage-legacy)
- [Creating themes](#creating-themes)
  - [Prerequisites](#prerequisites)
  - [Preparing the theme](#preparing-the-theme)
  - [Compiling the theme](#compiling-the-theme)
- [Feedback](#feedback)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## About
This module adds support for icon themes to FreeCAD.

It uses the resource files (.rcc) of QT (FreeCAD's interface framework). rcc-files bundle multiple resources into a single which is perfect for theming.

## Installation
### Via addon manager (recommended)
This module can be installed via the FreeCAD [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#1-builtin-addon-manager). In FreeCAD, Open Tools > Addon Manager and search for "IconThemes" in the list.

### Via manual installation

Install path for FreeCAD modules depends on the operating system used:

- Linux: `/home/user_name/.FreeCAD/Mod/IconThemes/InitGui.py`
- MacOS: `/Users/user_name/Library/Preferences/FreeCAD/Mod/IconThemes/InitGui.py`
- Windows: `C:\Users\user_name\AppData\Roaming\FreeCAD\Mod\IconThemes\InitGui.py`

## Usage
For the demonstration purposes demo.rcc icon theme was provided. 

Move the demo.rcc to the appropriate location:

- On Linux: `/home/user_name/.FreeCAD/Gui/Icons/demo.rcc`
- On MacOS: `/Users/user_name/Library/Preferences/FreeCAD/Gui/Icons/demo.rcc`
- On Windows: `C:\Users\user_name\AppData\Roaming\FreeCAD\Gui\Icons\demo.rcc`

**Note: The folder might not exist, but you can create them manually**

You can then open the icon themes preferences in FreeCAD (Accessories > IconThemes) and choose the icon theme.

![screenshot-of-FC-Accessories-dropdown](https://user-images.githubusercontent.com/4140247/64272349-2b549a00-cf0d-11e9-90c9-84e3f8191b2d.png)

## Usage (legacy)
For the demonstration purposes DemoTheme.zip icon theme was provided. 

Extract the DemoTheme.zip archive to the appropriate location:

- On Linux: `/home/user_name/.FreeCAD/Gui/Icons/DemoTheme`
- On MacOS: `/Users/user_name/Library/Preferences/FreeCAD/Gui/Icons/DemoTheme`
- On Windows: `C:\Users\user_name\AppData\Roaming\FreeCAD\Gui\Icons\DemoTheme`

## Creating themes
### Prerequisites
You need [QT](https://www.qt.io/)'s [resource compiler (rcc)](https://doc.qt.io/qt-5/rcc.html). You can get it [by installing the QT developer tools](https://www.qt.io/product/development-tools).

### Preparing the theme
Ingredients of a typical FreeCAD icon pack (all files located in a single folder):

- Icons preferably in the SVG format (e.g. view-top.svg)
- index.theme file
- .qrc file

You can find such a structure in `demo-rcc-assets`.

The contents of an index.theme file:

```
[Icon Theme]
Name=Demo
Comment=Demo icon theme pack
Inherits=FreeCAD-default
Directories=scalable

[scalable]
Size=64
Type=Scalable
MinSize=1
MaxSize=256
```

The contents of a .qrc file:

```
<!DOCTYPE RCC><RCC version="1.0">
    <qresource prefix="/icons/Demo">
        <file>index.theme</file>
    </qresource>
    <qresource prefix="/icons/Demo/scalable">
        <file>view-top.svg</file>
    </qresource>
</RCC>
```

**Note:** There is still work being done, but for now use the same icon file names that can be found in the [FreeCAD source code](https://github.com/FreeCAD/FreeCAD).

### Compiling the theme
QT's resource compiler tool (rcc) is used to compile the contents you specified in the .qrc-file into a single .rcc-file.

```
/usr/bin/rcc --binary demo.qrc -o demo.rcc --format-version 1
```

**Note 1:** If current version of rcc tool is used and to preserve support for Qt4 and older Qt5 versions (likely versions below Qt 5.9). Use the --format-version, otherwise you don't need to use it.

**Note 2:** The path of rcc tool depends on your OS:

- Linux: `/usr/bin/rcc`
- MacOS: `/usr/local/Cellar/qt/{your QT version}/bin/rcc`

## Feedback
Feedback can be posted to this [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=17901)

### License
LGPLv2.1