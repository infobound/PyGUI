from tkinter import *
from tkinter import filedialog as fd
import json
import Form
import Child

global _form
global _designFrame

def Init(form,frame):
    global _form
    global _designFrame

    _form=form
    _designFrame=frame

def SaveForm():
    global _form

    try:
        _json='{ "Form": { '
        _json+='"Properties": '
        _json+=json.dumps(_form.Properties)
        _json+=' ,'
        _json+='"Children": ['
        for child in _form.Children:
            _json+='{ "library": "'+child.Library+'",'
            _json+='"class": "'+child.Class+'",'
            _json+='"Properties":'
            _json+=json.dumps(child.Properties)
            _json+='},'

        _json=_json[:-1]
        _json+=' ]'


        _json+=' }'
        _json+=' }'

        file="Saves\\"+_form.Properties["name"]+".json"
        f = open(file, "w")
        f.write(_json)
        f.close()
    except Exception as ex:
        print("Saved Failed")
        print(ex)


def LoadForm():
    global _form
    global _designFrame

    filetypes = (
        ('Form files', '*.json'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='Saves\\',
        filetypes=filetypes)

    try:
        file = open(filename, "r")
        data=file.read()
        file.close()
    except Exception as e:
        print(e)
        return

    try:
        _data=json.loads(data)
    except Exception as e:
        print(e)
        return

    _form=None
    _form=Form.Form()
    for child in _designFrame.winfo_children():
        child.destroy()

    _form.Properties=_data["Form"]["Properties"]

    for dataChild in _data["Form"]["Children"]:
        formChild=Child.Child()
        formChild.Library=dataChild["library"]
        formChild.Class=dataChild["class"]
        formChild.Properties=dataChild["Properties"]
        if "Children" in dataChild: formChild.Children=dataChild["Children"]
        _form.Children.append(formChild)
        LoadControl(formChild)
        formChild=None

    return _form

def LoadControl(_child):
    global _designFrame
    global _form

    print("to do - create control by library.class")
    if _child.Class=="Button":
        control=Button(_designFrame)
    elif _child.Class=="Label":
        control=Label(_designFrame)
    elif _child.Class=="Entry":
        control=Entry(_designFrame)
    elif _child.Class=="Frame":
        control=Frame(_designFrame)
    elif _child.Class=="Canvas":
        control=Canvas(_designFrame)

    for key,val in _child.Properties.items():
        if key!="x" and key!="y" and key!="width" and key!="height" and key!="name" and key!="library" and key!="class" and val!="":
            control.configure({key:val})

    _geo=[]
    for key,val in _child.Properties.items():
        if key=="x" or key=="y" or key=="width" or key=="height":
            _geo.append({key:val})

    control.place(_geo)
    _child.Widget=control

def LoadProperties():
    #the code to get properties from the toolbar class has become ugly.  This is the start
    #of refactoring those properties into a more conscise class

    try:
        file = open("Data\\form.json", "r")
        data=file.read()
        file.close()
    except Exception as e:
        print(e)
        return

    try:
        _data=json.loads(data)
    except Exception as e:
        print(e)
        return

    return _data

def LoadFile(FilePath):
    try:
        file = open(FilePath, "r")
        rawdata=file.read()
        file.close()
    except Exception as e:
        print(e)
        return

    try:
        formatteddata=json.loads(rawdata)
    except Exception as e:
        print(e)
        return

    return formatteddata
