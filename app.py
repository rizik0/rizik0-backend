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

@app.route('/api/game/create', methods=['POST'])
def create_game():
    post = request.get_json()
    creator = post['player_id']

    g = Game()
    games.append(g)
    g.add_player(creator, 'red')
    return jsonify({'game_id': g.game_id})

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

    g.add_player(player_id, 'blue' if len(g.players) == 2 else 'green')

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

    return jsonify({'status': g.status})

@app.route('/api/game/<game_id>/players', methods=['GET'])
def game_players(game_id):
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]
    
    names = [p.name for p in g.players]

    return jsonify({'players': names})

@app.route('/api/game/<game_id>/maps', methods=['GET'])
def game_maps(game_id):
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    return jsonify({'maps': g.maps})


@app.route('/api/game/<game_id>/troops/available', methods=['GET'])
def troops_available(game_id):
    post = request.get_json()
    player_id = post['player_id']
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    if player_id != g.status:
        return jsonify({'error': 'Not your turn'})
    
    available_troops = int(g.from_player_receive_number_of_territories(player_id)/3)

    if (g.turn != 0 and g.turn % 3 == 0):
        available_troops += randint(8, 12) # BONUS!

    return jsonify({'troops': available_troops})


@app.route('/api/game/<game_id>/troops/place', methods=['POST'])
def troops_place(game_id):
    post = request.get_json()
    player_id = post['player_id']
    g = [g for g in games if g.game_id == game_id]
    
    if g == []:
        return jsonify({'error': 'Game not found'})
    
    g = g[0]

    player = [p for p in g.players if p.name == player_id][0]

    if player.name != g.status:
        return jsonify({'error': 'Not your turn'})

    
    g.maps = post['maps']

    return jsonify({'message': 'Troops placed'})


if __name__ == '__main__':
    app.run("localhost", 3000, debug=True)