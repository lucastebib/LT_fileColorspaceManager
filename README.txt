########## DESCRIPTION ##########

LT_FilesColorManager has been created in order to change the input colorspace (known as IDT) of several File nodes at a time.
When having a lot of files in a Maya scene, it can be a really repetitive and tedious task to go through all of the File nodes we need to change.

This tool provides an interface to select several files and the desired colorspace for those files.

This should work with Maya 2016 and above.


########## INSTALLATION ##########

- Copy the SCRIPTS and ICONS folder in your user prefs folder.

• Windows:
Default is C:\Users\My Documents\Documents\maya\<version>\prefs\

• Linux:
~<username>/Maya/<version>/prefs/

• MacOS:
/Users/<username>/Library/Preferences/Autodesk/Maya/<version>/prefs/


- In Maya, open the Script Editor, create a new Python shelf and copy and paste this code:
import LT_filesColorManager
reload(LT_filesColorManager)

Then press Ctrl+Enter.
From the Script Editor, you can also drag and drop this code in a shelf in order to create a button for this tool.


########## LICENSE ##########

This tool is completely free of charge. You can share it, but you may not sell it in any way, shape, or form. No profit whatsoever is allowed under any circumstances.
This tool is licensed under the CC BY-NC-ND 4.0 license.


########## CONTACT ##########

For any enquiries or bug report, please send me an email: ltebib@artfx.fr

www.artstation.com/lucastebib
www.linkedin.com/in/tebiblucas
www.gumroad.com/lucastebib