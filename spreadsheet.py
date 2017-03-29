import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("shokuiki").sheet1
def vs():
    team1=sheet.acell('B3').value
    team2=sheet.acell('B14').value
    team3=sheet.acell('B25').value
    team4=sheet.acell('B36').value

    sheet.update_acell('C3','vs {}'.format(team4))
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
        winnum=0
        winperson=0
        wg=[]
        wg.append(sheet.acell('C{}'.format(12+i*11)).value)
        wg.append(sheet.acell('D{}'.format(12+i*11)).value)
        wg.append(sheet.acell('E{}'.format(12+i*11)).value)

        for j in range(8):
            wg.append(sheet.acell('F{}'.format(4+j+i*11)).value)

        for k in range(3):
            if int(wg[k])>2:
                winnum+=1
        for k in range(8):
            if int(wg[3+k])==3:
                winperson+=1
        sheet.update_acell('I{}'.format(3+i*11),winnum)
        sheet.update_acell('I{}'.format(5+i*11),winperson)

def ranking():
    cpcells=[(3,9),(4,9),(5,9),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6)]
    cpnum=0
    flag=True
    while flag:
        cpvalue=[]

        for i in range(4):
            cpvalue.append(int(sheet.cell(cpcells[cpnum+i*11][0],cpcells[cpnum][1]).value))
        cpmax=max(cpvalue)
        winteam=[i for i,j in enumerate(cpvalue) if j == cpmax]
        if len(winteam)==1:
            sheet.acell('B{}'.format(3+winteam[0]*11)).value
            flag=False
        elif cpnum==10:
            print('引き分け')
            flag=False
        else:
            cpnum+=1



# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

#vs()
#calc()