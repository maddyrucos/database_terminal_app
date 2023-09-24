'''
Модуль для создания столбца.
Позволяет выбрать параметры для создания столбца (на данный момент реализовано только
добавление PRIMARY KEY, AUTOINCREMENT и выбор типа данных).
Передает строковые значения в вызывающую переменную. 
'''
def add_column():
        
        type_of_column = int(input('Выберите тип данных столбца: \n'
                                   '\t1. Text\n'
                                   '\t2. Integer\n'
                                   '\t3. Real\n'
                                   '\t4. Time\n'))

        add_autoincrement = ''

        if type_of_column == 1:
            type_of_column = 'TEXT'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        elif type_of_column == 2:
            type_of_column = 'INTEGER'
            print(f'\nВыставлен тип данных {type_of_column}\n')
            add_autoincrement = int(input('Добавить автоматическое заполнение?\n1. Да\n2. Нет\n'))

            if add_autoincrement == 1:
                add_autoincrement = ' AUTOINCREMENT'
                print('Добавлено автоматическое заполнение.\n')

            elif add_autoincrement == 2:
                add_autoincrement = ''
                print('Автоматическое заполнение отключено.\n')

            else:
                add_autoincrement = ''
                print('Введено неправильное значение. Автомтическое заполнение отключено.\n')

        elif type_of_column == 3:
            type_of_column = 'REAL'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        elif type_of_column == 4:
            type_of_column = 'TIME'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        else:
            print('Неизвестный формат!')
            type_of_column = 'TEXT'


        return type_of_column, add_autoincrement


if __name__ == '__main__':
    print('Hello world!')

