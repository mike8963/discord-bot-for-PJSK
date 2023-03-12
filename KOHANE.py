import discord
from discord.ext import commands
import matplotlib
from gsheet import GoogleSheets
from main import GoogleAPIClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

__TOKEN__ = " Here put my BOT TOKEN "

# command_prefix 是你希望打指令前加的前綴
bot = commands.Bot(command_prefix="/")
'''
@bot.command()
async def 指令(ctx):
    
    result = "<舊倍率>"
    await ctx.send(result)
    result = "/舊倍率 p1 p2 p3 p4 p5"
    await ctx.send(result)
    result = "倍率"
    await ctx.send(result)
    result = "/倍率 p1 p2 p3 p4 p5"
    await ctx.send(result)
'''   

# /舊倍率 110 110 110 110 110
@bot.command()
async def 舊倍率(ctx, m1, m2, m3, m4, m5):
    # 計算技能倍率
    m1 = 1 + float(m1) / 100
    m2 = 1 + float(m2) / 500
    m3 = 1 + float(m3) / 500
    m4 = 1 + float(m4) / 500
    m5 = 1 + float(m5) / 500
    ans = m1 * m2 * m3 * m4 * m5
    result = ('%.2f'%ans)
    await ctx.send(result)

@bot.command()
async def 倍率(ctx, m1, m2, m3, m4, m5):
    # 計算技能倍率
    m1 = float(m1) / 100
    m2 = float(m2) / 500
    m3 = float(m3) / 500
    m4 = float(m4) / 500
    m5 = float(m5) / 500
    ans = 1 + m1 + m2 + m3 + m4 + m5
    result = ('%.2f'%ans)
    await ctx.send(result)

@bot.command()
async def img(ctx, sheetname):
    myWorksheet = GoogleSheets()
    # range看要讀哪個部分
    data, date = myWorksheet.getWorkSheet(
        spreadsheetId=' 這邊放上班表的ID ',
        range = sheetname
    )
    # 圖片設置 第一行是因為matplotlib本身沒有中文字 所以有調字型 
    # 調的方式 https://pyecontech.com/2020/03/27/python_matplotlib_chinese/
    # 其他部分還沒調好 主要是圖片解析度跟字體大小
    
    # index更換成各時段(ex. 0-1)
    data.index = data['']
    del data['']
    #print(data)

    # 更改預設字體
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    plt.figure()
    ax = plt.axes(frame_on = False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    pd.plotting.table(ax, data, loc='center')
    plt.savefig('table.png', dpi=300)
    # 這邊我是先存到本地 再上傳圖片到DC 應該可以直接傳
    img = discord.File('C:\\Users\\mike8\\Desktop\\code\\side\\pjsk\\pjsk_bot\\table.png')
    await ctx.send(file = img)


# prefix + 班表查詢 + 查詢名稱
# ex. /班表查詢 AZ
# 可設定的有car總數
@bot.command()
async def 班表查詢(ctx, username):

    #  car_num: 車總數
    car_num = 5

    # check the user is on car or not 
    onCar = False

    for i in range(car_num):
        # get googlesheet and turn into pandas.Dataframe
        myWorksheet = GoogleSheets()
        data = myWorksheet.getWorkSheet(
            spreadsheetId=' 這邊放上班表的ID ',
            range=str(f"'car{i + 1}'")
        )
        data.index = data['']
        del data['']


        if not data.loc[data['P1'].str.contains(username) | data['P2'].str.contains(username) | data['P3'].str.contains(username) | data['P4'].str.contains(username) | data['P5'].str.contains(username)].empty:

            await ctx.send(f'[car {i+1}]')
            await ctx.send(data.loc[data['P1'].str.contains(username) | 
                                    data['P2'].str.contains(username) |
                                    data['P3'].str.contains(username) |
                                    data['P4'].str.contains(username) |
                                    data['P5'].str.contains(username)])
            onCar = True

    if onCar == False:
        myWorksheet = GoogleSheets()
        data = myWorksheet.getWorkSheet(
            spreadsheetId=' 這邊放上班表的ID ',
            range=str("候补")
        )
        print(data)



bot.run(__TOKEN__)

