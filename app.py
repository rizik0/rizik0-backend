from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.Game import Game
from random import randint

app = Flask(__name__)

games = []

CORS(app)

@app.route('/api', methods=['GET'])
def api():
    return jsonify({'data': 'Hello, World!'})

# Definitive
@app.route('/api/game/create', methods=['POST'])
def create_game():
    post = request.get_json()
    creator = post['player_id']

    g = Game()
    games.append(g)
    g.add_player(creator, 'red')
    return jsonify({'game_id': g.game_id})

# Definitive
@app.route('/api/game/join', methods=['POST'])
def join_game():
    post = request.get_json()
    game_id = post['game_id']
    player_id = post['player_id']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]
    
    if len(g.players) == 3:
        return jsonify({'error': 'Game is full'})
    elif player_id in g.players:
        return jsonify({'error': 'Player already in game'})

    g.add_player(player_id, 'blue' if len(g.players) == 2 else 'yellow')

    if len(g.players) == 2:
        return jsonify({'message': 'joined game, waiting for more players'})        
    if len(g.players) == 3:
        g.shuffle_players()
        g.status = g.players[0].name
        g.assigning_maps_randomly()
        return jsonify({'message': 'game full, starting game'})

    return jsonify({'game_id': g.game_id})


@app.route('/api/game/<game_id>/status', methods=['GET'])
def game_status(game_id):    
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    return jsonify({'maps': g.maps, 'status': g.status, 'turn': g.turn, 'phase': g.turn_status, 'players': [{'name': p.name, 'color': p.color} for p in g.players]})

# Temporary
@app.route('/api/game/<game_id>/players', methods=['GET'])
def game_players(game_id):
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]
    
    names = [{"name": p.name, "color": p.color} for p in g.players]

    return jsonify({'players': names})


