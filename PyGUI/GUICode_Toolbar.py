from tkinter import *
import json

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
    _Tools=[]

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

    try:
        file = open("Data\\toolbar.json", "r")
        data=file.read()
        file.close()
    except Exception as e:
        print(e)
        return

    try:
        _Tools=json.loads(data)
    except Exception as e:
        print(e)
        return

    #from tools file
    lbl=Label(_ToolbarContainer)
    lbl.configure(relief="raised")
    lbl.configure(text="Toolbar",font="Arial 10 bold")
    lbl.pack(side="top",fill="x")
    for i in range(len(_Tools["Tools"])):
        lbl=Label(_ToolbarContainer)
        lbl.configure(relief="raised")
        lbl.configure(text=_Tools["Tools"][i]["Group Name"])
        lbl.pack(side="top",fill="x")
        for j in range(len(_Tools["Tools"][i]["Buttons"])):
            btn=Button(_ToolbarContainer)
            btn.configure(relief="flat",background="white")
            if _Tools["Tools"][i]["Buttons"][j]["Name"]=="Select": 
                btn.configure(background="wheat3")
                _ToolSelected="Select"
            btn.bind("<ButtonPress>", ToolButton_MouseButtonPress)
            btn.configure(width=20,height=1,text=_Tools["Tools"][i]["Buttons"][j]["Name"])
            btn.pack(side="top",fill="x")

            if "Properties" in _Tools["Tools"][i]["Buttons"][j]:
                if _Tools["Tools"][i]["Buttons"][j]["Properties"].lower().endswith(".json")==True:
                    try:
                        file = open("Data\\"+_Tools["Tools"][i]["Buttons"][j]["Properties"], "r")
                        data=file.read()
                        file.close()
                    except Exception as e:
                        print(e)

                    try:
                        _Tools["Tools"][i]["Buttons"][j]["Properties"]=json.loads(data)
                    except Exception as e:
                        print(e)

