import datetime
from colors import color

def heatmap(stat):
    print("    # calendar heatmap\n")
    yearindow = [[], [], [], [], [], [], []]
    strings = []
    months = [0]
    max = 0
    weekcount = 0
    def twkd(date):
        if date.weekday() == 6:
            return 0
        else:
            return date.weekday() + 1
    for x in range(twkd(datetime.date(datetime.date.today().year,1,1))):
        yearindow[x].append(0)
    for x in range(12):
        for y in range(len(stat[x+1])):
            yearindow[twkd(datetime.date(datetime.date.today().year,x+1,y+1))].append(int(stat[x+1][y]))
            if twkd(datetime.date(datetime.date.today().year,x+1,y+1)) == 6:
                weekcount += 1
            if int(stat[x+1][y]) > max:
                max = int(stat[x+1][y])
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
                data = round((y/max)*4)/4
            except:
                string = string + color("  ", "blue")
            else:
                match data:
                    case 0:
                        string = string + color("  ", "blue")
                    case 0.25:
                        string = string + color("░░", "blue")
                    case 0.5:
                        string = string + color("▒▒", "blue")
                    case 0.75:
                        string = string + color("▓▓", "blue")
                    case 1:
                        string = string + color("██", "blue")
        strings.append(string)
    for x in strings:
        print(x)
    print("")
