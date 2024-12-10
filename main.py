import re
from visualization import show_table

file = open("data.txt", "r", encoding="utf-8").read()

rounds_strings = file.split("\n\n")
players = []

class Round:
    def __init__(self, current_round: str, place: str, points: str, mod_mean: str, solkoff: str, cumulative: str,
                 cumulative_opposition: str):
        self.current_round = int(current_round)
        self.place = int(place)
        self.points = float(points)
        self.mod_mean = float(mod_mean)
        self.solkoff = float(solkoff)
        self.cumulative = float(cumulative)
        self.cumulative_opposition = float(cumulative_opposition)

    def __repr__(self):
        return (f"Round(current_round={self.current_round}, place={self.place}, points={self.points}, "
                f"mod_mean={self.mod_mean}, solkoff={self.solkoff}, cumulative={self.cumulative}, "
                f"cumulative_opposition={self.cumulative_opposition})")

    def get_all_values(self):
        return self.place, self.points, self.mod_mean, self.solkoff, self.cumulative, self.cumulative_opposition

class Player:
    def __init__(self, player_name: str):
        self.name = player_name
        self.participated_rounds = []
        self.total_place = -1
        self.total_points = -1
        self.total_mod_mean = -1
        self.total_solkoff = -1
        self.total_cumulative = - 1
        self.total_cumulative_opposition = -1
        self.totals = [self.total_place, self.total_points, self.total_mod_mean, self.total_solkoff, self.total_cumulative, self.total_cumulative_opposition]

    def __repr__(self):
        rounds_repr = "\n    ".join(repr(r) for r in self.participated_rounds)
        return (f"{'Unranked' if self.get_participation_count() < 4 else 'Ranked'} Player(name={self.name!r}, total_place={self.total_place}, "
                f"participated_rounds=[\n    {rounds_repr}\n])")

    def add_player_round(self, round_to_add: Round):
        self.participated_rounds.append(round_to_add)
        self.participated_rounds = sorted(self.participated_rounds, key=lambda r: (r.place, r.points, r.mod_mean, r.solkoff, r.cumulative, r.cumulative_opposition))

    def get_participation_count(self):
        return len(self.participated_rounds)


    def calculate_totals(self):
        # Reset totals
        self.total_place = 0
        self.total_points = 0.0
        self.total_mod_mean = 0.0
        self.total_solkoff = 0.0
        self.total_cumulative = 0.0
        self.total_cumulative_opposition = 0.0

        # Sum up values from up to 4 best game nights
        for round_obj in self.participated_rounds[:4]:
            self.total_place += round_obj.place
            self.total_points += round_obj.points
            self.total_mod_mean += round_obj.mod_mean
            self.total_solkoff += round_obj.solkoff
            self.total_cumulative += round_obj.cumulative
            self.total_cumulative_opposition += round_obj.cumulative_opposition


def create_dictionary():
    player = {}
    for r in rounds_strings:
        lines = r.split("\n")
        current_round = 0
        for l in lines:
            if "Round" in l:
                current_round = re.search(r"(?<=Round )\d+", l).group()
                continue
            l = l.replace(u"½", u".5")
            place, name, points, mod_mean, solkoff, cumulative, cumulative_opposition = l.split("\t")
            if not any(player.name == name for player in players):
                players.append(Player(name))
            for player in players:
                if player.name == name:
                    player.add_player_round(Round(current_round, place, points, mod_mean, solkoff, cumulative, cumulative_opposition))
                    player.calculate_totals()
                    break
    return player

player_dictionary = create_dictionary()
players = sorted(players, key=lambda p: (p.get_participation_count(), -p.total_place), reverse=True)
for p in players:
    print(p)
    print("\n")

print("Minimum Participation")
inp = int(input())

players = [player for player in players if player.get_participation_count() >= inp]

show_table(players)