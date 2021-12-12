class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed:float,
                calories:float
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )



class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    COEFF_RUN_1: int = 18
    COEFF_RUN_2: int = 20
    COEFF_MINUTE: int = 60
    def __init__(self,
                action: int,
                duration: float,
                weight: float
                ) -> None:
        self.duration = duration
        self.action = action
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
                           self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        spent_calories: float = (
                                (self.COEFF_RUN_1*self.get_mean_speed() - self.COEFF_RUN_2)
                                * self.weight/self.M_IN_KM
                                * (self.duration*self.COEFF_MINUTE)
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_WLK_1: float = 0.035
    DEGREE: int = 2
    COEFF_WLK_2: float = 0.029
    def __init__(
                 self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories: float =(
                                (self.COEFF_WLK_1 * self.weight
                                + (self.get_mean_speed()**self.DEGREE // self.height)
                                * self.COEFF_WLK_2 * self.weight)
                                * (self.duration*self.COEFF_MINUTE)
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_SWM_1: float = 1.1
    COEFF_SWM_2: int = 2

    def __init__(
                 self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = (
                                (self.get_mean_speed() + self.COEFF_SWM_1)
                                * self.COEFF_SWM_2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    compliance_dict: dict[str, str] = {'SWM': Swimming,
                                       'RUN': Running,
                                       'WLK': SportsWalking
                                       }
    if workout_type not in compliance_dict.keys():
        raise ValueError('Неизвестный тип тренировки')
        #print(workout_type)
    else:
        training_dict = {'SWM':Swimming, 'RUN':Running, 'WLK':SportsWalking}
        return training_dict[workout_type](*data)

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

