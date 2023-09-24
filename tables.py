from edittable import edit_table
from addcolumn import add_column

''' 
Функция, запускаемая из главного модуля (db_app)

Получает следующие принимаемые аргументы:
    1. db - подключенная база данных
    2. cur - курсор в подключенной базе данных

Включает в себя следующие функции:
    1. show_tables() - Функция, которая выводит список имеющихся в БД таблиц.
                       Не принимает аргументы.
                                             
    2. add_table() - Функция, которая позволяет добавить таблицу.
                     Не принимает аргументы.

    3. remove_table() - Функция, позволяющая удалять таблицы.
                        Не принимает аругменты
'''
def work_with_tables(db, cur):
    

    def add_table():

        # Пользователь вводит название новой таблицы
        name_of_new_table = input('\nВведите название новой таблицы: ')

        # Пользователь вводит название главного столбца (primary)
        name_of_key_row = input('\nВведите название основного столбца: ')        

        # Вызов функции добавления столбца. Аргументы не передаются.
        # Полученные данные (данные для формирования запроса) передаются в переменную
        key_column = add_column()

        # Переопределение данных в переменные
        type_of_column = key_column[0]
        add_autoincrement = key_column[1]

        # Создание новой таблицы с полученными значениями. 
        # В случае существования таблицы с таким названием, пользователю будет выведено сообщение
        try:

            cur.execute(f'''CREATE TABLE {name_of_new_table} ({name_of_key_row} {type_of_column} PRIMARY KEY{add_autoincrement})''')
            db.commit()
            print('\nТаблица успешно создана!\n')
            show_tables(db, cur)

        except:

            print('Такая таблица уже существует!')


    def remove_table():
        
        # Вызов функции отображения всех таблиц
        show_tables(db, cur)

        # Получение от пользователя названия таблицы для удаления
        name_of_table = input('Введите название таблицы для удаления: ')
        
        # Проверка на наличие таблицы, в случае отсуствия таблицы с введенным названием, появится предупреждение
        try:

            cur.execute(f'DROP TABLE "{name_of_table}"')
            db.commit()
        except:

            print('Такой таблицы не существует!')
        
        # Вызов функции отображения всех таблиц
        show_tables(db, cur)


    # Создание переменной действия
    action = True

    while action != 0:

        # Введенное пользователем значение переводится в целочисленное. Иные значения засчитаны не будут.
        try:
            action = int(input('\nВыберите действие:\n'
                               '\t1. Список таблиц\n'
                               '\t2. Добавить таблицу\n'
                               '\t3. Удалить таблицу\n'
                               '\t4. Редактировать таблицу\n'
                               '\t0. Назад\n'))
        
        except:
            print('Неверное значение!')
        
        # При вводе пользователем цифры 1, запускается функция show_tables, отображающая список таблиц
        if action == 1:
            show_tables(db, cur)
        
        # При вводе пользователем цифры 2, запускается функция add_table, позволяющая добавить таблицу
        if action == 2:
            add_table()
        
        # При вводе пользователем цифры 3, запускается функция remove_table, позволяющая удалить таблицу
        if action == 3:
            remove_table()
        
        # При вводе пользователем цифры 4, отображается список таблиц 
        # Затем запрашивается номер таблицы из списка для редактирования
        # Введенное число передается в модуль edit_table, позволяющий редактировать таблицу
        if action == 4:
            tables = show_tables(db, cur)
            
            #try:
            number_of_table = int(input('Введите номер таблицы: '))
            name_of_table = tables[number_of_table-1][1]
            edit_table(db, cur, name_of_table)

            #except:
                #print('Введено неверное значение!')


def show_tables(db, cur):

        print('\n № |\tНазвание\t|\tЗапрос')
        
        # При помощи курсора делает запрос к БД, в частности к sqlite_master
        # Тип данных "таблица" (type = "table")
        tables = cur.execute(f'SELECT * FROM sqlite_master WHERE type ="table"').fetchall() 
        
        # Вывод названия и запроса каждой таблицы
        for index, table in enumerate(tables): #2
            table_name = table[1]
            table_request = table[4]
            table_number = index+1
            
            if len(table_name) < 4:
                table_name += '\t\t'
            
            elif len(table_name) < 12:
                table_name +='\t'
            
            print(f' {table_number} |  {table_name}\t|  {table_request}')

        return tables


if __name__ == '__main__':
    print('Hello world!')