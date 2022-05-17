from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    M_IN_H: int = 60
    COEFF_CALORIE_RUN_1: int = 18
    COEFF_CALORIE_RUN_2: int = 20
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: int = 2
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError('Определите get_spent_calories() в %s.'
                                  % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2) * self.weight
                / self.M_IN_KM * self.M_IN_H * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_WLK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_WLK_2 * self.weight)
                * self.M_IN_H * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = ((self.length_pool * self.count_pool
                      / self.M_IN_KM) / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)
                * self.COEFF_CALORIE_SWM_2 * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_training: Dict[str, str] = {'SWM': Swimming,
                                     'RUN': Running,
                                     'WLK': SportsWalking}
    try:
        return dict_training[workout_type](*data)
    except KeyError:
        print('Внимание! Неизвестная тренировка.')


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
