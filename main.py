M_IN_KM = 1000
LEN_STEP = 0.65

class Training:

    def __init__(self, action:int, duration: int) -> None:
        self.action = action
        self.duration = duration

    def get_distance(self): # возвращает дистанцию (в километрах), которую преодолел пользователь за время тренировки.
        return self.action * LEN_STEP / M_IN_KM # расстояние, которое спортсмен преодолевает за один шаг или гребок. Один шаг — это 0.65 метра, один гребок при плавании — 1.38 метра.

    def get_mean_speed(self): # возвращает значение средней скорости движения во время тренировки.
        return self.get_distance() / self.duration

    def get_spent_calories(self): # возвращает количество килокалорий, израсходованных за время тренировки.
        pass

    def show_training_info(self):
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()) # возвращает объект класса сообщения.
        


class InfoMessage:

    def __init__(self, training_type, duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Running(Training):

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    
    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
        * self.weight / M_IN_KM * self.duration)



class SportsWalking(Training):

    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
    
    def get_spent_calories(self):
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight + (self.get_mean_speed()**2 / self.height)
        * self.CALORIES_MEAN_SPEED_SHIFT * self.weight) * self.duration



class Swimming(Training):

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2


    def __init__(self, action: int, duration: int, weight: float, length_pool: float, count_pool: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        return (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER) * self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration


def read_package(workout_type, data):
    training_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_class:
        return f'Такого типа тренировок нет'
    else:
        return training_class[workout_type](*data)


def main(training: Training):
    info = Training.show_training_info(training)
    #info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [        
        ('SWM', [7200, 1, 80, 25, 40]), # количество гребков, время в часах, вес пользователя, длина бассейна, сколько раз пользователь переплыл бассейн.
        ('RUN', [15000, 1, 75]), # количество шагов, время тренировки в часах, вес пользователя.
        ('WLK', [9000, 1, 75, 180]), # количество шагов, время тренировки в часах, вес пользователя, рост пользователя.
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
