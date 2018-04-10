#!/usr/bin/env python3


def main():

    with open('input_text') as input_text:
        input_data = input_text.read()

        words = input_data.split()
        words_dict = {k: v for k, v in enumerate(words)}
        check_words = ["ADJECTIVE", 'NOUN', 'ADVERB', 'VERB']

        for idx, word in words_dict.items():
            for cw in check_words:
                if cw in word:
                    if cw == 'ADJECTIVE':
                        print('Введите имя прилагательное: ')
                        words_dict[idx] = input()
                    elif cw == 'NOUN':
                        print('Введите имя существительное: ')
                        words_dict[idx] = input()
                    elif cw == 'ADVERB':
                        print('Введите наречие: ')
                        words_dict[idx] = input()
                    elif cw == 'VERB':
                        print('Введите глагол: ')
                        words_dict[idx] = input()

        print(' '.join(words_dict.values()))


if __name__ == '__main__':
    main()
