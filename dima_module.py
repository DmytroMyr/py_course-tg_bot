def movie_finder(genre, year):
    res = []

    with open('movies.txt', 'r') as f:
        for line in f:
            movie_line = line.strip().split(';')

            movie = {
                'title': movie_line[0],
                'genres': ', '.join(movie_line[1].split(', ')),
                'year': int(movie_line[2]),
                'link': movie_line[3]
            }

            if genre in movie['genres'] and year == movie['year']:
                res.append(f'{movie["title"]}\n{movie["genres"]}\n{movie["year"]}\n{movie["link"]}\n')

            if len(res) >= 5:
                break

    if len(res) > 0:
        return '\n'.join(res)
    else:
        return 'По вашим критеріям нічого не знайдено.'
