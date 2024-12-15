from typing import List, Dict, Optional
import pandas as pd


# Ожидаемая последовательность событий
EXPECTED_SEQUENCE = [
    {15},  # Выбор программы
    {1},   # Завершение преднагрева
    {20, 21},  # Статусы открытия/закрытия дверей
    {16},  # Начало выпекания
    {17, 18, 8}  # Завершение выпекания или прерывание
]

class BakingState:
    """
    Класс для работы с состоянием выпекания.
    """
    def __init__(self):
        self.state = 0
        self.start_time: Optional[pd.Timestamp] = None
        self.end_time: Optional[pd.Timestamp] = None
        self.program: Optional[int] = None
        self.oven_number: Optional[int] = None

    def process_event(self, event_id: int, event_time: pd.Timestamp, program: int, oven_number: int) -> bool:
        """
        Обрабатывает событие и проверяет, соответствует ли оно ожидаемой последовательности.
        """
        if self.state >= len(EXPECTED_SEQUENCE):
            return False

        # Получаем ожидаемые события для текущего состояния
        expected_events = EXPECTED_SEQUENCE[self.state]

        # Проверяем, соответствует ли текущее событие ожидаемым
        if event_id in expected_events:
            if self.state == 0:
                self.program = program
                self.oven_number = oven_number
            elif self.state == 2 and event_id == 20:
                # открытие двери
                return
            elif self.state == 3:
                # Время старта выпекания
                self.start_time = event_time
            elif self.state == 4:
                # Время завершения выпекания
                self.end_time = event_time
                return True
            self.state += 1

        else:
            # Cбрасываем состояние
            self.reset()
        return False

    def reset(self):
        """
        Сбрасывает состояние.
        """
        self.state = 0
        self.start_time = None
        self.end_time = None
        self.program = None
        self.oven_number = None


def process_group(group: pd.DataFrame) -> List[Dict]:
    """
    Обрабатывает группу событий и возвращает результаты выпекания.
    """
    state = BakingState()
    results = []

    for _, row in group.iterrows():
        event_id = row['ID события']
        event_time = row['Дата']
        program = row['Программа']
        oven_number = row['Номер духовки']

        # Обработка события
        if state.process_event(event_id, event_time, program, oven_number):
            # Если последовательность завершена, добавляем результат
            results.append({
                'Дата': state.start_time.date(),
                'Печь': row['Печь'],
                'Время старта': state.start_time,
                'Время завершения': state.end_time,
                'Номер программы выпечки': state.program,
                'Номер духовки': state.oven_number,
                'Количество духовок': row['Количество духовок'],
                'Длительность': state.end_time - state.start_time
            })
            state.reset()  # Сбрасываем состояние для новой последовательности

    return results
