from blog.models import *

def checkCL(baseid,classid):
    base = Base.objects.get(id = baseid)
    if (base.classes_set.all()):
        classes=base.classes_set.all()
        for tarclass in classes:
            if tarclass.id == classid:
                return True,tarclass
    else:
        return False,None

def checkStudent(classid,studentid):
    try:
        student = Students.objects.get(id = studentid)
        cl = Classes.objects.get(id = classid)
        sts = cl.students.all()
        for st in sts:
            if(st == student):
                return cl,student
        return None,None
    except:
        return None,None

def tagsstate(tarclass,teacher):
    lst = []
    if  Tags.objects.filter(tarclass = tarclass).exists():
        tags = Tags.objects.filter(tarclass = tarclass)
        for tag in tags :
            if Tasks.objects.filter(auther = teacher,tarclass = tarclass,tag = tag).exists():
                t=0
                f=0
                tasks = Tasks.objects.filter(auther = teacher,tarclass = tarclass,tag = tag)
                for task in tasks: 
                    if StudentTasks.objects.filter(task = task).exists():
                        stts = StudentTasks.objects.filter(task = task)
                        for stt in stts:
                            if stt.finish :
                                if stt.result :
                                    t += 1
                                else:
                                    f += 1
                data = {"tag":tag,"true":t,"false":f,"all":t+f}
                lst.append(data)
            else:
                data = {"tag":tag,"true":0,"false":0,"all":0}
                lst.append(data)
    return lst

