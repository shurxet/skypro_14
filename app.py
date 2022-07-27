from flask import Flask, jsonify
import sqlite3



def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def connect(query):
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    @app.route('/movie/<title>')
    def search_by_title(title):
        query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC
                LIMIT 1
        """

        response = connect(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'listed_in': response[3],
            'description': response[4]
        }

        return jsonify(response_json)


    @app.route('/movie/<int:start>/to/<int:end>')
    def search_by_year_range(start, end):
        second_query = f"""
                   SELECT title, release_year
                   FROM netflix
                   WHERE release_year BETWEEN {start} AND {end}
                   ORDER BY release_year DESC
                   LIMIT 100
           """

        response = connect(second_query)
        response_json = []
        for i in response:
            response_json.append({
                                    'title': i[0],
                                    'release_year': i[1]
                                 })

        return jsonify(response_json)

    @app.route('/rating/children')
    def search_by_rating_child():
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating = 'G'
                       
"""

        response = connect(query)
        response_json = []
        for i in response:
            response_json.append({
                'title': i[0],
                'rating': i[1],
                'description': i[2]
            })

        return jsonify(response_json)

    @app.route('/rating/family')
    def search_by_rating_family():
        second_query = f"""
                           SELECT title, rating, description
                           FROM netflix
                           WHERE rating IN ('G', 'PG', 'PG-13') 

                   """

        response = connect(second_query)
        response_json = []
        for i in response:
            response_json.append({
                'title': i[0],
                'rating': i[1],
                'description': i[2]
            })

        return jsonify(response_json)

    @app.route('/rating/adult')
    def search_by_rating_adult():
        second_query = f"""
                               SELECT title, rating, description
                               FROM netflix
                               WHERE rating IN ('R', 'NC-17') 

                       """

        response = connect(second_query)
        response_json = []
        for i in response:
            response_json.append({
                'title': i[0],
                'rating': i[1],
                'description': i[2]
            })

        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        second_query = f"""
                                   SELECT title, description, listed_in, release_year
                                   FROM netflix
                                   WHERE listed_in LIKE '%{genre}%'
                                   ORDER BY release_year
                                   LIMIT 10

                           """

        response = connect(second_query)
        response_json = []
        for i in response:
            response_json.append({
                                    'title': i[0],
                                    'description': i[1].strip()
                                 })

        return jsonify(response_json)


    def get_actors(actors_1='Rose McIver', actors_2='Ben Lamb'):
        query = f"""
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE '%{actors_1}%'
                AND "cast" LIKE '%{actors_2}%'
    
        """

        response = connect(query)
        all_actors = []

        for actor in response:
            all_actors.extend(actor[0].split(', '))

        result = []

        for actors in all_actors:
            if actors not in [actors_1, actors_2] and all_actors.count(actors) > 2:
                result.append(actors)

        result = set(result)

        print(result)


    def get_movies_and_serials(type='Movie', year=2020, genre='Dramas'):
        query = f"""
                        SELECT type, release_year, listed_in 
                        FROM netflix
                        WHERE type = '{type}'
                        AND release_year = '{year}'
                        AND listed_in LIKE '%{genre}%'

                """

        response = connect(query)

        for film in response:
            print(f"\n", {
                          'title': film[0],
                          'year': film[1],
                          'genre': film[2]
            })


    #get_movies_and_serials()
    #get_actors()
    app.run()

if __name__ == '__main__':
    main()