import pandas as pd
import time
from os import system, name

# define our clear function


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


while 1:
    clear()
    try:
        df = pd.read_csv("data.csv", index_col="학번")
    except:
        print("서버에서 초기파일 불러옵니다.")
        df = pd.read_csv(
            "https://raw.githack.com/han220/templatedata/master/data2U8.csv", index_col="학번")
    df.astype(str)

    honorcode = print("층장 관리 시스템은 한동 명예제도(Handong Honor Code)를 기반으로 운영됩니다.")
    try:
        number = int(input("학번을 입력하십시오 : "))
    except ValueError:
        print("잘못 입력하셨습니다. 다시 입력해주세요")
        time.sleep(1.5)
        continue

    if number == 99999999:
        print("[관리자 전용 파일]")
        # 확인 할 월일을 입력받는다
        input_number = input("학번 혹은 날짜를 입력하세요(학번: 0000000, 날짜: yymmdd): ")
        newList = []
        numdayList = ["학번", "날짜"]

        if len(input_number) == 8:
            ipryeok = numdayList[0]
        elif len(input_number) == 6:
            ipryeok = numdayList[1]
        else:
            print("다시 입력하세요.")

        df = pd.read_csv(
            "https://raw.githack.com/han220/templatedata/master/data2U8.csv", index_col="학번")
        df.astype(str)
        df.loc[:, ipryeok]

        manager = input("전체 항목을 원하시면 Enter를 누르세요")
        if manager == "":
            filt = df[check_month].isnull()
            df[filt].loc[:, ["성함", "성별", "RC", "호실"]].to_csv(
                r""+check_month+".csv")  # 모든 데이터 저장
        # 입력안된 사람만 출력

    else:
        try:
            student = df.loc[number]
            print("안녕하세요", student["성함"], "학우님 오늘 하루도 수고하셨습니다 :)")
            print(student["성함"], "님의 호실은", student["호실"], "입니다.")
            check = input("만약 본인의 정보와 맞으시면 \"1\" 을 틀리면 \"2\"번을 입력해주세요 : ")

            if check == "1":
                print("현재시각 : ", time.strftime(
                    "%m/%d %H:%M:%S", time.localtime(time.time())))

                df.loc[number, time.strftime("%m%d", time.localtime(
                    time.time()))] = time.strftime("%H:%M:%S", time.localtime(time.time()))

                df.to_csv(r"data.csv")  # 모든 데이터 저장
                input("엔터를 누르면 저장됩니다")
        except KeyError:
            print("잘못 입력하셨습니다. 다시 입력해주세요")
            time.sleep(1.5)
            continue
