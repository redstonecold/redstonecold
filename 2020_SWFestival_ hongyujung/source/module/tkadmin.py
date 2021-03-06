# 어드민 화면 구축

from tkinter import *
from tkinter import messagebox, filedialog
from pandastable import Table, TableModel
import pandas as pd
import sys


class TkAdmin:
    def __init__(self, df):
        self.df = df

    # 파일로 내보내기
    def save(self):
        input_number = self.enterNumber.get()
        df = self.table.model.df
        print(df.head())
        filename = filedialog.asksaveasfilename(
            initialfile=input_number, initialdir="/", title="파일 저장", filetypes=(("CSV 파일", "*.csv"),))
        if(filename != ""):
            df.to_csv(r""+filename+".csv", index=False)  # 모든 데이터 저장

    # 학번/날짜 통합 검색
    def search(self, *args):
        df = self.df
        input_number = self.enterNumber.get()
        print("Searched ", input_number)

        # int_number = int(input_number)
        # newList = []
        # numdayList = ["학번", "날짜"]

        if len(input_number) == 8:
            self.errorMsg.configure(text="")

            try:
                new_df2 = df.loc[int(input_number)].to_frame().reset_index()

                self.table.updateModel(TableModel(new_df2))
                self.table.redraw()
                print(new_df2)
            except KeyError:
                self.errorMsg.configure(text="존재하지 않는 학번입니다.")
            # self.table.data.TableModel(dataframe=new_df2)
            # self.table.model.df = new_df2
#             addSheet(sheetname=None, df=None, meta=None, select=False)
# Add a sheet with new or existing data

            # print(new_df2)
        elif len(input_number) == 4:
            self.errorMsg.configure(text="")
            try:
                new_df2 = df.loc[:, ["성함", "성별",
                                     "RC", input_number]].reset_index()
                self.table.updateModel(TableModel(new_df2))
                self.table.redraw()
                print(new_df2)
            except KeyError:
                self.errorMsg.configure(text="해당 날짜를 찾을 수 없습니다.")
        elif len(input_number) == 3:
            self.errorMsg.configure(text="")
            filt = (df["호실"] == int(input_number))
            new_df2 = df.loc[filt].reset_index()
            self.table.updateModel(TableModel(new_df2))
            self.table.redraw()
            print(new_df2)
        else:
            self.errorMsg.configure(text="잘못 입력하셨습니다.")

    def openAdminWindow(self):
        df = self.df

        top = Toplevel()
        top.title("관리자 페이지")
        top.geometry("1280x720")

        leftG = Frame(top, width=1000)
        leftF = Frame(leftG, borderwidth=3,
                      relief="ridge", padx=50, pady=10)

        #    | LEFT SEARCH PORTION |    #

        self.errorMsg = Label(leftF, text="", fg="red")
        self.errorMsg.pack()
        Label(leftF, text="학번, 날짜, 호수 중 하나를 입력하세요").pack()
        Label(leftF, text="(학번: 00000000, 날짜: mmdd, 호수: 000)").pack()

        self.enterNumber = Entry(leftF)
        self.enterNumber.pack()
        self.enterNumber.bind("<Return>", self.search)

        enterButton = Button(leftF, text="조회", command=self.search)
        enterButton.pack()

        leftF.pack(expand=True)

        Button(leftG, text="데이터 저장", command=self.save).pack(
            fill=BOTH, expand=True)
        Button(leftG, text="프로그램 종료", command=sys.exit).pack(
            fill=BOTH, expand=True)
        Button(leftG, text="닫기", command=top.destroy).pack(
            fill=BOTH, expand=True)

        # leftG.place(x=0, y=0, anchor="nw", width=450, height=720)
        leftG.grid(row=0, column=0)

        #    | RIGHT RESPONSE PORTION |    #
        rightG = Frame(top, borderwidth=3,
                       relief="ridge", padx=5, pady=5)
        rightF = Frame(rightG)

        self.table = pt = Table(rightF, dataframe=df.reset_index(),
                                showstatusbar=True, height=720, width=830)
        pt.show()

        # Welcome Page
        rightF.pack(expand=True)
        rightG.grid(row=0, column=1)

        # top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)


def main():
    print("Started")
    try:
        df = pd.read_csv("data.csv", index_col="학번")
    except:
        print("서버에서 초기파일 불러옵니다.")
        df = pd.read_csv(
            "https://raw.githack.com/han220/templatedata/master/data2U8.csv", index_col="학번")
    df.astype(str)
    root = Tk()
    tkadmin = TkAdmin(df)
    tkadmin.openAdminWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
