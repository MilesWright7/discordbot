import operator


with open('./assets/words_alpha_trigram.txt', 'r') as f, open('./assets/words_alpha_trigram_sorted.txt', 'w') as o:
    tri_dict = {}
    for line in f:
        key, value = line.split(' ')
        tri_dict[key] = int(value)

    sort = sorted(tri_dict.items(), key=operator.itemgetter(1),  reverse=True)

    for item in sort:
        if item[1] > 0:
            o.write(f'{item[0]} {item[1]}\n')
