# LT_FilesColorspaceManager

LT_FilesColorspaceManager has been created in order to change the input colorspace (known as IDT) of several File nodes at a time.
When having a lot of files in a Maya scene, it can be a really repetitive and tedious task to go through all of the File nodes we need to change.
This tool provides an interface to select several files and the desired colorspace for those files.
It should work on Maya 2016 and above.

# Installation
Copy the **scripts** and **icons** folder in your user preferences folder.

Windows:
>C:\Users\My Documents\Documents\maya\version\prefs\

• Linux:
>~username/Maya/version/prefs/

• MacOS:
>/Users/username/Library/Preferences/Autodesk/Maya/version/prefs/

# Usage
In Maya, open the **Script Editor**, create a new **Python** shelf and copy and paste this code:

    import LT_filesColorManager
    LT_filesColorManager.run_gui()

Then press **Ctrl+Enter**.
From the **Script Editor**, you can also drag and drop this code in a shelf in order to create a button for this tool.

# License
This tool is completely free of charge. You can share it, but you may not sell it in any way, shape, or form. No profit whatsoever is allowed under any circumstances.
This tool is licensed under the CC BY-NC-ND 4.0 license.
