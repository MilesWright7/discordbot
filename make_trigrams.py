

# def to_dict(word, tri_dict):
#     if len(word) < 3:
#         return 0
#     else:
#         trigram_dict[word[:3]] += 1
#         to_dict(word[1:], tri_dict)

def main():
    trigram_dict = {}
    letters = 'abcdefghijklmnopqrstuvwxyz'
    # letters1 ='abc'
    for a in letters:
        for b in letters:
            for c in letters:
                trigram_dict[a+b+c] = 0

    # print(trigram_dict)
    # counter = 0

    with open('./assets/words_alpha.txt', 'r') as infile:
        for word in infile:
            # newline on end of each word so ill cut that off
            if word[-1] == '\n':
                word = word[:-1]
            
            
            while len(word) > 2:
                trigram_dict[word[:3]] += 1
                word = word[1:]
                    
            # WAY TOO SLOW METHOD. DONT NEED TO GO THROUGH ENTIRE DICT
            # JUST TO FIND THE FEW COMBINATINS IN THE WORD. JSUT GO THROUGH
            # LETTERS IN WORD TO INCREMENT THE DICT
            # for a in letters:
            #     for b in letters:
            #         for c in letters:
            #             if a+b+c in word:
            #                 trigram_dict[a+b+c] += 1

    with open('./assets/words_alpha_trigram.txt' , 'w') as outfile:
        for item in trigram_dict:
            outfile.write(f'{item} {trigram_dict[item]}\n')

if __name__ == '__main__':
    main()