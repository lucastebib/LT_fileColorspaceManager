#!/usr/bin/env python
# coding=utf-8
"""MODULES IMPORT"""
import pymel.core as pm
import os

# Create variables and empty lists
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


def hyperlinks(value):
    """
    Gives numeric values to each URL.
    :param value: the number corresponding to the desired URL.
    """
    if value == 0:
        os.startfile('https://www.artstation.com/lucastebib')
    if value == 1:
        os.startfile('https://www.linkedin.com/in/tebiblucas')
    if value == 2:
        os.startfile('https://www.gumroad.com/lucastebib')


def refresh_list():
    """
    Clear the listview and display the current nodes in the scene.
    """
    global nodeFiles

    # Clear lists
    del nodesWithFile[:]
    del fullName[:]
    del fileColorspaceList[:]
    del nodeFiles[:]
    del filePathList[:]
    del fileNameList[:]

    # Clear all items in list.
    pm.textScrollList('files_selector', e=True, removeAll=True)

    # Collect all files in the scene.
    nodeFiles = pm.ls(type='file')

    # Check if the nodes are actually pointing to a file and keep only them
    for i in nodeFiles:
        file_path = pm.getAttr("%s.fileTextureName" % i)
        if file_path:
            nodesWithFile.append(i)

    # Get the file path, the name and the colorspace of each file
    for e in nodesWithFile:
        # Get the file path of each node pointing to a file
        file_path = pm.getAttr("%s.fileTextureName" % e)
        filePathList.append(str(file_path))

        # Get the filename of each file
        file_name = os.path.basename(file_path)
        fileNameList.append(file_name)

        # Get the colorspace of each file node
        file_colorspace = pm.getAttr("%s.colorSpace" % e)
        fileColorspaceList.append(file_colorspace)

    for n, b, c in zip(nodesWithFile, fileNameList, fileColorspaceList):
        fullName.append(n + ' | ' + '' + b + ' | ' + c)

    # Add nodes with file to the listview.
    for obj in fullName:
        pm.textScrollList('files_selector', e=True, append=obj)


def select_in_texture_list():
    """
    From the user's selection in the UI, returns a list of correct nodes selection
    :return: new_selection: list of nodes selected
    """
    node_list = []

    # Collect a list of selected items.
    # ' or []' converts it to a list when nothing is selected to prevent errors.
    selected_items = pm.textScrollList('files_selector', q=True, si=True) or []

    # Get the node name based on the first part of the string selection.
    for i in selected_items:
        node_name = i.split(' | ')
        node_list.append(node_name[0])

    # Use a list comprehension to remove all nodes that no longer exist in the scene.
    new_selection = [obj for obj in node_list if pm.objExists(obj)]

    pm.select(new_selection)
    return new_selection


def apply():
    """
    Set the selected colorspace to the selected textures
    """
    # Get selected file nodes
    selection = pm.ls(sl=True, type='file')

    # Get the colorspace to apply from the dropdown menu
    new_colorspace = pm.optionMenu('colorspaces_menu', q=True, value=True)

    # Change the colorspace to the one desired and check 'Ignore Color Space file Rules' parameter
    for i in selection:
        pm.setAttr('%s.colorSpace' % i, new_colorspace, type='string')
        pm.setAttr('%s.ignoreColorSpaceFileRules' % i, 1)

    refresh_list()
    pm.select(d=True)


def run_gui():
    """
    Creates GUI objects and show the window
    """
    window_name = "FilesColorSpaceManager_Window"
    if pm.window(window_name, ex=True):
        pm.deleteUI(window_name, window=True)

    my_window = pm.window(window_name, title='Files Colorspace Manager 1.1', h=400, w=350, sizeable=True, visible=False)

    pm.formLayout('mainForm', w=350, h=400)

    pm.textScrollList('files_selector', allowMultiSelection=True, selectCommand=select_in_texture_list)

    pm.formLayout('mainForm', e=True,
                  attachForm=[('files_selector', 'top', 5), ('files_selector', 'bottom', 109),
                              ('files_selector', 'right', 5),
                              ('files_selector', 'left', 5)])

    pm.optionMenu('colorspaces_menu', label='Color Space', w=1)
    for i in colorspacesList:
        pm.menuItem(i)

    pm.formLayout('mainForm', e=True, attachForm=[('colorspaces_menu', 'top', 5), ('colorspaces_menu', 'bottom', 84),
                                                  ('colorspaces_menu', 'right', 5), ('colorspaces_menu', 'left', 5)],
                  attachControl=[('colorspaces_menu', 'top', 5, 'files_selector')])

    pm.button('refresh_button', label='Refresh', align='center', command=refresh_list)
    pm.button('apply_button', label='Apply', align='center', command=apply, bgc=(0.33, 0.5, 0.33))

    pm.formLayout('mainForm', e=True,
                  attachForm=[('refresh_button', 'top', 5), ('refresh_button', 'bottom', 34),
                              ('refresh_button', 'right', 5),
                              ('refresh_button', 'left', 5), ('apply_button', 'top', 5), ('apply_button', 'bottom', 34),
                              ('apply_button', 'right', 5), ('apply_button', 'left', 5)],
                  attachControl=[('refresh_button', 'top', 5, 'colorspaces_menu'),
                                 ('apply_button', 'top', 5, 'colorspaces_menu'),
                                 ('apply_button', 'left', 5, 'refresh_button')],
                  attachPosition=[('refresh_button', 'right', 0, 50)])

    links_row = pm.rowLayout('linksRow', nc=4)
    pm.text(label='Created by Lucas TEBIB - v1.0 ', align='right', font='obliqueLabelFont')
    pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.artstation.com/lucastebib')",
                      i=artstationIcon, parent=links_row, width=24, align='right')
    pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.linkedin.com/in/tebiblucas')",
                      i=linkedinIcon, parent=links_row, width=24, align='right')
    pm.iconTextButton(st="iconOnly", command="os.startfile('https://www.gumroad.com/lucastebib')",
                      i=gumroadIcon, parent=links_row, width=24, align='right')

    pm.formLayout('mainForm', e=True,
                  attachForm=[('linksRow', 'top', 5), ('linksRow', 'bottom', 5), ('linksRow', 'right', 0)],
                  attachControl=[('linksRow', 'top', 5, 'apply_button')])

    my_window.show()
    refresh_list()
