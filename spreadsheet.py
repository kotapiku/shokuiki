import gspread
from oauth2client.service_account import ServiceAccountCredentials

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


def ranking():
    teamcells = ['B3', 'B14', 'B25', 'B36']
    teams = [sheet.acell(teamcells[i]).value for i in range(4)]

    cpcells = [(3, 9), (4, 9), (5, 9), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6)]
    cpnum = 0
    flag = True
    answer = []
    tms = [0, 1, 2, 3]
    while flag:
        cpvalue = []
        for i in tms:
            cpvalue.append(int(sheet.cell(cpcells[cpnum][0] + i * 11, cpcells[cpnum][1]).value))
        cpval_2 = list(zip(tms, cpvalue))

        cpvalue.sort(reverse=True)

        while cpvalue:
            if (len(cpvalue) == 1) or (cpvalue[0] != cpvalue[1]):
                for cpv in cpval_2:
                    if cpv[1] == cpvalue[0]:
                        answer.append(teams[cpv[0]])
                        tms.remove(cpv[0])
                del cpvalue[0]

            else:
                cpvalue = []

        if len(answer) == 4 or cpnum == 10:
            flag = False

        else:
            cpnum += 1

    print(answer)

# vs()
# calc()
# ranking()
