# Лабораторная работа №4 - Вариант 17
# Версия 2 - обновление от 10.04.2026
# Главный файл программы

from office_history import OfficeRecord, OfficeHistory, OfficeIterator

def create_example_file():
    """Создание примера файла data.csv"""
    import os
    if not os.path.exists('data.csv'):
        history = OfficeHistory()
        examples = [
            OfficeRecord(1, '2024-01-15 08:00:00', True, 101),
            OfficeRecord(2, '2024-01-15 09:30:00', False, 203),
            OfficeRecord(3, '2024-01-15 10:15:00', True, 101),
            OfficeRecord(4, '2024-01-15 12:00:00', False, 305),
            OfficeRecord(5, '2024-01-15 14:30:00', True, 101),
        ]
        for rec in examples:
            history.add_record(rec)
        OfficeHistory.save_file(history)
        print("Создан пример файла data.csv")

def main():
    print("Лабораторная работа №4 - Вариант 17")
    print("История перемещений офисных работников\n")
    
    create_example_file()
    history = OfficeHistory.load_file('data.csv')
    
    if len(history) == 0:
        print("Нет данных для работы.")
        return
    
    while True:
        print("\n" + "="*55)
        print("1. Показать все данные")
        print("2. Сортировка по дате и времени (строковое поле)")
        print("3. Сортировка по номеру комнаты (числовое поле)")
        print("4. Фильтрация (только на рабочем месте)")
        print("5. Добавить новую запись")
        print("6. Сохранить данные в файл")
        print("7. Доступ по индексу (__getitem__)")
        print("8. Итерация по записям (итератор)")
        print("9. Генератор информации о перемещениях")
        print("0. Выход")
        print("="*55)
        
        choice = input("\nВыберите опцию: ")
        
        if choice == '1':
            history.print_info()
        
        elif choice == '2':
            sorted_records = history.get_sorted_by_datetime()
            history.print_info(records=sorted_records, title="Сортировка по дате и времени")
        
        elif choice == '3':
            sorted_records = history.get_sorted_by_room()
            history.print_info(records=sorted_records, title="Сортировка по номеру комнаты")
        
        elif choice == '4':
            filtered = history.filter_by_workplace()
            history.print_info(records=filtered, title="Фильтрация: сотрудники на рабочем месте")
        
        elif choice == '5':
            print("\nФормат даты и времени: ГГГГ-ММ-ДД ЧЧ:ММ:СС")
            datetime_str = input("Дата и время: ")
            
            if not OfficeHistory.validate_datetime(datetime_str):
                print("Ошибка: Неверный формат даты/времени")
                continue
            
            workplace_input = input("На рабочем месте? (да/нет): ").lower()
            is_workplace = workplace_input in ('да', 'yes', 'true', '1')
            
            try:
                room_number = int(input("Номер комнаты: "))
                if room_number < 0:
                    print("Ошибка. Номер комнаты не может быть отрицательным")
                    continue
                
                new_id = len(history) + 1
                new_record = OfficeRecord(new_id, datetime_str, is_workplace, room_number)
                history.add_record(new_record)
                print(f"Запись #{new_id} успешно добавлена")
            except ValueError:
                print("Ошибка. Введите корректное число")
        
        elif choice == '6':
            OfficeHistory.save_file(history)
        
        elif choice == '7':
            try:
                print(f"\nВсего записей: {len(history)}")
                index = int(input(f"Введите индекс (0-{len(history)-1}): "))
                print(f"\nЗапись по индексу {index}:")
                print(history[index])
            except IndexError:
                print("Ошибка: Индекс вне диапазона")
            except ValueError:
                print("Ошибка: Введите целое число")
        
        elif choice == '8':
            print("\nИтерация по записям:")
            for record in history:
                print(record)
        
        elif choice == '9':
            print("\nГенератор информации о перемещениях:")
            for line in history.generate_car_info():
                print(f"  {line}")
        
        elif choice == '0':
            print("До свидания!")
            break
        
        else:
            print("Такой опции нет. Введите 0-9.")

if __name__ == "__main__":
    main()