import sys
import config
import redis

redis_db = redis.StrictRedis(host='localhost', decode_responses=True, port=6379, db=0)

# def read_known_users():
#     known_users = []
#     with open("data/user_ids.txt", encoding='utf-8') as f:
#         for user_id in f:
#             user_id = user_id.strip().split(',')
#             user_id[0] = int(user_id[0])
#             known_users.append(user_id)
#     return known_users


# def get_known_ids():



# def write_new_user(message):
#     current_user = message
#     print('cr', current_user)
#     current_user[0] = str(current_user[0])
#     current_user = ','.join(current_user)
#
#     try:
#         with open("data/user_ids.txt", "a") as f:
#             f.write('\n' + current_user)
#     except:
#         print('exc', current_user)
#         with open("data/user_ids.txt", "a", encoding='utf-8') as f:
#             f.write('\n' + current_user)
#     return True


def save_new_user(user_info):
    if not redis_db.sismember('users:ids', user_info.id):
        redis_db.sadd('users:ids', user_info.id)
        redis_db.hmset('users:' + str(user_info.id), {'user_name': user_info.username,
                                                    'first_name': user_info.first_name,
                                                    'last_name': user_info.last_name})
        return True
    else:
        return False


# def take_user(message):
#     user = []
#     user.append(message.from_user.id)
#
#     if message.from_user.first_name != None:
#         user.append(message.from_user.first_name)
#         print("first_not_none")
#     else:
#         print('first_none')
#         user.append('None')
#
#     if message.from_user.last_name != None:
#         print('last_not_none')
#         user.append(message.from_user.last_name)
#     else:
#         print('lnone')
#         user.append('None')
#
#     print(user)
#     return user


def read_film_rates():
    with open("data/filmrate.txt") as f:
        for n, film_data in enumerate(f):
            film_data = film_data.strip().split(',')
            film_data[1] = int(film_data[1])
            config.vote_films[n]['film'] = film_data[0]
            config.vote_films[n]['vote_film'] = film_data[1]
    return config.vote_films


def write_film_rates(film_rates):
    # with open('filmrate.txt', 'w') as wfilmrate:
    #     for n in range(len(new_vote_films)):
    #         wfilmrate.write(str(new_vote_films[n]['vote_film']) + '\n')
    try:
        with open("data/filmrate.txt", 'w') as f:
            for pos in film_rates:
                temp_list = []
                temp_list.append(pos['film'])
                temp_list.append(str(pos['vote_film']))
                pos = ','.join(temp_list)
                f.write(str(pos) + '\n')
        return True

    except:
        return False


def read_film_rates_with_id(param):
    list_ids_with_film = []
    names_and_rates = []
    # used_ids = []
    films_with_ids = (
        {'film_name': '', 'user_ids': [], 'rate': 0},
        {'film_name': '', 'user_ids': [], 'rate': 0},
        {'film_name': '', 'user_ids': [], 'rate': 0}
    )
    with open("data/film_rate_used_ids.txt") as f:
        for n, film_with_ids in enumerate(f):
            film_with_ids = film_with_ids.strip().split(',')
            films_with_ids[n]['film_name'] = film_with_ids.pop(0)
            films_with_ids[n]['user_ids'] = list(map(lambda x: int(x), film_with_ids))
            films_with_ids[n]['rate'] = len(films_with_ids[n]['user_ids'])

    if param == 0:
        temp = list(map(lambda ind: films_with_ids[ind]['user_ids'], range(len(films_with_ids))))
        used_ids = temp[0] + temp[1] + temp[2]
        return used_ids
    elif param == 1:
        print(films_with_ids)
        return films_with_ids


def get_film_rates():
    film_rates = []
    film_names = redis_db.hgetall('films:names')
    for ind, key in enumerate(film_names.keys()):
        film_rates.append({key: film_names[key], 'rate': redis_db.scard('films:' + film_names[key])})
    return film_rates


def save_film_rates(user_id, choosen_film):
    film_names = redis_db.hvals('films:names')
    choosen_film = redis_db.hgetall('films:names').get(choosen_film)
    film_names.remove(choosen_film)
    if not redis_db.sismember('films:' + film_names[0], user_id) and not redis_db.sismember('films:' + film_names[1], user_id):
        if not redis_db.sismember('films:' + choosen_film, user_id):
            redis_db.sadd('films:' + choosen_film, user_id)
        else:
            redis_db.srem('films:' + choosen_film, user_id)

    return get_film_rates()


def write_film_rates_with_id(film_rates):
    temp_list = []
    print('fr', film_rates)
    for ind, pos in enumerate(film_rates):
        new_line = []
        # temp_list[ind].append(new_line)
        new_line.append(pos['film_name'])
        new_line += list(map(lambda ind: str(pos['user_ids'][ind]), range(len(pos['user_ids']))))
        temp_list.append(new_line)

    # with open('filmrate.txt', 'w') as wfilmrate:
    #     for n in range(len(new_vote_films)):
    #         wfilmrate.write(str(new_vote_films[n]['vote_film']) + '\n')
    try:
        with open("data/film_rate_used_ids.txt", "w") as f:
            for ind in range(len(temp_list)):
                f.write(','.join(temp_list[ind]) + '\n')
    except:
        pass
        # print(current_user)
        # with open("data/user_ids.txt", "a", encoding='utf-8') as f:
        #     f.write('\n' + current_user)