@app.route('/api/game/<game_id>/play/initial/get', methods=['POST'])
def game_play_initial_get(game_id):
    post = request.get_json()
    player_id = post['player_id']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'initial':
        return jsonify({'error': 'Not in initial phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    return jsonify({'troops': p.initial_units})

@app.route('/api/game/<game_id>/play/initial/place', methods=['POST'])
def game_play_initial_place(game_id):
    post = request.get_json()
    player_id = post['player_id']
    troops = int(post['troops'])
    territory = post['territory']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'initial':
        return jsonify({'error': 'Not in initial phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    if p.initial_units < troops:
        return jsonify({'error': 'Not enough troops'})

    p.initial_units -= troops

    g.maps[g.from_territory_name_get_territory_index(territory)]['troops'] += troops

    if p.initial_units == 0:
        if player_id == g.players[2].name:
            g.status = g.players[0].name
            g.turn_status = 'positioning'
        else:
            g.status = g.players[(g.players.index(p) + 1)].name

    return jsonify({'troops': p.initial_units})

@app.route('/api/game/<game_id>/play/positioning/get', methods=['POST'])
def game_play_positioning_get(game_id):
    post = request.get_json()
    player_id = post['player_id']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'positioning':
        return jsonify({'error': 'Not in positioning phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    continent_bonus = 0
    random_bonus = 0

    if g.has_a_full_continent(p.name, 'africa'):
        continent_bonus += 3
    if g.has_a_full_continent(p.name, 'asia'):
        continent_bonus += 7
    if g.has_a_full_continent(p.name, 'europe'):
        continent_bonus += 5
    if g.has_a_full_continent(p.name, 'north_america'):
        continent_bonus += 5
    if g.has_a_full_continent(p.name, 'oceania'):
        continent_bonus += 2
    if g.has_a_full_continent(p.name, 'south_america'):
        continent_bonus += 2
    
    if int(g.turn/3) != 0 and int(g.turn/3) % 3 == 0:
        random_bonus = randint(6, 12)
    
    if p.initial_units == 0:
        p.initial_units = int(g.from_player_receive_number_of_territories(p.name)/3) + continent_bonus + random_bonus
    
    return jsonify({'troops': p.initial_units})

@app.route('/api/game/<game_id>/play/positioning/place', methods=['POST'])
def game_play_positioning_place(game_id):
    post = request.get_json()
    player_id = post['player_id']
    troops = int(post['troops'])
    territory = post['territory']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'positioning':
        return jsonify({'error': 'Not in positioning phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    if p.initial_units < troops:
        return jsonify({'error': 'Not enough troops'})

    p.initial_units -= troops

    g.maps[g.from_territory_name_get_territory_index(territory)]['troops'] += troops

    if p.initial_units == 0:
        g.turn_status = 'attacking'

    return jsonify({'troops': p.initial_units})

@app.route('/api/game/<game_id>/play/attacking/', methods=['POST'])
def game_play_attacking(game_id):
    post = request.get_json()
    player_id = post['player_id']
    from_territory = post['from_territory']
    to_territory = post['to_territory']
    troops = int(post['troops'])

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'attacking':
        return jsonify({'error': 'Not in attacking phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    from_territory_index = g.from_territory_name_get_territory_index(from_territory)
    to_territory_index = g.from_territory_name_get_territory_index(to_territory)

    if g.maps[from_territory_index]['troops'] + 1 <= troops:
        return jsonify({'error': 'Not enough troops'})

    if g.maps[from_territory_index]['owner'] != player_id:
        return jsonify({'error': 'Not your territory'})

    if g.maps[to_territory_index]['owner'] == player_id:
        return jsonify({'error': 'Cannot attack your own territory'})

    if g.maps[from_territory_index]['neighbours'].count(to_territory) == 0:
        return jsonify({'error': 'Territories are not neighbours'})
    
    if troops > 3:
        return jsonify({'error': 'Cannot attack with more than 3 troops'})
    
    if troops < 1:
        return jsonify({'error': 'Cannot attack with less than 1 troop'})
    
    defending_troops = g.maps[to_territory_index]['troops']
    attacking_troops = troops

    if defending_troops > 3:
        defending_troops = 3
    
    attacking_dices = []
    defending_dices = []

    for i in range(attacking_troops):
        attacking_dices.append(randint(1, 6))

    for i in range(defending_troops):
        defending_dices.append(randint(1, 6))

    attacking_dices.sort(reverse=True)
    defending_dices.sort(reverse=True)

    attack_losses = 0
    defense_losses = 0

    for i in range(min(len(attacking_dices), len(defending_dices))):
        if attacking_dices[i] > defending_dices[i]:
            g.maps[to_territory_index]['troops'] -= 1
            defense_losses += 1
        else:
            g.maps[from_territory_index]['troops'] -= 1
            attack_losses += 1

    # g.maps[to_territory_index]['troops'] -= troops

    # if g.maps[to_territory_index]['troops'] == 0:
    #     g.maps[to_territory_index]['owner'] = player_id
    #     g.maps[to_territory_index]['troops'] = troops
    #     g.maps[from_territory_index]['troops'] -= troops
    # else:
    #     g.maps[from_territory_index]['troops'] -= troops

    if g.maps[to_territory_index]['troops'] == 0:
        g.maps[to_territory_index]['owner'] = player_id
        g.maps[to_territory_index]['color'] = p.color
        g.maps[to_territory_index]['troops'] = troops - attack_losses
        g.maps[from_territory_index]['troops'] -= troops

        return jsonify({'won': 'yes', 'attack_losses': attack_losses, 'defense_losses': defense_losses, 'attacking_dices': attacking_dices, 'defending_dices': defending_dices})

    return jsonify({'won': 'no', 'attack_losses': attack_losses, 'defense_losses': defense_losses, 'attacking_dices': attacking_dices, 'defending_dices': defending_dices})

@app.route('/api/game/<game_id>/play/attacking/move', methods=['POST'])
def game_play_attacking_move(game_id):
    post = request.get_json()
    player_id = post['player_id']
    from_territory = post['from_territory']
    to_territory = post['to_territory']
    troops = int(post['troops'])

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'attacking':
        return jsonify({'error': 'Not in attacking phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    from_territory_index = g.from_territory_name_get_territory_index(from_territory)
    to_territory_index = g.from_territory_name_get_territory_index(to_territory)

    if g.maps[from_territory_index]['troops'] <= troops:
        return jsonify({'error': 'Not enough troops'})

    if g.maps[from_territory_index]['owner'] != player_id:
        return jsonify({'error': 'Not your territory'})

    if g.maps[to_territory_index]['owner'] != player_id:
        return jsonify({'error': 'Not your territory'})

    if g.maps[from_territory_index]['neighbours'].count(to_territory) == 0:
        return jsonify({'error': 'Territories are not neighbours'})

    g.maps[to_territory_index]['troops'] += troops
    g.maps[from_territory_index]['troops'] -= troops

    return jsonify({'message': 'Troops moved'})

@app.route('/api/game/<game_id>/play/attacking/end', methods=['POST'])
def game_play_attacking_end(game_id):
    post = request.get_json()
    player_id = post['player_id']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'attacking':
        return jsonify({'error': 'Not in attacking phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    g.turn_status = 'movement'

    return jsonify({'message': 'Attacking phase ended'})

if __name__ == '__main__':
    app.run("localhost", 3000, debug=True)