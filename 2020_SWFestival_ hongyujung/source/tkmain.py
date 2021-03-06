from tkinter import *
from tkinter import font, messagebox, END
import pandas as pd
import math

from module.tkadmin import TkAdmin

# import random
import time

root = Tk()
# root.configure(bg="white")
root.title("무인점호 시스템")
root.configure(bg="white")

iconImg = Image("photo", file="icon.gif")
# root.tk.call("wm", "iconphoto", root._w, iconImg)

root.iconphoto(True, iconImg)
# root.iconphoto(False, PhotoImage(file="icon.gif"))
# root.geometry("1280x720")

root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen', True)

# Define Function


def update_clock():
    timeLabel.configure(text="현재시각 : " + time.strftime(
        "%m/%d %H:%M:%S", time.localtime(time.time())))
    # single_anzeige = random.random()*100
    # timeLabel.config(text=single_anzeige)
    # timeLabel.config(text="Hello World")

    # 공지 파일 불러오기
    try:
        announcement = open("announcement.txt", "r").readlines()
        announcementLabel.configure(
            text=announcement[0], font=font.Font(size=18), pady=30)
    except:
        pass

    timeLabel.after(1000, update_clock)


clearLastInfoTimer = -1


def clearLastInfo():
    global clearLastInfoTimer
    if(clearLastInfoTimer == 0):
        try:
            clearLastInfoFrame.pack_forget()
        except NameError:
            pass
    if clearLastInfoTimer > -1:
        clearLastInfoTimer -= 1
    root.after(1000, clearLastInfo)


clearLastInfo()


def run_tasks(*args):
    global clearLastInfoFrame
    global clearLastInfoTimer
    # 데이터 불러오기
    try:
        df = pd.read_csv("data.csv", index_col="학번")
    except:
        print("서버에서 초기파일 불러옵니다.")
        df = pd.read_csv(
            "http://raw.githack.com/han220/templatedata/master/data2U8.csv", index_col="학번")
    df.astype(str)

    admin = TkAdmin(df)

    # 입력된 학번을 숫자로 바꿔준다.
    try:
        number = int(hakbunEntry.get())
    except ValueError:
        messagebox.showwarning("", "잘못 입력하셨습니다. 다시 입력해주세요")
        hakbunEntry.delete(0, END)
        return

    # 입력된 학번을 학생 객체로 바꿔준다.
    try:
        if(number == 99999999):
            print("Admin Screen Requested")
            admin.openAdminWindow()
            return
        student = df.loc[number]
        datecode = time.strftime("%m%d", time.localtime(
            time.time()))

        # 기존 정보 초기화
        clearLastInfoTimer = 0
        clearLastInfo()

        check = messagebox.askyesno(
            "본인정보 확인", "이름: " + student["성함"]+"\n학번: " + str(number) + "\n방번호: " + str(student["호실"]))

        # Check 가 yes 가 아닐경우 실행취소
        if(check != 1):
            hakbunEntry.delete(0, END)
            return

        # 이미 점호가 된 상황인지 확인
        if(datecode in df and not pd.isnull(student[datecode])):
            messagebox.showwarning(
                "이미 점호처리 되었습니다.", "점호시간: " + student[datecode])
            hakbunEntry.delete(0, END)
            return

        clearLastInfoFrame = Frame(home, bg="white")
        Label(clearLastInfoFrame, text="점호 완료 되셨습니다.",
              fg="blue", bg="white").pack()
        Label(clearLastInfoFrame,
              text=student["성함"] + "학우님 오늘 하루도 수고하셨습니다. :)", fg="blue", bg="white").pack()
        clearLastInfoFrame.pack()

        clearLastInfoTimer = 5
        hakbunEntry.delete(0, END)

        df.loc[number, datecode] = time.strftime(
            "%H:%M:%S", time.localtime(time.time()))

        df.to_csv(r"data.csv")  # 모든 데이터 저장
    except KeyError:
        messagebox.showwarning("", "잘못 입력하셨습니다. 다시 입력해주세요")
        hakbunEntry.delete(0, END)


home = Frame(root, bg="white")

announcementLabel = Label(root, text="", bg="white")
announcementLabel.pack()

titleLabel = Label(home, text="무인 점호기", font=font.Font(
    size=48, weight="bold"), bg="white")

hakbunUserIn = Frame(home, bg="white")

hakbunLabel = Label(
    hakbunUserIn, text="학번 : ", font=font.Font(size=20, weight="bold"), bg="white")
hakbunEntry = Entry(hakbunUserIn, justify='center')
nextButton = Button(hakbunUserIn, text="조회", command=run_tasks)

# Entry 입력할때 <Return> 입력시 조회
hakbunEntry.bind("<Return>", run_tasks)

titleLabel.pack()
hakbunLabel.pack(side="left")

# Pack 시작

hakbunEntry.pack(side="left")
nextButton.pack(side="right")

hakbunUserIn.pack(pady=10)
home.pack(expand=True, anchor="s")

# 아너코드 추가
honorCodeFrame = Frame(root, bg="white")

honorCodeContentFrame = Frame(
    honorCodeFrame, borderwidth=3, relief="ridge", padx=5, pady=5, bg="white")

honorCodeTitleLabel = Label(honorCodeContentFrame, text="한동 명예제도 (Handong Honor Code)",
                            font=font.Font(size=15, weight="bold"), bg="white")
honorCodeLabel = Label(honorCodeContentFrame, text="1. 한동인은 모든 말과 글과 행동에 책임을 집니다.\n1. 한동인은 학업과 생활에서 정직하고 성실합니다.\n1. 한동인은 다른 사람을 돕고 겸손히 섬깁니다.\n1. 한동인은 다른 사람을 위해 자신을 희생합니다.\n1. 한동인은 모든 구성원의 인격과 권리를 존중합니다.\n1. 한동인은 학교의 재산과 다른 사람의 재산을 소중히 여깁니다.",
                       font=font.Font(size=15), bg="white")

honorCodeTitleLabel.pack()
honorCodeLabel.pack()

honorCodeContentFrame.pack()

honorCodeFrame.pack(expand=True)

timeLabel = Label(root, text="", bg="white")
timeLabel.pack()
# 1초마다 시간 갱신
update_clock()

root.mainloop()
