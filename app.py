from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.Game import Game
from random import randint
import sqlite3
from flask import g
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_current_user, get_jwt_identity
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
import os
import sqlite3

#CONFIG
#database.db removal
if os.path.exists('database.db'):
    os.remove('database.db')
#database config
with open('database.sql', 'r') as sql_file:
    sql_script = sql_file.read()
#execute sql script
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.close()

#app config
SECRET_KEY = "TommyCAT"
ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

games = []

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

#ROUTES
@app.route('/api/player/register', methods=['POST'])
def register():
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()

    post = request.get_json()
    print(post)

    username = post[0]
    email = post[1]
    password_hash = post[2]

    cursor.execute('''INSERT INTO players (username,email,password_hash) VALUES (?, ?, ?);''', (username, email, bcrypt.generate_password_hash(password_hash).decode('utf-8')))

    sqliteConnection.commit()
    return jsonify({'message': 'Player registered'})

@app.route('/api/player/login', methods=['POST'])
def login():
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()

    post = request.get_json()
    print(post)

    username = post[0]
    password = post[1]

    cursor.execute('''SELECT * FROM players WHERE username = ?;''', (username,))
    player = cursor.fetchone()

    if player == None:
        return jsonify({'error': 'Player not found'})

    if bcrypt.check_password_hash(player[2], password):
        access_token = create_access_token(identity={'username':player[0],'email':player[1],'expires':(datetime.now() + timedelta(hours=1)).strftime("%m/%d/%Y, %H:%M:%S")})
        result = access_token
    else:
        result = jsonify({'error': 'Wrong username/password'})

    result = {'jwt': result}

    print(jsonify(result))
    return jsonify(result)

@app.route('/api/player/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()

    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()

    cursor.execute('''SELECT count(*) FROM games WHERE winner = ?;''', (current_user['username'],))

    wins = cursor.fetchone()[0]

    cursor.execute('''SELECT count(*) FROM games WHERE player1 = ? OR player2 = ? OR player3 = ?;''', (current_user['username'], current_user['username'], current_user['username']))
    
    games = cursor.fetchone()[0]


    return jsonify({'wins': wins, 'games': games})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()

    cursor.execute('''
        SELECT username, (SELECT count(*) FROM games WHERE winner = username) as wins 
        FROM players
        ORDER BY wins DESC;
    ''')

    leaders = cursor.fetchall()

    return jsonify({'standings': leaders, 'potw': 'Cristian'})

    
@app.route('/api/game/create', methods=['POST'])
@jwt_required()
def create_game():
    creator = get_jwt_identity()

    g = Game()
    games.append(g)
    g.add_player(creator['username'], 'red')
    return jsonify({'game_id': g.game_id, 'playerGoal': g.players[0].goal})

@app.route('/api/game/join', methods=['POST'])
@jwt_required()
def join_game():
    post = request.get_json()
    game_id = post['game_id']
    player_id = get_jwt_identity()['username']

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]
    
    if len(g.players) == 3:
        return jsonify({'error': 'Game is full'})
    elif player_id in g.players:
        return jsonify({'error': 'Player already in game'})

    g.add_player(player_id, 'blue' if len(g.players) == 2 else 'yellow')

    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})
    
    p = p[0]

    if len(g.players) == 2:
        return jsonify({'message': 'joined game, waiting for more players', 'playerGoal': p.goal})        
    if len(g.players) == 3:
        g.shuffle_players()
        g.status = g.players[0].name
        g.assigning_maps_randomly()
        return jsonify({'message': 'game full, starting game', 'playerGoal': p.goal})
    return jsonify({'game_id': g.game_id})


@app.route('/api/game/<game_id>/status', methods=['GET'])
def game_status(game_id):    
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    return jsonify({'maps': g.maps, 'status': g.status, 'turn': g.turn, 'phase': g.turn_status, 'players': [{'name': p.name, 'color': p.color} for p in g.players]})

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
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    if p.initial_units < troops:
        return jsonify({'error': 'Not enough troops'})
    
    if troops < 1:
        return jsonify({'error': 'Cannot place less than 1 troop'})
    
    if g.maps[g.from_territory_name_get_territory_index(territory)]['owner'] != player_id:
        return jsonify({'error': 'This territory is not yours'})

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

    if troops < 1:
        return jsonify({'error': 'Cannot place less than 1 troop'})
    
    if g.maps[g.from_territory_name_get_territory_index(territory)]['owner'] != player_id:
        return jsonify({'error': 'This territory is not yours'})

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
        return jsonify({'error': 'Not enough troops, at least one troop needs to stay here'})

    if g.maps[from_territory_index]['owner'] != player_id:
        return jsonify({'error': 'The territory you are moving troops from is not yours'})

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


    if g.maps[to_territory_index]['troops'] == 0:
        g.maps[to_territory_index]['owner'] = player_id
        g.maps[to_territory_index]['color'] = p.color
        g.maps[to_territory_index]['troops'] = troops - attack_losses
        g.maps[from_territory_index]['troops'] -= troops

        if g.has_a_full_continent(player_id, p.goal):
            g.turn_status = 'won'
            sqliteConnection = sqlite3.connect('database.db')
            cursor = sqliteConnection.cursor()
            cursor.execute('''INSERT INTO games (player1, player2, player3, winner, winner_goal, match_year, match_month, match_day) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', (g.players[0].name, g.players[1].name, g.players[2].name, player_id, p.goal, 2024, 5, 23))
            sqliteConnection.commit()
            cursor.close()

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

    if troops < 1:
        return jsonify({'error': 'Cannot place less than 1 troop'})

    if g.maps[from_territory_index]['troops'] <= troops:
        return jsonify({'error': 'Not enough troops'})

    if g.maps[from_territory_index]['owner'] != player_id:
        return jsonify({'error': 'The territory you are moving troops from is not yours'})

    if g.maps[to_territory_index]['owner'] != player_id:
        return jsonify({'error': 'The territory you are moving troops to is not yours'})

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

@app.route('/api/game/<game_id>/play/movement/', methods=['POST'])
def game_play_movement(game_id):
    post = request.get_json()
    player_id = post['player_id']
    from_territory = post['from_territory']
    to_territory = post['to_territory']
    troops = int(post['troops'])

    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if g.turn_status != 'movement':
        return jsonify({'error': 'Not in movement phase'})
    
    p = [p for p in g.players if p.name == player_id]

    if p == []:
        return jsonify({'error': 'Player not found'})

    p = p[0]

    from_territory_index = g.from_territory_name_get_territory_index(from_territory)
    to_territory_index = g.from_territory_name_get_territory_index(to_territory)

    if g.maps[from_territory_index]['troops'] <= troops:
        return jsonify({'error': 'Not enough troops'})

    if g.maps[from_territory_index]['owner'] != player_id:
        return jsonify({'error': 'The territory you are moving troops from is not yours'})

    if g.maps[to_territory_index]['owner'] != player_id:
        return jsonify({'error': 'The territory you are moving troops to is not yours'})

    if g.maps[from_territory_index]['neighbours'].count(to_territory) == 0:
        return jsonify({'error': 'Territories are not neighbours'})

    g.maps[to_territory_index]['troops'] += troops
    g.maps[from_territory_index]['troops'] -= troops

    g.turn += 1
    g.turn_status = 'positioning'
    g.status = g.players[g.turn % 3].name

    return jsonify({'message': 'Troops moved'})

if __name__ == '__main__':
    app.run("localhost", 3000, debug=True)