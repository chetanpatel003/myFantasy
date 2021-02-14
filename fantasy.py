import requests
import bs4

def calculate(data ,is_batsman):
    points = 0

    # Batting points
    runs_scored = int(data[0])
    points += runs_scored

    if runs_scored >= 100:
        points += 16

    elif runs_scored >= 50 and runs_scored < 100:
        points += 8

    balls_played = int(data[1])

    fours = int(data[2])
    points += fours

    sixes = int(data[3])
    points += 2*sixes


    strike_rate = float(data[4])
    if balls_played > 10 and is_batsman:
        if strike_rate < 50:
            points -= 6
        elif strike_rate > 50 and strike_rate < 60:
            points -= 4
        elif strike_rate > 60 and strike_rate < 70:
            points -= 2

    # Bowling points    
    overs = float(data[5])

    maidens = int(data[6])
    points += maidens*8

    wickets = int(data[8])
    points += wickets*25

    if wickets == 4:
        points += 8

    elif wickets == 5:
        points += 16

    economy = float(data[11])
    if overs >= 2:
        if economy <= 4:
            points += 6
        elif economy > 4 and economy <= 5:
            points += 4
        elif economy > 5 and economy <= 6:
            points += 2
        elif economy > 9 and economy <= 10:
            points -= 2
        elif economy > 10 and economy <= 11:
            points -= 4
        elif economy >= 11:
            points -= 6

    # Feilding points

    catch = int(data[12])
    points += catch*8

    run_out = int(data[13])
    points += run_out*6

    stumping = int(data[14])
    points += stumping*12

    if points < 0:
        points = 0
    return points


url = 'https://www.cricbuzz.com/live-cricket-scorecard/30545/aus-vs-ind-3rd-t20i-india-tour-of-australia-2020-21'

res = requests.get(url)
bs = bs4.BeautifulSoup(res.text,'html.parser')

teams = bs.find_all('div', class_="cb-col cb-col-100 cb-minfo-tm-nm")
for i in range(len(teams)):
    data = teams[i].getText()
    if i == 1:
        team_1 = data
    if i == 3:
        team_2 = data


team_1 = team_1.split('  ')[1].split(', ')
team_2 = team_2.split('  ')[1].split(', ')
team = []
for i in range(11):
    team.append(team_1[i])
    team.append(team_2[i])

stats = bs.find_all('div', class_="cb-col cb-col-100 cb-scrd-itms")
l = []
for i in stats:
    data = i.getText()
    if data[:3] == '   ':
        l.append(data.strip())

batting_stats = []
bowling_stats = []
for i in l:
    if len(i.split('    ')) == 2:
        batting_stats.append(i)
    else:
        bowling_stats.append(i)

wickets = []
new_batting_stats = []
for batsman in batting_stats:
    splits = batsman.split('    ')
    name = [(splits[0].strip()).split(' ')[0]]
    wickets.append((splits[1].split('  ')[0]).strip())
    score = (splits[1].split('  ')[1]).strip()
    name.extend(score.split(' '))
    new_batting_stats.append(name)



new_bowling_stats = []
for bowler in bowling_stats:
    splits = bowler.split('   ')
    name = [(splits[0].strip()).split(' ')[0]]
    score = splits[1].split(' ')
    name.extend(score)
    new_bowling_stats.append(name)


catches = []
run_outs = []
stumpings = []
for wicket in wickets:
    splits = wicket.split(' ')
    if splits[0] == 'c':
        player = splits[1].split(' ')[0]
        catches.append(player)
    if splits[0] == 'run':
        players = splits[2]
        players = players[1:len(players)].split('/')
        if len(players) == 1:
            player = players[0].split(' ')
            run_outs.append(player)
            run_outs.append(player)
        else:
            for p in players[:2]:
                player = p.split(' ')[0]
                run_outs.append(player)
    if splits[0] == 'st':
        player = splits[1].split(' ')[0]
        stumpings.append(player)

team[9] , team[11] = team[11] , team[9]

batsman = team[:10]
all_rounders = team[10:14]
bowlers = team[14:]

new_team = {}
for i in range(22):
    player = team[i].split(' ')

    if '(wk)' in player or '(c)' in player:
        team[i] = ' '.join(player[:-1])
        if i in range(10):
            batsman[i] = ' '.join(player[:-1])
        elif i in range(10,14):
            all_rounders[i-10] = ' '.join(player[:-1])
        else:
            bowler[i-14] = ' '.join(player[:-1])
    data = []


    for stats in new_batting_stats:
        if stats[0] in player:
            data.extend(stats[1:])

    if len(data) == 0:
        data.extend(['0']*5)

    for stats in new_bowling_stats:
        if stats[0] in player:
            data.extend(stats[1:])

    if len(data) == 5:
        data.extend(['0']*7)

    for p in player:
        if p in catches:
            break
    data.append(str(catches.count(p)))

    for p in player:
        if p in run_outs:
            break
    data.append(str(run_outs.count(p)))

    for p in player:
        if p in stumpings:
            break
    data.append(str(stumpings.count(p)))
    
    new_team[team[i]] = calculate(data ,team[i] not in bowlers)


new_team['Off'] = 0

new_team_ = {}
for i in new_team:
    new_team_[i] = new_team[i]
