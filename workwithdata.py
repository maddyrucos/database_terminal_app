from tables import show_tables
import sqlite3

''' 
Функция, запускаемая из главного модуля (db_app)

Получает следующие принимаемые аргументы:
    1. db - подключенная база данных
    2. cur - курсор в подключенной базе данных

Включает в себя следующие функции:
    1. choose_table() - Функция, которая позволяет переключаться между имеющимися в БД таблицами.
                        Не принимает аргументы.
                                             
    2. add_row() - Функция, которая позволяет добавить запись (строку).
                   Аргументов не принимает.

    3. remove_row() - Функция, которая позволяет удалить запись (строку).
                      Аргументов не принимает.

    4. edit_row() - Функция, которая позволяет отредактировать запись (строку).
                    Аргументов не принимает.

    5. show_single_row() - Функция, которая полностью отображает данные одной конкретной записи (строки).
                           Требует аргумент key_value - значение ключевого столбца в строке.

    6. show_all_rows() - Функция, которая отображает все записи (строки) в таблице. Записи ограничены в 20 символов.
                         Аргументов не принимает.

    7. get_key_column() - Функция, которая передает название ключевого столбца в таблице.
                          Аргументов не принимает.

    8. get_key_value() - Функция, которая передает значение в ключевом столбце.
                         Аргументов не принимает.

    9. get_list_of_columns() - Функция, которая передает список стобцов в таблице.
                               Аргументов не принимает.
                                                    
'''
def work_with_data(db, cur):

    def choose_table():
        
        # Отобажение пронумерованного списка всех таблиц
        tables = show_tables(db, cur)
        
        # Получения значения номера таблицы, принимается только целочисленное значение
        # Если пользователь введет не целочисленное значение, сработает исключение
        try:          
            active_table = int(input('\nВведите номер таблицы: '))
        
        except:
            print('Введено неверное значение!')

        # 0 является значением для выхода, поэтому условие ограничено неравенством с нулем 
        # Также, значение должно быть только положительным
        if active_table != 0 and active_table > 0:

            # Из введенного пользователем номера вычитается 1, т.к. список значений нумеруется с нуля,
            # А выведенный пользователю список пронумерован с 1
            active_table = tables[active_table-1][1]
            
            return active_table

        # Если значение не соответствует условию, то ничего не происходит
        else:
            pass
            

    def add_row():
        
        # Получение списка столбцов в активной таблице
        list_of_columns = get_list_of_columns()
        # Получение названия ключевого столбца в активной таблице
        key_column = get_key_column()
        # Получение значения ключевого столбца
        key_value = get_key_value()

        # Запись новой строки с отслеживанием возможных ошибок
        try:
            # Внесение в активную таблицу () в ключевой столбец (key_column) введенного пользователем значения (key_value)
            cur.execute(f'INSERT INTO {active_table}("{key_column}") VALUES("{key_value}")')
            db.commit()

        # В случае, если такое значение первичного ключа уже существует, сработает данное исключение. Строка добавлена не будет
        # Работа функции будет завершена
        except sqlite3.IntegrityError:
            print('Запись с таким первичным ключом уже существует!')
            
            return

        # В случае других возможных ошибок сработает данное исключение. Строка добавлена не будет
        # Работа функции будет завершена
        except sqlite3.OperationalError:
            print("Не удалось ввести значение!")
            
            return
 
        # Если строка была успешно создана, запустится процесс её заполнения, в случае если количество столбцов > 1
        if len(list_of_columns)>1:
            
            # Заполнение будет происходить без учета ключевого столбца
            for i in range(1, len(list_of_columns)):
                
                # Для каждого столбца будет запрашиваться значение
                column_name = list_of_columns[i][1]
                new_value = input(f'\nВведите значение для столбца "{column_name}": ')

                # Обновление таблицы, при котором вносятся введенные значения
                cur.execute(f'UPDATE {active_table} SET "{column_name}"="{new_value}" WHERE "{key_column}" == "{key_value}"')
                db.commit()
        
        print('\nЗапись успешно добавлена!\n')


    def remove_row():

        # Отобажение списка всех строк
        show_all_rows()  

        # Получение названия ключевого столбца в активной таблице
        key_column = get_key_column()
        # Получение значения ключевого столбца
        key_value = get_key_value()

        # Удаление происходит с отслеживанием каких-либо ошибок
        try:
            # Удаление из активной таблицы () строки, 
            # В которой ключевое значение (key_column) соответствует введенному пользователем (key_value)
            cur.execute(f'DELETE FROM {active_table} WHERE "{key_column}" = "{key_value}"')
            db.commit()
            print('Запись удалена!')

        # Исключение, которое сработает на любую ошибку
        except:
            print('Возникла ошибка!')


    def edit_row():
        
        # Отобажение списка всех строк
        show_all_rows()

        # Получение списка столбцов в активной таблице
        list_of_columns = get_list_of_columns()
        # Получение названия ключевого столбца в активной таблице
        key_column = get_key_column()
        # Получение значения ключевого столбца
        key_value = get_key_value()

        # Полный вывод строки, которую необходимо отредактировать
        # Столбцы пронумерованы
        show_single_row(key_value)

        # Попытка редактирования строки в отслеживанием каких-либо ошибок
        try:
            # Получение номера столбца, который необходимо отредактировать
            column_to_edit = int(input('Введи номер столбца, который необходимо отредактировать: '))
            # Получение значения, которое будет внесено в выбранный ранее столбец
            new_value = input('Введите новое значение: ')
            
            ''' 
            Обновление таблицы, при котором в строке, у которой значение из ключевого столбца(key_column) равно введенному пользователем (key_value)
            Будет изменен столбец, номер которого (column_to_edit) был выбран пользователем.
            Номер (column_to_edit), уменьшенный на 1 (из-за разной нумерации) является индексом для списка столбцов (list_of_columns)
            '''
            cur.execute(f'UPDATE {active_table} SET "{list_of_columns[column_to_edit-1][1]}" = "{new_value}" WHERE "{key_column}" = "{key_value}"')
            db.commit()
            print('Значение успешно изменено!')
            
            # Полный вывод отредактированной строки
            show_single_row(key_value)

        except:
            print('Введено неверное значение')


    def show_single_row(key_value):
        
        # Получение списка столбцов в активной таблице
        list_of_columns = get_list_of_columns()
        # Получение названия ключевого столбца в активной таблице
        key_column = get_key_column()
        # Получение всех значений из строки, значение ключевого столбца (key_column) соответствует введенному пользователем (key_value)
        list_of_values = cur.execute(f'SELECT * FROM {active_table} WHERE "{key_column}" == "{key_value}"').fetchone()
        # Вывод списка с отслеживанием ошибок
        try: 
            # Выводится пронумерованный список, отсчет начинается с 1 
            for i in range(len(list_of_values)):
                # Вывод в формате: <Номер>. <Название строки>: <Содержимое строки>
                print(f'\n{i+1}. {list_of_columns[i][1]}: {list_of_values[i]}\n')

        except:
            print('Возникла ошибка!')



    def show_all_rows():
        
        # Вывод название активной таблицы
        print(f'\nТаблица: {active_table}\n')

        # Получения списка всех значений из активной таблицы
        all_rows = cur.execute(f'SELECT * FROM {active_table}').fetchall()
        list_of_columns = get_list_of_columns()
        
        # Функция форматирования вывода таблицы
        def make_formatting(column):
            if len(str(column)) > 23: 
                    column = str(column)[:20]+'...'
            elif 23 == len(str(column)):
                    column = str(column) + ''
            elif 23 > len(str(column)) >= 15:
                    column = str(column) + '\t'
            elif 15 > len(str(column)) >= 7:
                    column = str(column) + '\t\t'
            elif 7 > len(str(column)) >= 4:
                    column = str(column) + '\t\t\t'
            elif 4 > len(str(column)) >=1:
                    column = str(column) + '\t\t\t'
            elif len(str(column)) == 0:
                    column = str(column)+ '\t\t\t\t'

            print(f'{column}', end = '|')

        # Для каждого столбца из списка столбцов (list_of_columns) производится форматирование и вывод
        for column in list_of_columns:
            make_formatting(column[1])         

        # Для каждой строки из списка всех строк (all_rows) производится форматирование и вывод
        for row in all_rows:
            print('\n')
            for column in row:
                make_formatting(column)
        
        print('\n')


    def get_key_column():
        # Получения списка всех столбцов
        list_of_columns = get_list_of_columns()
        # Название ключевого столбца является первое значение (название) из нулевого элемента списка (информация о ключевом столбце)
        key_column = list_of_columns[0][1]
     
        return key_column


    def get_key_value():
        # Получение названия ключевого столбца
        key_column = get_key_column()
        # Получение значения для ключевого столбца
        key_value = input(f'Введите "{key_column}" нужной записи: ')

        return key_value


    def get_list_of_columns():
        # Получение списка столбцов активной таблицы
        list_of_columns = list(cur.execute(f'PRAGMA table_info({active_table})').fetchall())
        
        return list_of_columns


    # Переменная, в которой хранится название активной таблицы
    active_table = choose_table()
    # Переменная действия
    action = True

    # Цикл работает, пока значение переменной действия (action) не равно 0
    while action != False:

        # У пользователя запрашивается номер пункта, который является целым числом
        try:
            action = int(input(f'\nТекущая таблица - {active_table}\n'
                               'Выберите действие:\n'
                               '\t1. Добавить запись\n'
                               '\t2. Удалить запись\n'
                               '\t3. Изменить запись\n'
                               '\t4. Показать одну запись\n'
                               '\t5. Показать все записи\n'
                               '\t6. Сменить таблицу\n'
                               '\t0. Назад\n'))

        # Если пользователь введет не целое число, сработает исключение и цикл сработает заново
        except:
            print('Введено неверное значение!')


        if action == 1:
            add_row()
        
        elif action == 2:
            remove_row()

        elif action == 3:
            edit_row()

        elif action == 4:
            show_all_rows()
            key_value = get_key_value()
            show_single_row(key_value)

        elif action == 5:
            show_all_rows()

        elif action == 6:
            active_table = choose_table()

        elif action == 0:
            pass