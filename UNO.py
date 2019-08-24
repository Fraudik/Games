import tkinter


def main():
    global deck, order, players

    def game(autopass, show, table, deck, firstwin):
        winners = []
        win = False
        colour = 'черная'
        action = 1
        k = 0
        while not win:
            colour = table[0].split()[0]
            sign = table[0].split()[1]
            if len(table[0].split()) > 2:
                sign = table[0].split()[1] + table[0].split()[2]
            if len(order) == 1:
                print('\n'.join(winners))
                print('Проиграл игрок номер', str(order[0]))
                break
            print('Ход игрока ' + str(order[0]))
            for i in players:
                if str(i) == str(order[0]):
                    cur = i
                    break
            if show and not cur.bot:
                print('Карты игрока. Для продолжения закройте окно со списком карт.')
                label.config(text='|'.join(i.hand), cursor='dot', font='Courier', height=2)
                label.pack()
                master.mainloop()
            print('На столе лежит ' + str(table[0]).upper() + ' карта')
            if cur.bot:
                for i in cur.hand:
                    i = i.split()
                    pos = 0
                    isign = i[1]
                    if len(i) > 2:
                        isign = i[1] + i[2]
                    if colour == i[0] or isign == sign or colour == 'черная' or i[0] == 'черная':
                        pos = 1
                        print('Хожу')
                        table.insert(0, ' '.join(i))
                        del cur.hand[cur.hand.index(' '.join(i))]
                        if i[0] == 'черная':
                            colour = random.choice(['красная', 'синяя', 'желтая', 'зеленая'])
                        if isign == 'плюс2' or len(i) == 4 or isign == 'пропуск' \
                                or isign == 'наоборот':
                            action = 1
                            if isign == 'наоборот':
                                order.reverse()
                        break
                if pos == 0:
                    print('Не могу походить. Беру карту.')
                    take(cur)
                pos = 0
            elif table[0].split()[0] == 'черная':
                print('Текущий цвет -', colour)
            elif table[0].split()[1] == 'пропуск' and action == 1:
                action = 0
                pass
            elif table[0].split()[1] == 'наоборот' and action == 1:
                action = 0
            elif table[0].split()[1] == 'плюс' and table[0].split()[0] != 'черная' and action == 1:
                ctwo = 2
                if not autopass:
                    print('Желаете использовать свою плюс 2? Да/Нет')
                    print('Если желаете прсомотреть список карт, введите "карты".(можно без кавычек)')
                    answer = input()
                    while answer != 'Да' and answer != 'Нет':
                        if answer == "карты" or answer == '"карты"':
                            master = tkinter.Tk()
                            label = tkinter.Label(master, text='|'.join(cur.hand), cursor='dot', font='Courier',
                                                  height=2)
                            label.pack()
                            master.mainloop()
                        answer = input('Да/Нет: ')

                    if answer == 'Да':

                        def chplus2():
                            print('Укажите номер карты, слева направо. '
                                  'Если вы не желаете или не можете взять карту, укажите 0.'
                                  ' В этом случае вы возьмете', ctwo, 'карты.'
                                  '\nЕсли желаете прсомотреть список карт, введите "карты".'
                                  '(можно без кавычек).')
                            num = input()
                            while num not in [str(d) for d in range(len(cur.hand) + 1)]:
                                if num == "карты" or num == '"карты"':
                                    master = tkinter.Tk()
                                    label = tkinter.Label(master, text='|'.join(cur.hand), cursor='dot', font='Courier',
                                                          height=2)
                                    label.pack()
                                    master.mainloop()
                                num = input('Укажите номер карты: ')
                            return int(num) - 1

                        num = chplus2()
                        while 1:
                            if num == -1:
                                while ctwo != 0:
                                    take(cur)
                                    ctwo -= 1
                                action = 0
                                break
                            elif cur.hand[num].split()[1] != 'плюс' or cur.hand[num].split()[0] == 'черная':
                                print('Это карта не "плюс 2".')
                                num = chplus2()
                            else:
                                desk.insert(0, cur.hand[num])
                                del cur.hand[num]
                                ctwo += 2
                                break
                    elif answer == 'Нет':
                        while ctwo != 0:
                            take(cur)
                            ctwo -= 1
                        action = 0
                else:
                    for i in cur.hand:
                        s = False
                        i = i.split()
                        if len(i) == 3 and i[1] == 'плюс':

                            def chplus2():
                                print('Укажите номер карты, слева направо. '
                                      'Если вы не желаете или не можете взять карту, укажите 0.'
                                      ' В этом случае вы возьмете', ctwo, 'карты.'
                                      '\nЕсли желаете прсомотреть список карт, введите "карты".'
                                      '(можно без кавычек).')
                                num = input()
                                while num not in [str(d) for d in range(len(cur.hand) + 1)]:
                                    if num == "карты" or num == '"карты"':
                                        master = tkinter.Tk()
                                        label = tkinter.Label(master, text='|'.join(cur.hand), cursor='dot',
                                                              font='Courier',
                                                              height=2)
                                        label.pack()
                                        master.mainloop()
                                    num = input('Укажите номер карты: ')
                                return int(num) - 1

                            num = chplus2()
                            while 1:
                                if num == -1:
                                    while ctwo != 0:
                                        take(cur)
                                        ctwo -= 1
                                    action = 0
                                    break
                                elif cur.hand[num].split()[1] != 'плюс' or cur.hand[num].split()[0] == 'черная':
                                    print('Это карта не "плюс 2".')
                                    num = chplus2()
                                else:
                                    table.insert(0, cur.hand[num])
                                    del cur.hand[num]
                                    ctwo += 2
                                    break
                            s = True
                            break
                    if not s:
                        print('Вы берете', ctwo, 'карты.')
                        while ctwo != 0:
                            take(cur)
                            ctwo -= 1
                        action = 0
            elif table[0].split()[0] == 'черная' and table[0].split()[1] == 'плюс' and action == 1:
                    print('Вы берете 4 карты.')
                    ctwo = 4
                    while ctwo != 0:
                        take(cur)
                        ctwo -= 1
                    action = 0
            else:
                if autopass and not cur.bot:
                    for i in cur.hand:
                        i = i.split()
                        pos = 0
                        isign = i[1]
                        if len(i) > 2:
                            isign = i[1] + i[2]
                        if colour == i[0] or isign == sign or colour == 'черная' or i[0] == 'черная':
                            pos = 1
                            print('Вы можете походить.')
                            break
                    if not pos:
                        print('Вы не можете походить. Вы берете карту.')
                        take(cur)
                if pos or not autopass:
                    print('Укажите номер карты, слева направо. '
                          'Если вы не желаете или не можете взять карту, укажите 0.'
                          '\nЕсли желаете прсомотреть список карт, введите "карты".'
                          '(можно без кавычек).')
                    num = input('Укажите номер карты: ')
                    while num not in [str(d) for d in range(len(cur.hand) + 1)]:
                        if num == "карты" or num == '"карты"':
                            master = tkinter.Tk()
                            label = tkinter.Label(master, text='|'.join(cur.hand), cursor='dot', font='Courier',
                                                  height=2)
                            label.pack()
                            master.mainloop()
                        num = input('Укажите номер карты: ')
                    num = int(num) - 1
                    while 1:
                        if num == -1:
                            take(cur)
                            break
                        i = cur.hand[num].split()
                        isign = i[1]
                        if len(i) > 2:
                            isign = i[1] + i[2]
                        if colour != i[0] and isign != sign and colour != 'черная' and i[0] != 'черная':
                            print('Вы не можете походить этой картой')
                            num = input('Введите номер: ')
                            while num not in [str(d) for d in range(len(cur.hand) + 1)]:
                                if num == "карты" or num == '"карты"':
                                    master = tkinter.Tk()
                                    label = tkinter.Label(master, text='|'.join(cur.hand), cursor='dot', font='Courier',
                                                          height=2)
                                    label.pack()
                                    master.mainloop()
                                num = input('Введите номер: ')
                            num = int(num) - 1
                        else:
                            table.insert(0, ' '.join(i))
                            del cur.hand[num]
                            if i[0] == 'черная':
                                print('Выберите цвет.')
                                colour = input('красная/синяя/зеленая/желтая: ')
                                if colour not in ('красная', 'синяя', 'желтая', 'зеленая'):
                                    colour = input('красная/синяя/зеленая/желтая: ')
                            if isign == 'плюс2' or len(i) == 4 or isign == 'пропуск' \
                                    or isign == 'наоборот':
                                action = 1
                                if isign == 'наоборот':
                                    order.reverse()
                            break
            if len(cur.hand) == 1:
                print('UNO')
            elif len(cur.hand) == 0 and not firstwin:
                win = True
                print('Победил игрок номер ', str(order[0]))
            elif len(cur.hand) == 0 and firstwin:
                k += 1
                print('Игрок номер', str(order[0]), 'вышел из игры')
                winners.append(str(str(k) + ' Игрок номер ' + str(order[0]) + ' вышел из игры'))
                del order[0]
            if len(deck) < 10:
                deck += table
                table = table[:1]
                random.shuffle(deck)
            order.append(order[0])
            del order[0]

    import random
    random.seed(random.randint(13752425264, 253532253678358))
    colo = {1: 'красная', 2: 'желтая', 3: 'зеленая', 4: 'синяя'}
    spec = {10: 'пропуск', 11: 'наоборот', 12: 'плюс 2'}
    deck = ['черная смена цвета', 'черная смена цвета', 'черная смена цвета', 'черная смена цвета',
            'черная плюс 4 и смена цвета', 'черная плюс 4 и смена цвета', 'черная плюс 4 и смена цвета',
            'черная плюс 4 и смена цвета']
    for i in range(1, 5):
        for j in range(13):
            if j < 10:
                deck.append(colo[i] + ' ' + str(j))
                if j != 0:
                    deck.append(colo[i] + ' ' + str(j))
            else:
                deck.append(colo[i] + ' ' + spec[j])
                deck.append(colo[i] + ' ' + spec[j])
    random.shuffle(deck)

    def take(who):
        if type(who) == Player:
            who += deck[0]
            del deck[0]
        else:
            who.append(deck[0])
            del deck[0]

    class Player:
        def __init__(self, num):
            self.hand = []
            self.number = str(num)
            self.bot = False

        def __str__(self):
            return self.number

        def __add__(self, other):
            self.hand.append(other)

        def __getitem__(self, item):
            return self.hand[item]

        def __delitem__(self, key):
            del self.hand[key]

    p1 = Player(1)
    p2 = Player(2)
    p3 = Player(3)
    p4 = Player(4)
    p5 = Player(5)
    p6 = Player(6)
    p7 = Player(7)
    p8 = Player(8)
    players = [p1, p2, p3, p4, p5, p6, p7, p8]
    print('Вопрос по механизму игры - если у человека нет карты, которую он может сыграть'
          'его ход автоматически пропускается (со всеми соответствующими штрафами) или он делает это сам?\n'
          '(второй вариант создан для возможности сохранить на будущее какую-то карту,'
          ' не выдавая у себя ее наличие.(бесполезно для новчиков). Более долгая игра.)')
    answer = input('1/2: ')
    while answer not in ('1', '2'):
        answer = input('1/2: ')
    autopass = bool((int(answer) * -1) + 2)
    print('Еще один вопрос. Показывать ли в начале хода карты игрока автоматически?'
          'Вы можете посмотреть их вручную, введя "карты" (можно без кавычек)')
    answer = input('Да/Нет: ')
    while answer not in ('Да', "Нет"):
        answer = input('Да/Нет: ')
    if answer == 'Да':
        show = 1
    else:
        show = 0
    print('Играем до последнего оставшегося(1) или первого выигрывшего(2)?')
    answer = input('1/2: ')
    while answer not in ('1', '2'):
        answer = input('1/2: ')
    firstwin = bool((int(answer) * -1) + 2)
    print('Сколько человек играет? 2/3/4/5/6/7/8')
    n = input()
    while n not in ('2', '3', '4', '5', '6', '7', '8'):
        print('Сколько человек играет? 2/3/4/5/6/7/8')
        print('Введите одну цифру из перечисленных')
        n = input()
    print('А сколько из них ботов?')
    p = input()
    while n not in ('2', '3', '4', '5', '6', '7', '8'):
        print('А сколько из них ботов?')
        print('Введите одну цифру из перечисленных ранее, не больше числа игроков')
        p = input()
    print('Сколько карт у каждого игрока? 4/5/6/7')
    q = input()
    while q not in ('2', '3', '4', '5', '6', '7'):
        print('Сколько карт у каждого игрока? 4/5/6/7')
        q = input()
    q = int(q)
    n = int(n)
    p = int(p)
    order = []
    for _ in range(q):
        for i in players[:n]:
            take(i)
    for i in range(1, n + 1):
        order.append(i)
    for i in players[::-1]:
        if int(i.number) in order and p > 0:
            p -= 1
            i.bot = True
    table = []
    take(table)
    game(autopass, show, table, deck, firstwin)


main()

#на данный момент не сделана механика с цветом - какой цвет текущий, но это реализуется только при реализации самой игры
#пока готовы только условия. дальше, правила игры. возможность введения доп. передавая в виде параметра в функции gane()
#
