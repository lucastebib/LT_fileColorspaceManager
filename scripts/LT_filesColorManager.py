# coding=utf-8

import pymel.core as pm
import os

# Create empty lists
nodeFiles = []
nodesWithFile = []
filePathList = []
fileNameList = []
fileColorspaceList = []
fullName = []
colorspacesList = pm.colorManagementPrefs(q=True, inputSpaceNames=True)
userDir = pm.internalVar(userAppDir=True)
mayaVersion = pm.about(v=True)
iconsPath = os.path.join(userDir, mayaVersion + '/prefs/icons/LT_filesColorManager')
artstationIcon = iconsPath + '/artstation24.png'
linkedinIcon = iconsPath + '/linkedin24.png'
gumroadIcon = iconsPath + '/gumroad24.png'


# Links
def hyperlinks(value):
    if value == 0:
        os.startfile('https://www.artstation.com/lucastebib')
    if value == 1:
        os.startfile('https://www.linkedin.com/in/tebiblucas')
    if value == 2:
        os.startfile('https://www.gumroad.com/lucastebib')


# Clear the listview and display the current nodes in the scene.
def refreshList(*args):
    global nodeFiles

    # Clear lists
    del nodesWithFile[:]
    del fullName[:]
    del fileColorspaceList[:]
    del nodeFiles[:]
    del filePathList[:]
    del fileNameList[:]

    # Clear all items in list.
    pm.textScrollList(filesSelector, e=True, removeAll=True)

    # Collect all files in the scene.
    nodeFiles = pm.ls(type='file')

    # Check if the nodes are actually pointing to a file and keep only them
    for i in nodeFiles:
        filePath = pm.getAttr("%s.fileTextureName" % i)
        if filePath:
            nodesWithFile.append(i)

    # Get the file path, the name and the colorspace of each file
    for e in nodesWithFile:
        # Get the file path of each node pointing to a file
        filePath = pm.getAttr("%s.fileTextureName" % e)
        filePathList.append(str(filePath))

        # Get the filename of each file
        fileName = os.path.basename(filePath)
        fileNameList.append(fileName)

        # Get the colorspace of each file node
        fileColorspace = pm.getAttr("%s.colorSpace" % e)
        fileColorspaceList.append(fileColorspace)

    for n, b, c in zip(nodesWithFile, fileNameList, fileColorspaceList):
        fullName.append(n + ' | ' + '' + b + ' | ' + c)

    # Add nodes with file to the listview.
    for obj in fullName:
        pm.textScrollList(filesSelector, e=True, append=obj)


# Selection function
def selectInTextList(*args):
    nodeList = []

    # Collect a list of selected items.
    # 'or []' converts it to a list when nothing is selected to prevent errors.
    selectedItems = pm.textScrollList(filesSelector, q=True, si=True) or []

    # Get the node name based on the first part of the string selection
    for i in selectedItems:
        nodeName = i.split(' | ')
        nodeList.append(nodeName[0])

    # Use a list comprehension to remove all nodes that no longer exist in the scene.
    newSelection = [obj for obj in nodeList if pm.objExists(obj)]

    pm.select(newSelection)
    return newSelection


# Apply function
def apply(*args):
    # Get selected file nodes
    selection = pm.ls(sl=True, type='file')

    # Get the colorspace to apply from the dropdown menu
    newColorspace = pm.optionMenu(colorspacesMenu, q=True, value=True)

    # Change the colorspace to the one desired and check 'Ignore Color Space file Rules' parameter
    for i in selection:
        pm.setAttr('%s.colorSpace' % i, newColorspace, type='string')
        pm.setAttr('%s.ignoreColorSpaceFileRules' % i, 1)

    refreshList()
    pm.select(d=True)


# Create window.
# Delete the UI if it exists - basically ensure we only ever have one instance running
# try:
#     pm.deleteUI(myWindow)
# except:
#     myWindow = pm.window(title='Files Color Manager v1.0', h=400, w=350, sizeable=True)

filesSelectorForm = pm.formLayout('main_form', w=350, h=400)

filesSelector = pm.textScrollList('filesSelector', allowMultiSelection=True, selectCommand=selectInTextList)

pm.formLayout('mainForm', e=True,
              attachForm=[('filesSelector', 'top', 5), ('filesSelector', 'bottom', 109), ('filesSelector', 'right', 5),
                          ('filesSelector', 'left', 5)])

colorspacesMenu = pm.optionMenu('colorspacesMenu', label='Color Space', w=1)
for i in colorspacesList:
    pm.menuItem(i)

pm.formLayout('mainForm', e=True, attachForm=[('colorspacesMenu', 'top', 5), ('colorspacesMenu', 'bottom', 84),
                                              ('colorspacesMenu', 'right', 5), ('colorspacesMenu', 'left', 5)],
              attachControl=[('colorspacesMenu', 'top', 5, 'filesSelector')])

refreshButton = pm.button('refreshButton', label='Refresh', align='center', command=refreshList)
applyButton = pm.button('applyButton', label='Apply', align='center', command=apply, bgc=(0.33, 0.5, 0.33))

pm.formLayout('mainForm', e=True,
              attachForm=[('refreshButton', 'top', 5), ('refreshButton', 'bottom', 34), ('refreshButton', 'right', 5),
                          ('refreshButton', 'left', 5), ('applyButton', 'top', 5), ('applyButton', 'bottom', 34),
                          ('applyButton', 'right', 5), ('applyButton', 'left', 5)],
              attachControl=[('refreshButton', 'top', 5, 'colorspacesMenu'),
                             ('applyButton', 'top', 5, 'colorspacesMenu'), ('applyButton', 'left', 5, 'refreshButton')],
              attachPosition=[('refreshButton', 'right', 0, 50)])

linksRow = pm.rowLayout('linksRow', nc=4)
copyright = pm.text(label='Created by Lucas TEBIB - v1.0 ', align='right', font='obliqueLabelFont')
artstationButton = pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.artstation.com/lucastebib')",
                                     i=artstationIcon, parent=linksRow, width=24, align='right')
linkedinButton = pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.linkedin.com/in/tebiblucas')",
                                   i=linkedinIcon, parent=linksRow, width=24, align='right')
gumroadButton = pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.gumroad.com/lucastebib')",
                                  i=gumroadIcon, parent=linksRow, width=24, align='right')

pm.formLayout('mainForm', e=True,
              attachForm=[('linksRow', 'top', 5), ('linksRow', 'bottom', 5), ('linksRow', 'right', 0)],
              attachControl=[('linksRow', 'top', 5, 'applyButton')])

refreshList()
pm.showWindow(myWindow)
