from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.Game import Game

app = Flask(__name__)

games = []


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'data': 'Hello, World!'})

@app.route('/api/game/create', methods=['POST'])
def create_game():
    post = request.get_json()
    creator = post['player_id']

    g = Game()
    games.append(g)
    g.add_player(creator)
    return jsonify({'game_id': g.game_id})

@app.route('/api/game/join', methods=['POST'])
def join_game():
    post = request.get_json()
    game_id = post['game_id']
    player_id = post['player_id']

    try:
        g = [g for g in games if g.game_id == game_id][0]
    except:
        return jsonify({'error': 'Game does not exist'})

    if g is None:
        return jsonify({'error': 'Game not found'})
    elif len(g.players) == 3:
        return jsonify({'error': 'Game is full'})
    elif player_id in g.players:
        return jsonify({'error': 'Player already in game'})

    g.add_player(player_id)


    if len(g.players) == 2:
        return jsonify({'message': 'joined game, waiting for more players'})        
    if len(g.players) == 3:
        g.shuffle_players()
        g.status = g.players[0].name
        g.assigning_map_randomly()
        return jsonify({'message': 'game full, starting game'})

    return jsonify({'game_id': g.game_id})


@app.route('/api/game/<game_id>/status', methods=['GET'])
def game_status(game_id):
    g = [g for g in games if g.game_id == game_id][0]

    if g is None:
        return jsonify({'error': 'Game not found'})

    return jsonify({'status': g.status})

@app.route('/api/game/<game_id>/players', methods=['GET'])
def game_players(game_id):
    g = [g for g in games if g.game_id == game_id][0]

    if g is None:
        return jsonify({'error': 'Game not found'})
    
    names = [p.name for p in g.players]

    return jsonify({'players': names})

@app.route('/api/game/<game_id>/map', methods=['GET'])
def game_map(game_id):
    g = [g for g in games if g.game_id == game_id][0]

    if g is None:
        return jsonify({'error': 'Game not found'})
    
    new_map = g.map.copy()
    for row in new_map:
        row["owner"] = row["owner"].name if row["owner"] is not None else None


    return jsonify({'map': g.map})


if __name__ == '__main__':
    app.run("localhost", 8080, debug=True)