from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from PIL import ImageTk ,Image

import GUICode_Toolbar as TB
import GUICode as GC
import GUICode_IO as IO

global _propertiesFrame
global _props
global _SelectedWidget

def Init(parent):
    global _propertiesFrame
    _propertiesFrame=parent

def BuildPropertyValueField(propFrame,formChild,propName,propType):
    global _SelectedWidget
    _SelectedWidget=formChild

    if propType=="label":
        widget=Label(propFrame)
        widget.configure(text=formChild.Properties[propName])
    elif propType=="text":
        widget=Entry(propFrame)
        sv=StringVar()
        sv.set(formChild.Properties[propName])
        widget.configure(text=sv)
        if propName=="name":
            widget.bind("<FocusOut>",lambda event,args=propName: UpdateNameProperty(event,args))
        else:
            widget.bind("<FocusOut>",lambda event,args=propName: UpdateTextProperty(event,args))
    elif propType=="font":
        widget=Button(propFrame)
        print("to do - font property pick")
        if formChild.Properties[propName]!="":
            widget.configure(text=formChild.Properties[propName])
        else:
            widget.configure(text="Choose font...")
    elif propType=="color":
        widget=Button(propFrame)
        if formChild.Properties[propName]!="":
            widget.configure(bg=formChild.Properties[propName], text=formChild.Properties[propName])
        else:
            widget.configure(text="Choose color...")
        widget.configure(command=lambda: UpdateColorProperty(widget,propName))
    elif propType=="file":
        widget=Button(propFrame)
        print("to do - file property pick")
        if formChild.Properties[propName]!="":
            widget.configure(text=formChild.Properties[propName])
        else:
            widget.configure(text="Choose file...")
        widget.configure(command=lambda: UpdateFileProperty(widget,propName))
    elif propType=="int":
        widget=Entry(propFrame)
        sv=StringVar()
        sv.set(formChild.Properties[propName])
        widget.configure(text=sv)
        widget.bind("<FocusOut>",lambda event,args=propName: UpdateIntegerProperty(event,args))

        #is it geometry?
    elif propType=="select":
        _toolPropOptions=TB._Tools["Toolbar"][formChild.Properties["library"]][formChild.Properties["class"]]["properties"]["attributes"][propName]["options"]
        vlist = []
        for option in _toolPropOptions:
            vlist.append(option["value"])

        widget = ttk.Combobox(propFrame, values = vlist,state="readonly")
        widget.set(formChild.Properties[propName])
        widget.bind("<<ComboboxSelected>>",lambda event,args=propName: UpdateSelectProperty(event,args))
    else:
        widget=Label(propFrame)
        widget.configure(text=formChild.Properties[propName])

    return widget

def ShowFormProperties(obj):
    global _propertiesFrame
    global _props
    global _SelectedWidget
    _SelectedWidget=None

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
    #show the properties of a widget, obj is a child from the form class object
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

    #here I loop through the tools and the tool properties to get attributes instead of through the form
    #object because I can make the save bekept smaller, no need to save default or description.
    for group,tools in TB._Tools["Toolbar"].items(): # this is going through the tool groups at this level
        for tool,settings in tools.items(): #this is looking at each tool
            if "properties" in settings:
                toolProp=settings["properties"]
                if "base" in toolProp:
                   if toolProp["base"]["library"]["default"]==obj.Library and toolProp["base"]["class"]["default"]==obj.Class:
                       for attribgroup, attrib in toolProp.items():
                            #group header
                            rowCnt+=1
                            lbl=Label(fra)
                            lbl.configure(relief="raised")
                            lbl.configure(text=attribgroup,font="Arial 10 bold")
                            lbl.grid(columnspan=2,row=rowCnt,sticky="we")
                            for attribname, attribsettings in attrib.items():
                                rowCnt+=1
                                lbl=Label(fra)
                                lbl.configure(text=attribname)
                                if "descriptionbreak" in attribsettings:
                                    if attribsettings["descriptionbreak"]!="":
                                        tooltip=Balloon(win)
                                        tooltip.bind_widget(lbl,balloonmsg=attribsettings["description"])
                                lbl.grid(column=0,sticky="w",row=rowCnt)

                                widget=BuildPropertyValueField(fra,obj,attribname,attribsettings["type"])
                                widget.grid(column=1,sticky="w",row=rowCnt)

                                #val=StringVar()
                                #val.set(obj.Properties[attribname])
                                #widget=Entry(fra)
                                #widget.configure(text=val)
                                #widget.grid(column=1,sticky="w",row=rowCnt)
#tab#tab#tab#tab#tab#tab#tab#tab I hate tabs
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

def UpdateNameProperty(event,args):
    global _SelectedWidget

    _newname=event.widget.get()
    if _SelectedWidget.Properties["name"]==_newname: return #no change

    if GC.WidgetNameAlreadyExists(_newname)==True:
         msg=messagebox.showerror(title="Name Change Fail", message="The widget name already exists.")
         sv=StringVar()
         sv.set(_SelectedWidget.Properties["name"])
         event.widget.configure(text=sv)
    else:
        _SelectedWidget.Properties[args]=event.widget.get()

def UpdateTextProperty(event,args):
    global _SelectedWidget
    _SelectedWidget.Properties[args]=event.widget.get()
    _SelectedWidget.Widget.configure({args: event.widget.get()})

def UpdateFileProperty(widget,property):
    global _SelectedWidget

    if property=="image":
        filename=IO.LoadImage()
        
        if filename=="":
            msg=messagebox.showerror(title="Image Load Fail", message="Unable to load image file.")
        elif filename=="cancel":
            return
        else:
            img=ImageTk.PhotoImage(Image.open(filename))
            _SelectedWidget.Properties["image"]=filename
            _SelectedWidget.Widget.configure(image=img)

            btntxt=filename.split("/")[len(filename.split("/"))-1]
            widget.configure(text=btntxt)
    else:
        #not sure if anything will ever go here
        return


def UpdateColorProperty(widget,property):
    global _SelectedWidget

    colors = askcolor(title="Choose "+property+" color")
    if colors==None: return

    _SelectedWidget.Properties[property]=colors[1]
    _SelectedWidget.Widget.configure({property: colors[1]})
    widget.configure(bg=colors[1], text=colors[1])

def UpdateFontProperty():
    return

def UpdateIntegerProperty(event,args):
    global _SelectedWidget
    newvalue=event.widget.get()
    if newvalue=="": newvalue="0"

    if is_number(newvalue)==False:
        msg=messagebox.showerror(title="Value Change Fail", message="The value must be a number.")
    else:
        _SelectedWidget.Properties[args]=event.widget.get()
        if args in TB._Tools["Toolbar"][_SelectedWidget.Properties["library"]][_SelectedWidget.Properties["class"]]["properties"]["geometry"]:
            print("to do - Update Int Prop: reset selection boxes and place/pack/grid from form properties.")
            _SelectedWidget.Widget.place({args: newvalue})
        else:
            _SelectedWidget.Widget.configure({args: newvalue})

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def UpdateSelectProperty(event,property):
    global _SelectedWidget
    _SelectedWidget.Properties[property]=event.widget.get()
    _SelectedWidget.Widget.configure({property: event.widget.get()})
