# Лабораторная работа №4 - Вариант 17
# Классы для истории перемещений офисных работников
# ИЗМЕНЕНИЕ В ОРИГИНАЛЕ - версия 1

import csv  # ИЗМЕНЕНИЕ ИЗ КОПИИ
import os
from datetime import datetime

class OfficeRecord:
    """Класс для хранения одной записи о перемещении"""
    
    def __init__(self, record_id, datetime_str, is_workplace, room_number):
        # Используем __setattr__ для установки свойств
        self.__setattr__('_id', record_id)
        self.__setattr__('_datetime', datetime_str)
        self.__setattr__('_is_workplace', is_workplace)
        self.__setattr__('_room_number', room_number)
    
    @property
    def id(self):
        return self._id
    
    @property
    def datetime(self):
        return self._datetime
    
    @property
    def is_workplace(self):
        return self._is_workplace
    
    @property
    def room_number(self):
        return self._room_number
    
    def __setattr__(self, name, value):
        """Перегрузка __setattr__ - запись только через этот метод"""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Прямая запись в {name} запрещена. Используйте методы класса.")
    
    def __repr__(self):
        return (f"OfficeRecord(id={self._id}, datetime='{self._datetime}', "
                f"is_workplace={self._is_workplace}, room={self._room_number})")
    
    def __str__(self):
        workplace = "Да" if self._is_workplace else "Нет"
        return f"{self._id:<4} {self._datetime:<20} {workplace:<18} {self._room_number:<15}"


class BaseHistory:
    """Базовый класс - для наследования"""
    
    def __init__(self):
        self._records = []
    
    def add_record(self, record):
        self._records.append(record)
    
    def __len__(self):
        return len(self._records)
    
    def __getitem__(self, index):
        """Доступ по индексу"""
        return self._records[index]
    
    def __iter__(self):
        """Итератор"""
        return OfficeIterator(self._records)
    
    def get_all_records(self):
        return self._records
    
    @staticmethod
    def validate_datetime(datetime_str):
        """Статический метод проверки даты"""
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False


class OfficeHistory(BaseHistory):
    """Основной класс для работы с историей офисных работников"""
    
    def get_sorted_by_datetime(self):
        """Сортировка по дате (строковое поле)"""
        return sorted(self._records, key=lambda x: x.datetime)
    
    def get_sorted_by_room(self):
        """Сортировка по номеру комнаты (числовое поле)"""
        return sorted(self._records, key=lambda x: x.room_number)
    
    def filter_by_workplace(self):
        """Фильтрация: только на рабочем месте"""
        return [record for record in self._records if record.is_workplace == True]
    
    def generate_car_info(self):
        """Генератор информации о перемещениях"""
        for record in self._records:
            status = "на рабочем месте" if record.is_workplace else "покинул рабочее место"
            yield f"Запись #{record.id}: {record.datetime} - {status}, комната {record.room_number}"
    
    def print_info(self, records=None, title="Данные"):
        """Вывод информации на экран"""
        if records is None:
            records = self._records
        
        if not records:
            print("Нет данных для отображения.")
            return
        
        print(f'\n{title}\n')
        print(f"{'ID':<4} {'Дата и время':<20} {'На рабочем месте':<18} {'Номер комнаты':<15}")
        print("-" * 65)
        
        for record in records:
            print(record)
    
    @staticmethod
    def load_file(filename):
        """Статический метод загрузки из файла"""
        history = OfficeHistory()
        
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            return history
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    is_workplace = row['is_workplace'].lower() in ('true', '1', 'yes')
                    record = OfficeRecord(
                        record_id=int(row['id']),
                        datetime_str=row['datetime'],
                        is_workplace=is_workplace,
                        room_number=int(row['room_number'])
                    )
                    history.add_record(record)
            print(f"Загружено {len(history)} записей из файла {filename}")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
        
        return history
    
    @staticmethod
    def save_file(history, filename='data.csv'):
        """Статический метод сохранения в файл"""
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'datetime', 'is_workplace', 'room_number']
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                for record in history.get_all_records():
                    writer.writerow({
                        'id': record.id,
                        'datetime': record.datetime,
                        'is_workplace': str(record.is_workplace),
                        'room_number': record.room_number
                    })
            print(f"Данные успешно сохранены в файл {filename}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


class OfficeIterator:
    """Класс итератора для перебора записей"""
    
    def __init__(self, records):
        self._records = records
        self._index = 0
    
    def __next__(self):
        if self._index < len(self._records):
            result = self._records[self._index]
            self._index += 1
            return result
        raise StopIteration
    
    def __iter__(self):
        return self
# Новая функция для офисных работников
# ИЗМЕНЕНИЕ ИЗ КОПИИ - версия 2