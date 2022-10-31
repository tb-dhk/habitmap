import os
import json
import datetime as dt
import statistics
import calendar
from colors import color

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    dic = json.load(open(os.getcwd()+'/stats.json'))
    stepno = dic["stepno"]
except:
    stepno = 4

step_to4 = [ [0, 4], [0, 2, 4], [0, 1, 3, 4] ]
step_from4 = [ [0, 0, 1, 1, 1], [0, 1, 1, 2, 2], [0, 1, 2, 2, 3] ]
   
def newyear(json, habit, year):
    nmth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    lmth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    json[habit] = {
        str(year) : []
    }

    for x in range(12):
        json[habit][str(year)].append([])
        if int(year) % 4 == 0:
            for x in range(lmth[x]):
                json[habit][str(year)][-1].append(0)
        else:
            for x in range(nmth[x]):
                json[habit][str(year)][-1].append(0)
    print(f"    habit '{habit}' added.")

def add(json, habit):
    if habit == "stepno":
        print("    invalid name.")
    elif habit in json:
        print(f"    habit '{habit}' already exists.")
    else:
        tyr = dt.date.today().year
        newyear(json, habit, tyr)

def track(json, habit, day, ono):
    ono = int(ono)
    if habit in json and ono <= stepno and ono >= 0:
        date = ()
        tdy = dt.date.today()
        yst = dt.date.today() - dt.timedelta(days=1) 

        match day:
            case "tdy":
                date = (tdy.year, tdy.month, tdy.day)
            case "yst":
                date = (yst.year, yst.month, yst.day)
            case _:
                try:
                    dat = dt.date.fromisoformat(day)
                except:
                    print("    invalid day. the 'day' argument must either be 'tdy', 'yst', or a date in ISO format (YYYY-MM-DD).")
                    exit()
                else:
                    date = (dat.year, dat.month, dat.day)

        if str(date[0]) not in json[habit]:
            newyear(json, habit, date[0])
       
        if stepno != 4:
            no = step_to4[stepno-1][ono]
            json[habit][str(date[0])][date[1]-1][date[2]-1] = no
            print(f"    value of habit {habit} on {date[0]}-{date[1]}-{date[2]} changed to {ono} of {stepno} ({no} in 4-step).")
        else:
            json[habit][str(date[0])][date[1]-1][date[2]-1] = ono
            print(f"    value of habit {habit} on {date[0]}-{date[1]}-{date[2]} changed to {ono} of {stepno}.")
    elif habit not in json:
        print("    invalid habit.")
    elif ono > stepno or ono < 0:
        print("    invalid stepno.")

def daymap(begin, end, col, json):
    col = "#" + col
    tdy = dt.date.today()
    yst = dt.date.today() - dt.timedelta(days=1)
    
    match begin:
        case "tdy":
            st = tdy 
        case "yst":
            st = yst
        case _:
            try:
                st = dt.date.fromisoformat(begin)
            except:
                print("    invalid day. the 'day' argument must either be 'tdy', 'yst', or a date in ISO format (YYYY-MM-DD).")
                exit()

    match end:
        case "tdy":
            end = tdy 
        case "yst":
            end = yst
        case _:
            try:
                dat = dt.date.fromisoformat(end)
            except:
                print("    invalid day. the 'day' argument must either be 'tdy', 'yst', or a date in ISO format (YYYY-MM-DD).")
                exit()
            else:
                end = dt.date.fromisoformat(begin)
    
    max = 0
    lis = ["yy", "mm", "dd"]
    
    for habit in dic:
        if len(habit) > max:
            max = len(habit)
        lis.append(habit)
        
    lis.append("overall")
    
    nums = []
    if len(lis) <= 4:
        print("    you have no habits. please add a habit and try again.")
        exit()

    for habit in lis:
        if habit != "stepno":
            if habit == "overall":
                string = "overall"
                while len(string) < max + 4:
                    string = " " + string
                string += " "
                num = round(statistics.mean(nums))
                match num:
                    case 0:
                        string += color("  ", col)
                    case 1:
                        string += color("░░", col)
                    case 2:
                        string += color("▒▒", col)
                    case 3:
                        string += color("▓▓", col)
                    case 4:
                        string += color("██", col)
                print(string)
            elif habit in ["yy", "mm", "dd"]:
                start = st
                string = habit
                while len(string) < max + 4:
                    string = " " + string
                string += " "
                while start <= end:
                    date = (start.year, start.month, start.day)
                    match habit:
                        case "yy":
                            if (start.month == 1 and start.day == 1) or start == st:
                                if start.year < 10:
                                    string += "0" + str(start.year)
                                else:
                                    string += str(start.year)[-2:]
                            else:
                                string += "  "
                        case "mm":
                            if start.day == 1 or start == st:
                                if start.month < 10:
                                    string += "0" + str(start.month)
                                else:
                                    string += str(start.month)
                            else:
                                string += "  "
                        case "dd":
                            if start.day == 1:
                                string += "01"
                            elif start.day == 5:
                                string += "05"
                            elif start.day == 30 and calendar.monthrange(start.year, start.month)[1] == 30:
                                string += "  "
                            elif start.day % 5 == 0:
                                string += str(start.day)
                            else:
                                string += "  "
                    start += dt.timedelta(days=1)  
                print(string)
            else:
                start = st
                string = "    " + habit
                while len(string) < max + 4:
                    string = " " + string
                string += " "
                while start <= end:
                    date = (start.year, start.month, start.day)
                    if date[0] not in dic[habit]:
                        newyear(json, habit, date[0])
                        print(json[habit])
                    num = dic[habit][str(date[0])][date[1]-1][date[2]-1]
                    nums.append(num)
                    match num:
                        case 0:
                            string += color("  ", col)
                        case 1:
                            string += color("░░", col)
                        case 2:
                            string += color("▒▒", col)
                        case 3:
                            string += color("▓▓", col)
                        case 4:
                            string += color("██", col)
                    start += dt.timedelta(days=1) 
                print(string)
    

def yearmap(habit, year, col):
    col = "#" + col
    stat = dic[habit][str(year)]
    yearindow = [[], [], [], [], [], [], []]
    strings = []
    months = [0]
    weekcount = 0
    def twkd(date):
        if date.weekday() == 6:
            return 0
        else:
            return date.weekday() + 1
    for x in range(twkd(dt.date(dt.date.today().year,1,1))):
        yearindow[x].append(0)
    for x in range(12):
        for y in range(len(stat[x])):
            yearindow[twkd(dt.date(dt.date.today().year,x+1,y+1))].append(int(stat[x][y]))
            if twkd(dt.date(dt.date.today().year,x+1,y+1)) == 6:
                weekcount += 1
        months.append(weekcount)

    months = months[:-1]
    monstr = "        "
    for x in range(len(months)):
        while len(monstr) < months[x] * 2 + 8:
            monstr = monstr + ("  ")
        if x+1 < 10:
            monstr = monstr + ("0" + str(x+1))
        else:
            monstr = monstr + (str(x+1))
    strings.append(monstr)

    for x in range(len(yearindow)):
        days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        string = "    " + days[x] + " "
        for y in yearindow[x]:
            try:
                int(y) 
            except:
                string += color("  ", col)
            else:
                match y:
                    case 0:
                        string += color("  ", col)
                    case 1:
                        string += color("░░", col)
                    case 2:
                        string += color("▒▒", col)
                    case 3:
                        string += color("▓▓", col)
                    case 4:
                        string += color("██", col)
        strings.append(string)
    for x in strings:
        print(x)
    print("")
