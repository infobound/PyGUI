from tkinter import *
import json
import Form
import GUICode
import GUICode_IO
import GUICode_Toolbar

global _form
global _propertiesFrame
#global _designFrame

_form=Form.Form()

def BuildInterface(window):
    global _form
    global _propertiesFrame
    #global _designFrame

    _windowWidth, _windowHeight = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (_windowWidth, _windowHeight))
    window.minsize(800, 600)
    window.resizable(1, 1)
    window.title("PyPOS - A tkinter form designer")
    window.configure(background="#d9d9d9")

    def CallLoadForm():
        global _form
        _form=GUICode_IO.LoadForm()
        GUICode.UpdateForm(_form)

    #menu bar
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda: print("to do - Menu New"))
    filemenu.add_command(label="Open", command=lambda: CallLoadForm())
    filemenu.add_command(label="Save", command=lambda: GUICode_IO.SaveForm())
    filemenu.add_command(label="Save as...", command=lambda: print("to do - Menu Save as"))
    filemenu.add_command(label="Export...", command=lambda: print("to do - Menu Export"))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=lambda: print("to do - Menu undo"))
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=lambda: print("to do - Menu cut"))
    editmenu.add_command(label="Copy", command=lambda: print("to do - Menu copy"))
    editmenu.add_command(label="Paste", command=lambda: print("to do - Menu paste"))
    editmenu.add_command(label="Delete", command=lambda: print("to do - Menu delete"))
    editmenu.add_command(label="Select All", command=lambda: print("to do - Menu select all"))
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=lambda: print("to do - Menu about"))

    window.config(menu=menubar)

    
    GUICode_Toolbar.Init(window)
    GUICode_Toolbar.BuildToolbar()





    #design frame
    design=Frame(window)
    design.configure(background="dim grey",relief="sunken",width=_windowWidth-150-200,padx=5,pady=5)
    design.pack(side="left", fill="both")
    _designFrame=GUICode.BuildForm(design,_form)
    GUICode_IO.Init(_form,_designFrame)

    #properties window
    properties=Frame(window)
    propertiesCanvas=Canvas(properties)
    propertiesFrameScrollbar=Scrollbar(properties,orient="vertical",command=propertiesCanvas.yview)
    propertiesScrollableFrame=Frame(propertiesCanvas)
    _propertiesFrame=propertiesScrollableFrame

    propertiesScrollableFrame.bind(
        "<Configure>",
        lambda e: propertiesCanvas.configure(
            scrollregion=propertiesCanvas.bbox("all")
        )
    )

    propertiesCanvas.create_window((0, 0), window=propertiesScrollableFrame, anchor="nw")
    propertiesCanvas.config(yscrollcommand=propertiesFrameScrollbar.set)

    GUICode.initPropertiesFrame(propertiesScrollableFrame)
    GUICode.ShowProperties(_form)

    properties.configure(relief="raised")
    propertiesCanvas.configure(width=150)
    
    properties.pack(side="left", fill="both")
    propertiesCanvas.pack(side="left", fill="y")
    propertiesFrameScrollbar.pack(side="right", fill="y")
    propertiesScrollableFrame.pack()








    





