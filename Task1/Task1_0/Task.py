'''
Создайте программу для игры в ""Крестики-нолики"" при помощи виртуального окружения и PIP
'''

import emoji


array = [['1' ,'|', '2' ,'|', '3'], ['-','-','-','-','-'],['4' ,'|', '5' ,'|', '6'], ['-','-','-','-','-'],['7' ,'|', '8' ,'|', '9'] ]
player1 = emoji.emojize(":hollow_red_circle:")
player2 = emoji.emojize(":cross_mark:")

def print_desk():
    for i in array: 
        print(' '.join(list(map(str, i))))

def motion(player):
    number = str(input(f'Введите число, на которое нужно поставить {player}: '))
    flag = False
    for i in range(len(array)):
        for k in range(len(array)):
            if array[i][k] == number:
                array[i][k] = player
                flag = True
    print_desk()
    return flag


def itogi():
    if array[0][0] == array[0][2] == array[0][4] or array[2][0] == array[2][2] == array[2][4] or array[4][0] == array[4][2] == array[4][4] or array[0][0] == array[2][0] == array[4][0] or array[0][2] == array[2][2] == array[4][2] or array[0][4] == array[2][4] == array[4][4] or array[0][0] == array[2][2] == array[4][4] or array[0][4] == array[2][2] == array[4][0]:
        return False
    else:
        return True


def draw():
    flag = False
    for i in range(len(array)):
        for k in range(len(array)):
            if array[i][k] in ["1","2","3","4","5","6","7","8","9"]:
                flag = True
    return flag


print_desk() 

current_player = player1
while itogi() and draw():
    if motion(current_player):
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
    else:
        print(f'Неверное число, игрок {current_player} вводит число заново')

if not draw() and itogi():
    print('Ничья - игра окончена')
elif current_player == player1:
    print("Победил игрок", player2)
else:
    print("Победил игрок", player1)