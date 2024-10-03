from flask import Flask, request, jsonify, render_template
from typing import List, Tuple

app = Flask(__name__)

RANKS = [
    "iron4", "iron3", "iron2", "iron1",
    "bronze4", "bronze3", "bronze2", "bronze1",
    "silver4", "silver3", "silver2", "silver1",
    "gold4", "gold3", "gold2", "gold1",
    "platinum4", "platinum3", "platinum2", "platinum1",
    "emerald4", "emerald3", "emerald2", "emerald1",
    "diamond4", "diamond3", "diamond2", "diamond1",
    "master", "grandmaster", "challenger"
]

ROLES = ["TOP", "JG", "MID", "ADC", "SUP"]

class Player:
    def __init__(self, name: str, rank: str, roles: List[str]):
        self.name = name
        self.rank = RANKS.index(rank)  # ランクを数値に変換
        self.roles = roles

def create_teams(players: List[Player]) -> Tuple[List[Player], List[Player]]:
    if len(players) != 10:
        raise ValueError("プレイヤー数は10人である必要があります。")

    # ランクでソート（高いランクが先になるように逆順にする）
    sorted_players = sorted(players, key=lambda x: x.rank, reverse=True)
    
    team1 = []
    team2 = []
    
    # スネーク方式でチーム分け
    for i, player in enumerate(sorted_players):
        if i % 4 < 2:
            team1.append(player)
        else:
            team2.append(player)
    
    # ロールの分布を確認と調整のロジックは変更なし

    return team1, team2

@app.route('/')
def index():
    return render_template('index.html', ranks=RANKS, roles=ROLES)

@app.route('/create_teams', methods=['POST'])
def api_create_teams():
    data = request.json
    players = [Player(p['name'], p['rank'], p['roles']) for p in data['players']]
    
    if len(players) != 10:
        return jsonify({"error": "プレイヤー数は10人である必要があります。"}), 400
    
    try:
        team1, team2 = create_teams(players)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    result = {
        'team1': [{'name': p.name, 'rank': RANKS[p.rank], 'roles': p.roles} for p in team1],
        'team2': [{'name': p.name, 'rank': RANKS[p.rank], 'roles': p.roles} for p in team2]
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
