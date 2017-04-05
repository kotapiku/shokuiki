import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("shokuiki").sheet1


def vs():
    team1 = sheet.acell('B3').value
    team2 = sheet.acell('B14').value
    team3 = sheet.acell('B25').value
    team4 = sheet.acell('B36').value

    sheet.update_acell('C3', 'vs {}'.format(team4))
    sheet.update_acell('D3', 'vs {}'.format(team3))
    sheet.update_acell('E3', 'vs {}'.format(team2))
    sheet.update_acell('C14', 'vs {}'.format(team3))
    sheet.update_acell('D14', 'vs {}'.format(team4))
    sheet.update_acell('E14', 'vs {}'.format(team1))
    sheet.update_acell('C25', 'vs {}'.format(team2))
    sheet.update_acell('D25', 'vs {}'.format(team1))
    sheet.update_acell('E25', 'vs {}'.format(team4))
    sheet.update_acell('C36', 'vs {}'.format(team1))
    sheet.update_acell('D36', 'vs {}'.format(team2))
    sheet.update_acell('E36', 'vs {}'.format(team3))


def calc():
    for i in range(4):
        winnum = 0
        winperson = 0
        wg = []
        wg.append(sheet.acell('C{}'.format(12 + i * 11)).value)
        wg.append(sheet.acell('D{}'.format(12 + i * 11)).value)
        wg.append(sheet.acell('E{}'.format(12 + i * 11)).value)

        for j in range(8):
            wg.append(sheet.acell('F{}'.format(4 + j + i * 11)).value)

        for k in range(3):
            if int(wg[k]) > 2:
                winnum += 1
        for k in range(8):
            if int(wg[3 + k]) == 3:
                winperson += 1
        sheet.update_acell('I{}'.format(3 + i * 11), winnum)
        sheet.update_acell('I{}'.format(5 + i * 11), winperson)


def getvalues():
    katiten = [int(sheet.cell(3 + 11 * i, 9).value) for i in range(4)]
    katisu = [int(sheet.cell(4 + 11 * i, 9).value) for i in range(4)]
    zensho = [int(sheet.cell(5 + 11 * i, 9).value) for i in range(4)]
    hachi = [[int(sheet.cell(4 + i * 11 + j, 6).value) for i in range(4)] for j in range(8)]

    return katiten, katisu, zensho, hachi


def ranking(cpcells):
    # teams = [sheet.cell(3 + i * 11, 2).value for i in range(4)]

    cpnum = 0
    flag = True
    answer = []
    tms = [0, 1, 2, 3]

    while flag:
        cpvalue = []
        for i in tms:
            cpvalue.append(cpcells[cpnum][i])
        cpval_2 = list(zip(tms, cpvalue))

        cpvalue.sort(reverse=True)

        while cpvalue:
            if (len(cpvalue) == 1) or (cpvalue[0] != cpvalue[1]):
                for cpv in cpval_2:
                    if cpv[1] == cpvalue[0]:
                        answer.append(cpv[0])
                        tms.remove(cpv[0])
                del cpvalue[0]

            else:
                cpvalue = []

        if len(answer) == 4:
            flag = False
            return answer

        elif cpnum == len(cpcells) - 1:
            flag = False
            return [5, 5, 5, 5]

        else:
            cpnum += 1


def minreq1(teamlist, cdnum):
    # teamlist=[todainum,vs_todainum,other1,other2] ( 0,1,2,3　
    # cdnum = 1 or 2 ( 1位の条件 or 2位の条件 )
    todai = 0
    flag = True
    katiten = [int(sheet.cell(3 + 11 * i, 9).value) for i in range(4)]
    katisu = [int(sheet.cell(4 + 11 * i, 9).value) for i in range(4)]

    while flag:
        flag1 = True
        katiten1 = copy.deepcopy(katiten)
        katisu1 = copy.deepcopy(katisu)

        katisu1[teamlist[0]] += todai
        katisu1[teamlist[1]] += 5 - todai
        if todai < 3:
            katiten1[teamlist[1]] += 1
        else:
            katiten1[teamlist[0]] += 1

        for i in range(6):
            katisu1[teamlist[2]] += i
            katisu1[teamlist[3]] += 5 - i
            if i < 3:
                katiten1[teamlist[3]] += 1
            else:
                katiten1[teamlist[2]] += 1
            answer = ranking([katiten1, katisu1])
            if cdnum == 1:
                if answer[0] != teamlist[0]:
                    flag1 = False
            if cdnum == 2:
                if answer[1] != teamlist[0] and answer[0] != teamlist[0]:
                    flag1 = False
        if flag1:
            flag = False
            print('必要な勝ち数は{}です'.format(todai))
        elif todai == 5:
            flag = False
            print('クリアする最低条件はありません')
        else:
            todai += 1


# vs()
# calc()
'''
 katiten, katisu, zensho, hachi = getvalues()
 comparevalues=[katiten,katisu,zensho]
 for i in range(8):
    comparevalues.append(hachi[i])
 ranking(comparevalues)
'''

# minreq1([1, 0, 2, 3], 2)
