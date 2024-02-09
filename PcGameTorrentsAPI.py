from flask import Flask, jsonify, request, g
from flask_restful import Api
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from database import Database


@dataclass
class Game:
    name: str = None
    post_date: str = None
    info: str = None
    link: str = None


class PcGameTorrentsAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['DATABASE'] = 'PcGameTorrents.db'
        self.api = Api(self.app)
        self.url = "https://www.pcgametorrents.com"
        self.games = []
        self.port = 5000

        try:
            self.db = Database('PcGameTorrents.db')
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def scrape_game_data(self, item_div):
        name_element = item_div.find('a', class_='uk-link-reset')
        post_date_element = item_div.find('p', class_='uk-article-meta').find('time')
        info_element = item_div.find('div', class_='uk-margin-medium').find('p')
        link_element = item_div.find('a', class_='uk-link-reset')['href']

        name = name_element.text if name_element else None
        info = info_element.text if info_element else None
        link = f"{self.url}{link_element}" if link_element else None

        return Game(name, post_date_element, info, link)

    def search_game(self, game_name):
        self.games = []
        search_url = f'{self.url}/?s={game_name.replace(" ", "+")}'

        try:
            response = requests.get(search_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                game_div = soup.find('div', class_='uk-grid uk-child-width-1-1 uk-grid-stack')

                if game_div:
                    for item_div in game_div.find_all('div', class_='uk-first-column'):
                        game = self.scrape_game_data(item_div)
                        self.games.append(Game(game.name, game.post_date, game.info, game.link))

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.games

    def run(self):
        @self.app.teardown_appcontext
        def close_db_connection(exception):
            db = g.pop('db', None)

            if db is not None:
                db.close()

        @self.app.route('/search<game_name>', methods=['GET'])
        def search_route(game_name):
            try:
                games = self.search_game(game_name)

                if games:
                    self.db.add_games(games)

                    response_str = '\n'.join(f"{i + 1}: {game}" for i, game in enumerate(games))
                    return jsonify(response_str)
                else:
                    return jsonify({'message': 'No games found'}), 404

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/games/<game_name>', methods=['GET', 'PUT', 'DELETE'])
        def game_operations(game_name):
            if request.method == 'GET':
                return self.get_game_by_name(game_name)

            elif request.method == 'DELETE':
                return self.delete_game(game_name)

            return jsonify({'error': 'Invalid request method'}), 405

        self.app.run(port=self.port, debug=True)

    def get_game_by_name(self, game_name):
        result = self.db.get_game_by_name(game_name)
        if result:
            return jsonify(result)
        return jsonify({'message': 'Game not found'}), 404

    def delete_game(self, game_name):
        success = self.db.delete_game(game_name)
        if success:
            return jsonify({'message': 'Game deleted successfully'})
        return jsonify({'message': 'Failed to delete game'}), 500
