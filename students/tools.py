from blog.models import *

def checkCL(baseid,classid):
    base = Base.objects.get(id = baseid)
    if (base.classes_set.all()):
        classes = base.classes_set.all()
        for tarclass in classes:
            if tarclass.id == classid:
                return True,tarclass
    else:
        return False,None

def gettask(Stask):
    return Stask.task.get()

