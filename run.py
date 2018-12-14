import subprocess
import os, sys
import random

def show_match(bot, opponent_bot, map_num):
    """
        Runs an instance of Planet Wars between the two given bots on the specified map. After completion, the
        game is replayed via a visual interface.
    """
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) + '.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" ' + \
              '| java -jar tools/ShowGame.jar'
    print(command)
    os.system(command)


def test(bot, opponent_bot, map_num):
    """ Runs an instance of Planet Wars between the two given bots on the specified map. """
    bot_name, opponent_name = bot.split('/')[1].split('.')[0], opponent_bot.split('/')[1].split('.')[0]
    print('Running test:',bot_name,'vs',opponent_name)
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) +'.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" '

    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    wins = 0
    losses = 0
    crashes = 0
    timed_out = 0

    while True:
        return_code = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline().decode('utf-8')
        if '1 timed out' in line:
            print(bot_name,'timed out.')
            timed_out+=1
            break
        elif '2 timed out' in line:
            print(opponent_name,'timed out.')
            break
        elif '1 crashed' in line:
            print(bot_name, 'crashed.')
            crashes+=1
            break
        elif '2 crashed' in line:
            #print(opponent_name, 'crashed')
            break
        elif 'Player 1 Wins!' in line:
            print(bot_name,'wins!------------------------------------------------')
            wins+=1
            break
        elif 'Player 2 Wins!' in line:
            print(opponent_name,'wins!')
            losses+=1
            break

        if return_code is not None:
            break

    results = {
        "wins" : 0,
        "losses" : 0,
        "crashes" : 0,
        "timed_out": 0,
        "easy_bot": 0,
        "spread_bot": 0,
        "aggressive_bot": 0,
        "defensive_bot": 0,
        "production_bot": 0,
        "win_percentage": 0,
        "unique_wins": 0
    }

    results[opponent_name] = wins
    results["wins"] = wins
    results["losses"] = losses
    #results["wins"] += wins
    p.kill()
    return results


def add_results(r1, r2):
    """
    r1["wins"] += r2["wins"]
    r1["losses"] += r2["losses"]
    r1["crashes"] += r2["crashes"]
    r1["timed_out"] += r2["timed_out"]
    """
    for key in r1.keys():
        r1[key] += r2[key]


def run_test(show = False, all = False):
    results = {
        "wins" : 0,
        "losses" : 0,
        "crashes" : 0,
        "timed_out": 0,
        "easy_bot": 0,
        "spread_bot": 0,
        "aggressive_bot": 0,
        "defensive_bot": 0,
        "production_bot": 0,
        "win_percentage": 0,
        "unique_wins": 0
    }
    
    #Run sim 3 times, to likely test the bot against each opponent on 3 randomized maps, lessening the chance
    #that randomly generated bots will just beat all 4 at the end and be picked as a good tree
    #number_runs = 100 if all else 5
    runs = range(1, 101) if all else range(0, 5)
    for i in runs:
        path =  os.getcwd()
        opponents = ['opponent_bots/easy_bot.py',
                     'opponent_bots/spread_bot.py',
                     'opponent_bots/aggressive_bot.py',
                     #'opponent_bots/defensive_bot.py',
                     'opponent_bots/production_bot.py'
                     ]

        #maps = [71, 13, 24, 56, 7]
        maps = []

        if all == True:
            maps = [i, i, i, i, i]
        else:
            for i in range(0, 5):
                maps.append(random.randint(1, 100))

        my_bot = 'behavior_tree_bot/bt_bot.py'
        #show = False



        for opponent, map in zip(opponents, maps):
            # use this command if you want to observe the bots
            if show:
                show_match(my_bot, opponent, map)
            else:
                # use this command if you just want the results of the matches reported
                add_results(results, test(my_bot, opponent, map))

    
    results["win_percentage"] = results["wins"]/((float(results["wins"]) + results["losses"]))

    games = 100 if all else 5
    results["easy_bot"] /= games
    results["aggressive_bot"] /= games
    results["production_bot"] /= games
    results["spread_bot"] /= games

    unique_wins = 0
    if results["easy_bot"] != 0:
        unique_wins += 1
    if results["aggressive_bot"] != 0:
        unique_wins += 1
    if results["spread_bot"] != 0:
        unique_wins += 1
    if results["production_bot"] != 0:
        unique_wins += 1
    results["unique_wins"] = unique_wins
    return results
    

if __name__ == '__main__':
    path =  os.getcwd()
    opponents = ['opponent_bots/easy_bot.py',
                 'opponent_bots/spread_bot.py',
                 'opponent_bots/aggressive_bot.py',
                 'opponent_bots/defensive_bot.py',
                 'opponent_bots/production_bot.py']

    maps = [71, 13, 24, 56, 7]

    my_bot = 'behavior_tree_bot/bt_bot.py'
    show = len(sys.argv) < 2 or sys.argv[1] == "show"
    for opponent, map in zip(opponents, maps):
        # use this command if you want to observe the bots
        if show:
            show_match(my_bot, opponent, map)
        else:
            # use this command if you just want the results of the matches reported
            test(my_bot, opponent, map)
