from tkinter import *
import json
import Form
import GUICode

global _form
global _propertiesFrame
_form=Form.Form()

def BuildInterface(window):
    global _form
    global _propertiesFrame

    _windowWidth, _windowHeight = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (_windowWidth, _windowHeight))
    window.minsize(800, 600)
    window.resizable(1, 1)
    window.title("PyPOS - A tkinter form designer")
    window.configure(background="#d9d9d9")

    def donothing():
        return

    #menu bar
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda: GUICode.BuildForm(design,_form))
    filemenu.add_command(label="Open", command=lambda: GUICode.LoadForm())
    filemenu.add_command(label="Save", command=lambda: GUICode.SaveForm())
    filemenu.add_command(label="Save as...", command=lambda: GUICode.BuildForm(design,_form))
    filemenu.add_command(label="Export...", command=lambda: GUICode.BuildForm(design,_form))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=donothing)

    window.config(menu=menubar)

    #toolbar
    toolbar=Frame(window)
    toolbarCanvas=Canvas(toolbar)
    toolbarFrameScrollbar=Scrollbar(toolbar,orient="vertical",command=toolbarCanvas.yview)
    toolbarScrollableFrame=Frame(toolbarCanvas)

    toolbarScrollableFrame.bind(
        "<Configure>",
        lambda e: toolbarCanvas.configure(
            scrollregion=toolbarCanvas.bbox("all")
        )
    )

    toolbarCanvas.create_window((0, 0), window=toolbarScrollableFrame, anchor="nw")
    toolbarCanvas.config(yscrollcommand=toolbarFrameScrollbar.set)

    GUICode.BuildToolsList(toolbarScrollableFrame)

    toolbar.configure(relief="raised")
    toolbarCanvas.configure(width=150)
    
    toolbar.pack(side="left", fill="both")
    toolbarCanvas.pack(side="left", fill="y")
    toolbarFrameScrollbar.pack(side="right", fill="y")
    toolbarScrollableFrame.pack()

    #design frame
    design=Frame(window)
    design.configure(background="dim grey",relief="sunken",width=_windowWidth-150-200,padx=5,pady=5)
    design.pack(side="left", fill="both")
    GUICode.BuildForm(design,_form)

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








    





