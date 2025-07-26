def get_team_names():
    filename = "data/MTeams.csv"
    team_names = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip().split(",")
            team_names[line[1].lower()] = int(line[0])

    return team_names


# win percent chance
# dict[name1] -> dict[name2] -> tuple[total games, name1 wins]
def get_win_percent():
    files = [
        "data/MRegularSeasonCompactResults.csv",
        "data/MConferenceTourneyGames.csv",
        "data/MGameCities.csv",
        "data/MNCAATourneyCompactResults.csv",
        "data/MSecondaryTourneyCompactResults.csv",
    ]
    win_percent = {}
    for filename in files:
        with open(filename, "r") as f:
            lines = f.readlines()
            line1 = lines[0].strip().split(",")
            win_col = line1.index("WTeamID")
            loss_col = line1.index("LTeamID")
            for line in lines[1:]:
                line = line.strip().split(",")
                team1 = int(line[win_col])
                team2 = int(line[loss_col])
                if team1 not in win_percent:
                    win_percent[team1] = {}
                if team2 not in win_percent[team1]:
                    win_percent[team1][team2] = [0, 0]
                win_percent[team1][team2][0] += 1
                win_percent[team1][team2][1] += 1

                if team2 not in win_percent:
                    win_percent[team2] = {}
                if team1 not in win_percent[team2]:
                    win_percent[team2][team1] = [0, 0]
                win_percent[team2][team1][0] += 1

    return win_percent


def get_average_scores():
    files = [
        "data/MRegularSeasonCompactResults.csv",
        "data/MConferenceTourneyGames.csv",
        "data/MGameCities.csv",
        "data/MNCAATourneyCompactResults.csv",
        "data/MSecondaryTourneyCompactResults.csv",
    ]
    scores = {}
    for filename in files:
        print("my filename is", filename)
        with open(filename, "r") as f:
            lines = f.readlines()
            line1 = lines[0].strip().split(",")
            if "WScore" not in line1:
                continue

            win_col = line1.index("WTeamID")
            loss_col = line1.index("LTeamID")
            score_col = line1.index("WScore")
            for line in lines[1:]:
                line = line.strip().split(",")
                team1 = int(line[win_col])
                team2 = int(line[loss_col])
                score1 = int(line[score_col])
                score2 = 200 - score1
                if team1 not in scores:
                    scores[team1] = []
                if team2 not in scores:
                    scores[team2] = []
                scores[team1].append(score1)
                scores[team2].append(score2)
    return scores


def main():
    team_names = get_team_names()
    win_percent = get_win_percent()
    while True:
        team1 = input("Enter team 1: ").lower()
        team2 = input("Enter team 2: ").lower()
        team1_id = team_names[team1]
        team2_id = team_names[team2]
        if (
            team1_id not in win_percent
            or team2_id not in win_percent[team1_id]
        ):
            print("No data available")
            continue

        total_games = win_percent[team1_id][team2_id][0]
        team1_wins = win_percent[team1_id][team2_id][1]
        team2_wins = total_games - team1_wins
        team1_win_percent = team1_wins / total_games
        team2_win_percent = team2_wins / total_games
        print(f"{team1} win percent: {team1_win_percent}")
        print(f"{team2} win percent: {team2_win_percent}")
        print("")


def main2():
    # given a name return average, median, and mode scores
    team_names = get_team_names()
    scores = get_average_scores()
    while True:
        team = input("Enter team: ").lower()
        team_id = team_names[team]
        if team_id not in scores:
            print("No data available")
            continue

        team_scores = scores[team_id]
        average = sum(team_scores) / len(team_scores)
        team_scores.sort()
        median = team_scores[len(team_scores) // 2]
        mode = max(set(team_scores), key=team_scores.count)
        print(f"{team} average score: {average}")
        print(f"{team} median score: {median}")
        print(f"{team} mode score: {mode}")
        print("")


if __name__ == "__main__":
    main2()
