from tkinter import *
import GUICode_Toolbar as TB

global _propertiesFrame
global _props

def Init(parent):
    global _propertiesFrame
    _propertiesFrame=parent

def BuildTextProperty(fra):
    widget=Entry(fra)
    return widget

def ShowFormProperties(obj):
    global _propertiesFrame
    global _props

    for child in _propertiesFrame.winfo_children():
        child.destroy()
    
    fra=Frame(_propertiesFrame)
    fra.pack(fill="both")

    rowCnt=0
    _props=[]
    lbl=Label(fra)
    lbl.configure(relief="raised")
    lbl.configure(text="Properties",font="Arial 10 bold")
    lbl.grid(columnspan=2,row=rowCnt,sticky="we")
    for key, val in obj.Properties.items():
        rowCnt+=1
        _props.append(StringVar(fra, value=val))

        lbl=Label(fra)
        lbl.configure(text=str(key))
        lbl.grid(column=0,row=rowCnt,sticky="we")

        widget=Entry(fra)
        widget.configure(textvariable=_props[rowCnt-1])
        widget.grid(column=1,row=rowCnt,sticky="we")
        widget=None

def ShowWidgetProperties(obj):
    global _propertiesFrame
    global _props

    for child in _propertiesFrame.winfo_children():
        child.destroy()

    fra=Frame(_propertiesFrame)
    fra.pack(fill="both")

    _props=[]
    rowCnt=0
    toolProp=None
    lbl=Label(fra)
    lbl.configure(relief="raised")
    lbl.configure(text="Properties",font="Arial 10 bold")
    lbl.grid(columnspan=2,row=rowCnt,sticky="we")
    for i in range(len(TB._Tools["Tools"])): # this is going through the tool groups at this level
        for j in range(len(TB._Tools["Tools"][i]["Buttons"])): #this is looking at each tool
            if "Properties" in TB._Tools["Tools"][i]["Buttons"][j]:
                toolProp=TB._Tools["Tools"][i]["Buttons"][j]["Properties"]
                if "Base" in toolProp and toolProp["Base"][0]["Type"]==obj.Library and toolProp["Base"][1]["Type"]==obj.Class:
                    #base
                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(relief="raised")
                    lbl.configure(text="Base",font="Arial 10 bold")
                    lbl.grid(columnspan=2,row=rowCnt,sticky="we")

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Library")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=toolProp["Base"][0]["Type"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Class")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=toolProp["Base"][1]["Type"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Name")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=obj.Properties["name"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)
                    
                    #geometry
                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(relief="raised")
                    lbl.configure(text="Geometry",font="Arial 10 bold")
                    lbl.grid(columnspan=2,row=rowCnt,sticky="we")

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="X")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=obj.Properties["x"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Y")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=obj.Properties["y"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Width")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=obj.Properties["width"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(text="Height")
                    lbl.grid(column=0,sticky="w",row=rowCnt)

                    lbl=Label(fra)
                    lbl.configure(text=obj.Properties["height"])
                    lbl.grid(column=1,sticky="w",row=rowCnt)

                    #all other properties
                    rowCnt+=1
                    lbl=Label(fra)
                    lbl.configure(relief="raised")
                    lbl.configure(text="Attributes",font="Arial 10 bold")
                    lbl.grid(columnspan=2,row=rowCnt,sticky="we")

                    for prop in toolProp["Attributes"]:
                        rowCnt+=1
                        lbl=Label(fra)
                        lbl.configure(text=prop["Name"])
                        lbl.grid(column=0,sticky="w",row=rowCnt)

                        lbl=Label(fra)
                        lbl.configure(text=obj.Properties[prop["Name"]])
                        lbl.grid(column=1,sticky="w",row=rowCnt)

                    return

def ShowSelectedList(_form,_selected):
    global _propertiesFrame
    global _props

    for child in _propertiesFrame.winfo_children():
        child.destroy()

    _props=[]

    fra=Frame(_propertiesFrame)
    fra.configure(relief="sunken",bg="white")
    fra.pack(side="top",fill="both")

    lbl=Label(fra)
    lbl.configure(relief="raised")
    lbl.configure(text="Selected ("+str(len(_selected))+")",font="Arial 10 bold")
    lbl.pack(side="top",fill="x")

    for i in range(len(_selected)):
        for j in range(len(_form.Children)):
            if _form.Children[j].Widget==_selected[i]:
                lbl=Label(fra)
                lbl.configure(text=_form.Children[j].Properties["name"],anchor="w")
                if i==0: 
                    lbl.configure(bg="blue",fg="white")
                else:
                    lbl.configure(bg="white")
                lbl.pack(side="top",fill="x")

