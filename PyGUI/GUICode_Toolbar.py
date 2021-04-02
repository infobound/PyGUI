from tkinter import *
import json
import GUICode_IO as io

global _window
global _ToolSelected
global _ToolbarContainer
global _Tools

def Init(window):
    global _window
    global _ToolSelected
    global _ToolbarContainer
    global _Tools

    _window=window
    _ToolSelected=None
    _ToolbarContainer=None
    _Tools=None

def BuildToolbar():
    global _window
    global _ToolSelected
    global _ToolbarContainer

    toolbar=Frame(_window)
    toolbarCanvas=Canvas(toolbar)
    toolbarFrameScrollbar=Scrollbar(toolbar,orient="vertical",command=toolbarCanvas.yview)
    toolbarScrollableFrame=Frame(toolbarCanvas)

    toolbarScrollableFrame.bind(
        "<Configure>",
        lambda e: toolbarCanvas.configure(
            scrollregion=toolbarCanvas.bbox("all")
        )
    )
    _ToolbarContainer=toolbarScrollableFrame

    toolbarCanvas.create_window((0, 0), window=toolbarScrollableFrame, anchor="nw")
    toolbarCanvas.config(yscrollcommand=toolbarFrameScrollbar.set)

    BuildToolsList()

    toolbar.configure(relief="raised")
    toolbarCanvas.configure(width=150)
    
    toolbar.pack(side="left", fill="both")
    toolbarCanvas.pack(side="left", fill="y")
    toolbarFrameScrollbar.pack(side="right", fill="y")
    toolbarScrollableFrame.pack()

def ResetTollbarSelection(_text):
    global _ToolSelected
    global _ToolbarContainer
    
    _ToolSelected=_text
    for i in _ToolbarContainer.children:
        if _ToolbarContainer.children[i].cget("text")==_text:
            _ToolbarContainer.children[i].configure(background="wheat3")
        else:
            _ToolbarContainer.children[i].configure(background="white")

def BuildToolsList():
    global _ToolSelected
    global _ToolbarContainer
    global _Tools

    def ToolButton_MouseButtonPress(event):
        global _ToolSelected

        _ToolSelected=event.widget.cget('text')
        ResetTollbarSelection(_ToolSelected)

    _Tools=io.LoadFile("Data\\toolbar.json")

    #from tools file
    lbl=Label(_ToolbarContainer)
    lbl.configure(relief="raised")
    lbl.configure(text="Toolbar",font="Arial 10 bold")
    lbl.pack(side="top",fill="x")
    for group,tools in _Tools["Toolbar"].items():
        lbl=Label(_ToolbarContainer)
        lbl.configure(relief="raised")
        lbl.configure(text=group)
        lbl.pack(side="top",fill="x")
        for tool,settings in tools.items():
            btn=Button(_ToolbarContainer)
            btn.configure(relief="flat",background="white")
            if tool=="Select": 
                btn.configure(background="wheat3")
                _ToolSelected="Select"
            btn.bind("<ButtonPress>", ToolButton_MouseButtonPress)
            btn.configure(width=20,height=1,text=tool)
            btn.pack(side="top",fill="x")

            if "properties" in settings:
                if type(settings["properties"]) is dict:
                    #nothing to do
                    break
                elif settings["properties"].lower().endswith(".json")==True:
                    settings["properties"]=io.LoadFile("Data\\"+settings["properties"])
