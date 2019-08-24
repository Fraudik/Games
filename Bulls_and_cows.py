import random
import tkinter
from itertools import product


class B_n_c_game:
    def __init__(self):
        print('Угадывающий называет число, а загадывающий специальным образом отвечает, '
              'сколько цифр совпало с ответом.')
        print('Если в названном числе цифра какого-то разряда совпала с цифрой в том же разряде правильного ответа, '
              'это называется «быком». Если указанная цифра есть в ответе, но на неверной позиции, это «корова».')
        print('Загадывающий отвечает, сколько «быков» и «коров» в числе угадывающего.')
        print('В полной версии оба игрока пытаются отгадать число оппонента и не дать отгадать свое.')
        print('Внимание...')
        print('На старт...')
        print('Вы готовы? Да/Нет')
        print('Не важно.')
        print("Начали!")
        random.seed(self.generate_answer())
        self.attempt = self.k = 0
        self.everything = ["".join(x) for x in product('0123456789', repeat=4)
                           if len(set(x)) == len(x)]
        self.answer = self.generate_answer()
        self.guess_space = set(self.everything)
        self.historys = []
        self.history = []
        self.digitals = []
        self.__play()

    def __is_compatible(self, guess):
        return all(self.bulls_n_cows(guess, previous_guess) == (bulls, cows)
                   for previous_guess, bulls, cows in self.historys)

    def __player(self):
        global wie
        self.attempt += 1
        while True:
            if len(self.guess_space) == 0:
                print('Ты пытался обмануть меня, гулпец.')
                wie = 1
                return True
            guess = random.choice(list(self.guess_space))
            self.guess_space.remove(guess)
            if self.__is_compatible(guess):
                break
        print('-------------------------------------------------------------------')
        print('Мой черед')
        print('Я думаю это число...' + str(guess))
        cowsbulls = input('Введите через пробел количество коров и быков: ').split()
        while len(cowsbulls) != 2:
            cowsbulls = input('Введите через пробел количество коров и быков: ').split()
        cows, bulls = cowsbulls
        cows, bulls = int(cows), int(bulls)
        self.historys.append((guess, int(bulls), int(cows)))
        print("Попытка {}. Мое число {}. У меня {} коров(а) "
              "и {} бык(ов)".format(
                self.attempt, guess, cows, bulls))
        if bulls == 4:
            print("Победил... я")
            wie = 1
            return True
        if bulls >= 2 or cows >= 3 or bulls + cows == 4:
            print('Муахахах я уже так близок... Бойся меня!')
        return False

    def bulls_n_cows(self, a, b):
        bulls = sum(1 for x, y in zip(a, b) if x == y)
        cows = len(set(a) & set(b)) - bulls
        return bulls, cows

    def __play(self):
        global wie
        wie = 0
        print('Кто ходит первый - кидаем бинарную монетку. У тебя выбор, 0 или 1.')
        c = int(input())
        a = random.choice((0, 1))
        if a == 0:
            print('Выпал... 0')
        else:
            print('Выпала... 1')
        if a == c:
            print('Ходит первым игрок')
        else:
            print('Я хожу первым.')
        while not wie:
            print(self.answer)
            if a == c:
                if not self.__player_try():
                    self.__player()
            else:
                if not self.__player():
                    self.__player_try()
        print('Игра окончена')

    def __player_try(self):
        global wie
        self.k += 1
        print('___________________________________________________________________')
        print('Пытайся, смертный.')
        print('Ты также можешь запросить список всех своих попыток и совпадений к ним.'
              ' Для этого введи "попытки"(можно без кавычек).')
        print('Введите четырёхзначное число c неповторяющимися цифрами: ')
        attempt = input()
        while attempt == 'попытки' or attempt == '"попытки"':
            master = tkinter.Tk()
            label = tkinter.Label(master, text='\n'.join(self.digitals), cursor='dot', font='Courier',
                                  height=2)
            label.pack()
            print('Для продолжения игры закрой список попыток. Оно открылось в новом окне.')
            master.mainloop()
            attempt = input('Введите четырёхзначное число c неповторяющимися цифрами: ')
        while len(set(list(attempt))) != 4 and attempt not in [str(d) for d in range(1000, 9999)]:
            attempt = input('Введите четырёхзначное число c неповторяющимися цифрами: ')
        bulls, cows = self.bulls_n_cows(attempt, self.answer)
        if bulls >= 2 or cows >= 3 or bulls + cows == 4:
            self.answer = self.cheat()
        bulls, cows = self.bulls_n_cows(attempt, self.answer)
        self.history.append([attempt, bulls, cows])
        writ = "Попытка {}. Твое число {}. У тебя {} коров(а) и {} бык(ов)".format(self.k, attempt, cows, bulls)
        print(writ)
        self.digitals.append(writ)
        if bulls == 4:
            print('Ты выиграл, смертный.')
            print('Напоследок, введи свое число')
            if int(input()) not in self.guess_space:
                print('Лжец. Ты обманывал меня. Победа присуждается мне.')
                wie = 1
                return True
            wie = 1
            print('За это открою секрет... я люблю ставить многоточие.')
            return True
        return False

    def generate_answer(self):
        n = [i for i in range(10)]
        number = []
        for _ in range(4):
            a = n.pop(random.choice(range(len(n))))
            number.append(str(a))
        return ''.join(number)

    def cheat(self):
        error = True
        new_answer = None
        while error:
            new_answer = self.generate_answer()
            if new_answer == self.answer:
                error = True
                break
            else:
                if self.history:
                    for i in self.history:
                        if self.bulls_n_cows(i[0], new_answer) != [i[1], i[2]]:
                            error = True
                            break
                        else:
                            error = False
                else:
                    error = False
        return new_answer


this = B_n_c_game()