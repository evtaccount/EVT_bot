# import


def read_film_rates():
    temp_rate_var = []
    film_rate = open("filmrate.txt")
    for rate in film_rate:
        rate = int(rate.strip())
        temp_rate_var.append(rate)
    film_rate.close()
    return temp_rate_var


def write_film_rate(new_vote_films):
    with open('filmrate.txt', 'w') as wfilmrate:
        for n in range(len(new_vote_films)):
            wfilmrate.write(str(new_vote_films[n]['vote_film']) + '\n')


def read_used_id():
    used_id = []
    with open("film_rate_used_id.txt") as f:
        for read_var in f:
            read_var = int(read_var.strip())
            used_id.append(read_var)
    # print(used_id)
    return used_id


def write_used_id(new_used_id):
    used_id = []
    with open("film_rate_used_id.txt") as f:
        for read_var in f:
            read_var = int(read_var.strip())
            used_id.append(read_var)
    used_id.append(new_used_id)
    with open("film_rate_used_id.txt", "w") as f:
        for write_var in used_id:
            f.write(str(write_var) + '\n')