class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.'
               )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    M_IN_H: int = 60
    LEN_STEP: float = 0.65
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration,
                           distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        speed = self.get_mean_speed()
        spent_calories = ((coeff_calorie_1 * speed - coeff_calorie_2)
                          * self.weight / self.M_IN_KM * self.M_IN_H
                          * self.duration)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_wlk_1 = 0.035
        coeff_calorie_wlk_2 = 0.029
        speed = self.get_mean_speed()
        spent_calories = ((coeff_calorie_wlk_1 * self.weight
                          + (speed ** 2 // self.height)
                          * coeff_calorie_wlk_2 * self.weight)
                          * self.M_IN_H * self.duration)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
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
        coeff_calorie_swm_1 = 1.1
        coeff_calorie_swm_2 = 2
        speed = self.get_mean_speed()
        spent_calories = ((speed + coeff_calorie_swm_1)
                          * coeff_calorie_swm_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return dict_training[workout_type](*data)


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
