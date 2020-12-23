from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 
from students.tools import * 

#デバッグ用の関数
def test(request,id):
    """task画面"""
    student,num = check(request)
    if num != 2:
        return redirect('home')
    if(id == 1):
       test1(student)
    return redirect('home')

"""
getMyClassHomework()の使い方
返り値は辞書型
classには出されたクラスのインスタンス(※1)が
homeworksにはclassに入ったクラスから出された宿題のインスタンスのリスト(※2)が
入っている
"""

#getMyClassHomeworkのデバッグ
def test1(student):
    datas = student.getMyClassHomework()
    print("=========================")
    for data in datas:
        thisclass = data["class"] #(※1)
        print("class:",thisclass.class_name)
        print("#########################")
        homeworks = data["homeworks"] #(※2)
        print("homeworks:")
        if(homeworks == []):
            print("Not have")
            print("=========================")
            continue
        for i in range(len(homeworks)):
            print(i+1,".",homeworks[i].task.all()[0].name)

        print("=========================")
