from tkinter import *
import json
import Form
import Child
from PIL import Image, ImageTk
from random import *
import GUICode_Toolbar as TB
import GUICode_Properties as PROP

global _MouseStartingX
global _MouseStartingY
global _MouseEndingX
global _MouseEndingY
global _SelectionBox
global _form
global _selected
global _SelectionGrips
global _designFrame

_ToolSelected="Select"
_ToolbarContainer=None
_Tools=None
_MouseStartingX=-1
_MouseStartingY=-1
_MouseEndingX=-1
_MouseEndingY=-1
_SelectionBox=None
_form=None
_selected=[]
_SelectionGrips=[]
_designFrame=None


def UpdateForm(form):
    global _form
    _form=form

def BuildForm(parentFrame,Form):
    global _form
    global _designFrame

    _form=Form

    designForm=Frame(parentFrame)
    designForm.configure(height=_form.Properties["height"],width=_form.Properties["width"],relief="raised")
    designForm.place(x=0,y=0)

    designFormTitlebar=Frame(designForm)
    designFormTitlebar.configure(background="blue2")
    designFormTitlebar.place(height=30,width=_form.Properties["width"])

    def designFormContainer_MouseButtonPress(event):
        global _MouseStartingX
        global _MouseStartingY

        _MouseStartingX=event.x
        _MouseStartingY=event.y

    def designFormContainer_MouseButtonRelease(event):
        global _ToolSelected
        global _MouseStartingX
        global _MouseStartingY
        global _MouseEndingX
        global _MouseEndingY
        global _SelectionBox

        _MouseEndingX=event.x
        _MouseEndingY=event.y
        designFormContainer.delete(_SelectionBox)

        
        if TB._ToolSelected=="Select":
            SelectControl()
        else:
            DrawControl()

        TB.ResetTollbarSelection("Select")

        _MouseStartingX=-1
        _MouseStartingY=-1
        _MouseEndingX=-1
        _MouseEndingY=-1

    def designFormContainer_MouseMove(event):
        global _MouseStartingX
        global _MouseStartingY
        global _SelectionBox

        designFormContainer.delete(_SelectionBox)
        _SelectionBox=designFormContainer.create_rectangle(_MouseStartingX, _MouseStartingY, event.x, event.y, outline="blue", width=1, dash=(3))

    def ResetSelection():
        global _selected
        global _SelectionGrips

        for _widget in _selected:
            try:
                _widget.configure(cursor="arrow")
            except Exception as e:
                #why does this happen????
                #only after i select an image for a button, so far.
                print("reset selection - unable to set cursor to arrow")
                print("to do - fix reset selection cursor change")

            _widget.unbind("<ButtonPress>")
            _widget.unbind("<ButtonRelease>")
            _widget.unbind("<B1-Motion>")

        _selected.clear()

        for _grip in _SelectionGrips:
            _grip.destroy()

        _SelectionGrips.clear()

    def SelectControl():
        global _MouseStartingX
        global _MouseStartingY
        global _MouseEndingX
        global _MouseEndingY
        global _selected

        _left=_MouseStartingX
        _top=_MouseStartingY
        _width=_MouseEndingX-_MouseStartingX
        _height=_MouseEndingY-_MouseStartingY
        if _width<0: _width=_MouseStartingX-_MouseEndingX; _left=_MouseEndingX;
        if _height<0: _height=_MouseStartingY-_MouseEndingY; _top=_MouseEndingY;
        
        ResetSelection()

        for i in designFormContainer.children:
            if designFormContainer.children[i].winfo_x()>=_left:
                if designFormContainer.children[i].winfo_y()>=_top:
                    if designFormContainer.children[i].winfo_x()+designFormContainer.children[i].winfo_width()<=_left+_width:
                        if designFormContainer.children[i].winfo_y()+designFormContainer.children[i].winfo_height()<=_top+_height:
                            _selected.append(designFormContainer.children[i])
        
        if len(_selected)==0: 
            PROP.ShowFormProperties(_form)
            return
        elif len(_selected)==1:
            for i in range(len(_form.Children)):
                if _form.Children[i].Widget==_selected[0]:
                    PROP.ShowWidgetProperties(_form.Children[i])
                    break
        else:
            PROP.ShowSelectedList(_form,_selected)
        
        _selected[0].configure(cursor="tcross")
        _selected[0].bind("<ButtonPress>", Selected_MouseButtonPress)
        _selected[0].bind("<ButtonRelease>", Selected_MouseButtonRelease)
        _selected[0].bind("<B1-Motion>", Selected_MouseMove)

        AddPrimaryResizeControls(_selected[0])
        for i in range(1,len(_selected)):
            AddSecondaryResizeControls(_selected[i])

            _selected[i].configure(cursor="tcross")
            _selected[i].bind("<ButtonPress>", Selected_MouseButtonPress)
            _selected[i].bind("<ButtonRelease>", Selected_MouseButtonRelease)
            _selected[i].bind("<B1-Motion>", Selected_MouseMove)

    def Selected_MouseButtonPress(event):
        global _MouseStartingX
        global _MouseStartingY

        _MouseStartingX=event.x
        _MouseStartingY=event.y
        
    def Selected_MouseButtonRelease(event):
        global _MouseStartingX
        global _MouseStartingY
        global _MouseEndingX
        global _MouseEndingY
        global _Selected

        _MouseEndingX=event.x
        _MouseEndingY=event.y

        print("to do - record move to form class")

    def Selected_MouseMove(event):
        global _MouseStartingX
        global _MouseStartingY
        global _Selected
        global _SelectionGrips

        _moveX=_MouseStartingX-event.x
        _moveY=_MouseStartingY-event.y

        for _widget in _selected:
            _widget.place(x=_widget.winfo_x()-_moveX, y=_widget.winfo_y()-_moveY)

        for _widget in _SelectionGrips:
            _widget.place(x=_widget.winfo_x()-_moveX, y=_widget.winfo_y()-_moveY)

    def Resizer_MouseButtonPress(event):
        global _MouseStartingX
        global _MouseStartingY

        _MouseStartingX=event.x
        _MouseStartingY=event.y
        
    def Resizer_MouseButtonRelease(event):
        global _MouseStartingX
        global _MouseStartingY
        global _MouseEndingX
        global _MouseEndingY
        global _Selected

        _MouseEndingX=event.x
        _MouseEndingY=event.y

        print("to do - record resize to form class")
        
    def Resizer_MouseMove(event):
        global _MouseStartingX
        global _MouseStartingY
        global _Selected
        global _SelectionGrips


        #determin which grip is being garbbed to know how the widget is being resized
        #unable to find a way to add custom properties to a canvas widget
        #since the primary grips are alwasy added first and in a specific order I will assume that
        #  their position in the griplist is fixed at 0=top left,1=bottom left,2=top right and 3=bottom right.
        #  I dont like this code code here :(
        _moveX=_MouseStartingX-event.x
        _moveY=_MouseStartingY-event.y

        _PullDirection=""
        for i in range(4):
            if _SelectionGrips[i]==event.widget:
                if i==0: #top left
                    #move grips
                    for j in range(len(_selected)):
                        _SelectionGrips[(j*4)+0].place(x=_SelectionGrips[(j*4)+0].winfo_x()-_moveX, y=_SelectionGrips[(j*4)+0].winfo_y()-_moveY) #top left
                        _SelectionGrips[(j*4)+1].place(x=_SelectionGrips[(j*4)+1].winfo_x()-_moveX) #bottom left
                        _SelectionGrips[(j*4)+2].place(y=_SelectionGrips[(j*4)+2].winfo_y()-_moveY) #top right

                    #resize button
                    for j in range(len(_selected)):
                        _selected[j].place(x=_selected[j].winfo_x()-_moveX, y=_selected[j].winfo_y()-_moveY, width=_selected[j].winfo_width()+_moveX, height=_selected[j].winfo_height()+_moveY)
                if i==1: #bottom left
                    #move grips
                    for j in range(len(_selected)):
                        _SelectionGrips[(j*4)+0].place(x=_SelectionGrips[(j*4)+0].winfo_x()-_moveX) #top left
                        _SelectionGrips[(j*4)+1].place(x=_SelectionGrips[(j*4)+1].winfo_x()-_moveX, y=_SelectionGrips[(j*4)+1].winfo_y()-_moveY) #bottom left
                        _SelectionGrips[(j*4)+3].place(y=_SelectionGrips[(j*4)+3].winfo_y()-_moveY) #bottom right

                    #resize button
                    for j in range(len(_selected)):
                        _selected[j].place(x=_selected[j].winfo_x()-_moveX, width=_selected[j].winfo_width()+_moveX, height=_selected[j].winfo_height()-_moveY)
                if i==2: #top right
                    #move grips
                    for j in range(len(_selected)):
                        _SelectionGrips[(j*4)+0].place(y=_SelectionGrips[(j*4)+0].winfo_y()-_moveY) #top left
                        _SelectionGrips[(j*4)+2].place(x=_SelectionGrips[(j*4)+2].winfo_x()-_moveX, y=_SelectionGrips[(j*4)+2].winfo_y()-_moveY) #top right
                        _SelectionGrips[(j*4)+3].place(x=_SelectionGrips[(j*4)+3].winfo_x()-_moveX) #bottom right

                    #resize button
                    for j in range(len(_selected)):
                        _selected[j].place(y=_selected[j].winfo_y()-_moveY, width=_selected[j].winfo_width()-_moveX, height=_selected[j].winfo_height()+_moveY)
                if i==3: #bottom right
                    #move grips
                    for j in range(len(_selected)):
                        _SelectionGrips[(j*4)+1].place(y=_SelectionGrips[(j*4)+1].winfo_y()-_moveY) #bottom left
                        _SelectionGrips[(j*4)+2].place(x=_SelectionGrips[(j*4)+2].winfo_x()-_moveX) #top right
                        _SelectionGrips[(j*4)+3].place(x=_SelectionGrips[(j*4)+3].winfo_x()-_moveX, y=_SelectionGrips[(j*4)+3].winfo_y()-_moveY) #bottom right

                    #resize button
                    for j in range(len(_selected)):
                        _selected[j].place(width=_selected[j].winfo_width()-_moveX, height=_selected[j].winfo_height()-_moveY)


    def AddPrimaryResizeControls(control):
        global _SelectionGrips

        _Left=control.winfo_x()
        _Top=control.winfo_y()
        _Width=control.winfo_width()
        _Height=control.winfo_height()
        _Size=5

        #top left
        can=Canvas(designFormContainer)
        can.configure(background="blue",width=_Size,height=_Size,cursor="sizing")
        can.place(x=_Left-_Size,y=_Top-_Size)
        can.bind("<ButtonPress>", Resizer_MouseButtonPress)
        can.bind("<ButtonRelease>", Resizer_MouseButtonRelease)
        can.bind("<B1-Motion>", Resizer_MouseMove)
        _SelectionGrips.append(can)

        #bottom left
        can=Canvas(designFormContainer)
        can.configure(background="blue",width=_Size,height=_Size,cursor="sizing")
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left-_Size,y=_Top+_Height)
        can.bind("<ButtonPress>", Resizer_MouseButtonPress)
        can.bind("<ButtonRelease>", Resizer_MouseButtonRelease)
        can.bind("<B1-Motion>", Resizer_MouseMove)
        _SelectionGrips.append(can)

        #top right
        can=Canvas(designFormContainer)
        can.configure(background="blue",width=_Size,height=_Size,cursor="sizing")
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left+_Width,y=_Top-_Size)
        can.bind("<ButtonPress>", Resizer_MouseButtonPress)
        can.bind("<ButtonRelease>", Resizer_MouseButtonRelease)
        can.bind("<B1-Motion>", Resizer_MouseMove)
        _SelectionGrips.append(can)

        #bottom right
        can=Canvas(designFormContainer)
        can.configure(background="blue",width=_Size,height=_Size,cursor="sizing")
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left+_Width,y=_Top+_Height)
        can.bind("<ButtonPress>", Resizer_MouseButtonPress)
        can.bind("<ButtonRelease>", Resizer_MouseButtonRelease)
        can.bind("<B1-Motion>", Resizer_MouseMove)
        _SelectionGrips.append(can)

    def AddSecondaryResizeControls(control):
        _Left=control.winfo_x()
        _Top=control.winfo_y()
        _Width=control.winfo_width()
        _Height=control.winfo_height()
        _Size=5

        #top left
        can=Canvas(designFormContainer)
        can.configure(background="sky blue",width=_Size,height=_Size)
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left-_Size,y=_Top-_Size)
        _SelectionGrips.append(can)

        #bottom left
        can=Canvas(designFormContainer)
        can.configure(background="sky blue",width=_Size,height=_Size)
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left-_Size,y=_Top+_Height)
        _SelectionGrips.append(can)

        #top right
        can=Canvas(designFormContainer)
        can.configure(background="sky blue",width=_Size,height=_Size)
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left+_Width,y=_Top-_Size)
        _SelectionGrips.append(can)

        #bottom right
        can=Canvas(designFormContainer)
        can.configure(background="sky blue",width=_Size,height=_Size)
        can.addtag_withtag("Use","SelectionGrip")
        can.place(x=_Left+_Width,y=_Top+_Height)
        _SelectionGrips.append(can)

    def DrawControl():
        global _MouseStartingX
        global _MouseStartingY
        global _MouseEndingX
        global _MouseEndingY
        global _ToolSelected

        _left=_MouseStartingX
        _top=_MouseStartingY
        _width=_MouseEndingX-_MouseStartingX
        _height=_MouseEndingY-_MouseStartingY
        if _width<0: _width=_MouseStartingX-_MouseEndingX; _left=_MouseEndingX;
        if _height<0: _height=_MouseStartingY-_MouseEndingY; _top=_MouseEndingY;
        if _width<15: _width=60
        if _height<15: _height=30

        for group,tools in TB._Tools["Toolbar"].items():
            for tool,settings in tools.items():
                if TB._ToolSelected==tool:
                    _properties=settings["properties"]
                    break

        print("to do - create control by library.class")
        if TB._ToolSelected=="Button":
            control=Button(designFormContainer)
        elif TB._ToolSelected=="Label":
            control=Label(designFormContainer)
        elif TB._ToolSelected=="Entry":
            control=Entry(designFormContainer)
        elif TB._ToolSelected=="Frame":
            control=Frame(designFormContainer)
        elif TB._ToolSelected=="Canvas":
            control=Canvas(designFormContainer)


        _child=Child.Child()
        _child.Library=_properties["base"]["library"]["default"]
        _child.Class=TB._ToolSelected
        _child.Properties.update({"library": _properties["base"]["library"]["default"]})
        _child.Properties.update({"class": _properties["base"]["class"]["default"]})

        nametestloop=0
        nametest=_properties["base"]["name"]["default"]
        while WidgetNameAlreadyExists(nametest)==True:
            nametestloop+=1
            nametest=_properties["base"]["name"]["default"]+str(nametestloop)

        _child.Properties.update({"name": nametest})

        for attrib, details in _properties["attributes"].items():
            try:
                if "default" in details:
                    _child.Properties.update({attrib: details["default"]})
                    control.configure({attrib: details["default"]})
                else:
                    _child.Properties.update({attrib: ""})
            except Exception as ex:
                print("Unable to set property:")
                print(_child.Library+"."+_child.Class+"."+attrib)
                print(ex.args)



        #for i in range(len(_properties["attributes"])):
        #    try:
        #        if "default" in _properties["attributes"][i]:
        #            _child.Properties.update({_properties["attributes"][i]["name"]: _properties["attributes"][i]["default"]})
        #            control.configure({_properties["attributes"][i]["name"]: _properties["attributes"][i]["default"]})
        #        else:
        #            _child.Properties.update({_properties["attributes"][i]["name"]: ""})
        #    except Exception as ex:
        #        print("Unable to set property:")
        #        print(_child.Library+"."+_child.Class+"."+_properties["attributes"][i]["name"])
        #        print(ex.args)

        control.place(x=_left,y=_top,width=_width,height=_height)
        
        _child.Properties.update({"x": _left})
        _child.Properties.update({"y": _top})
        _child.Properties.update({"width": _width})
        _child.Properties.update({"height": _height})

        _child.Widget=control
        _form.Children.append(_child)
        control=None

    designFormContainer=Canvas(designForm)
    designFormContainer.place(y=30,height=_form.Properties["height"]-30,width=_form.Properties["width"])
    designFormContainer.bind("<ButtonPress>", designFormContainer_MouseButtonPress)
    designFormContainer.bind("<ButtonRelease>", designFormContainer_MouseButtonRelease)
    designFormContainer.bind("<B1-Motion>", designFormContainer_MouseMove)
    _designFrame=designFormContainer

    BuildTitleBar(designFormTitlebar)
    BuildControls(designFormContainer)

    return designFormContainer

def BuildTitleBar(parentFrame):
    global _form

    load = Image.open("Images\Icon.ico")
    render = ImageTk.PhotoImage(load)
    img = Label(parentFrame, image=render)
    img.image = render
    img.configure(background="blue2")
    img.place(x=5, y=5)

    lbl=Label(parentFrame)
    lbl.configure(fg="white",font="Arial 10 bold",background="blue2",text=_form.Properties["text"])
    lbl.place(x=26,y=5)

    btn=Button(parentFrame)
    btn.configure(text="-",width=30)
    btn.place(x=_form.Properties["width"]-95,y=0)

    btn=Button(parentFrame)
    btn.configure(text="M",width=30)
    btn.place(x=_form.Properties["width"]-65,y=0)

    btn=Button(parentFrame)
    btn.configure(text="X",width=30)
    btn.place(x=_form.Properties["width"]-35,y=0)

def BuildControls(parentFrame):
    global _form


    return

def WidgetNameAlreadyExists(name):
    for child in _form.Children:
        if name==child.Properties["name"]:
            return True

    return False