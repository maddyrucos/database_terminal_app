from addcolumn import add_column as add_col

def edit_table(db, cur, name_of_table):


    '''
    def remove_column():
        name_of_column = input('\nВведите название столбца: ')
        cur.execute(f'ALTER TABLE {name_of_table} DROP COLUMN "{name_of_column}"')
        db.commit()
    '''

    # Функция создания нового столбца
    def add_column():
        
        # Получение названия столбца и передача в функцию создания
        name_of_new_column = input('Введите название нового столбца: ')
        new_column = add_col()

        cur.execute(f'ALTER TABLE {name_of_table} ADD COLUMN {name_of_new_column} {new_column[0]}{new_column[1]}')
        db.commit()
        print('Столбец успешно добавлен!\n')

    # Функция отображения столбцов
    def show_columns():
        
        # Из sqlite_master берется информация о выбранной таблице
        table_info = cur.execute(f'SELECT * FROM sqlite_master WHERE "name" = "{name_of_table}"').fetchone()
        
        # Форматирование полученной информации
        not_formated_columns = table_info[4].split('(')
        not_formated_columns = not_formated_columns[1].split(')')
        formated_columns = not_formated_columns[0].split(',')
        
        # Вывод пронумерованного списка стобцов с запросами
        for index, column in enumerate(formated_columns):
            name_of_column, request_of_column = column.split()[0], column.split()[1]
            print(f' {index+1}. {name_of_column}: {request_of_column}')
    

    action = True

    while action != False:

        action = int(input('\nВыберите действие:\n'
                           '\t1. Добавить столбец\n'
                           '\t2. Удалить столбец\n'
                           '\t3. Показать столбцы\n'
                           '\t0. Назад\n'))

        if action == 1:
            add_column()

        if action == 2:
            remove_column()

        if action == 3:
            show_columns()

        if action == 0:
            action = False





