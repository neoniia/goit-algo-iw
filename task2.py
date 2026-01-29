# Індивідуальна робота. Завдання 2.
# Локальний пошук для мінімізації функції Сфери.


import random
import math


# Визначення функції Сфери
def sphere_function(x):
    """
    f(x) = sum(x_i^2)
    Глобальний мінімум: в точці x = (0, 0, ..., 0), f(x) = 0.
    """
    return sum(xi ** 2 for xi in x)


def random_point(bounds):
    """Генерує випадкову точку в межах bounds."""
    return [random.uniform(low, high) for (low, high) in bounds]


def clamp_point(x, bounds):
    """Обмежує координати точки x межами bounds."""
    return [
        max(bounds[i][0], min(bounds[i][1], x[i]))
        for i in range(len(x))
    ]


def random_neighbor(x, bounds, step=0.1):
    """Генерує випадкового сусіда в околі step навколо x."""
    neighbor = [
        xi + random.uniform(-step, step)
        for xi in x
    ]
    return clamp_point(neighbor, bounds)


def distance(x1, x2):
    """Евклідова відстань між двома точками."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(x1, x2)))


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Алгоритм підйому на гору (тут – спуск до мінімуму):
    - стартує з випадкової точки
    - на кожній ітерації переходить до кращого сусіда (якщо є покращення)
    - завершується, якщо покращення майже немає.
    """
    current = random_point(bounds)
    current_value = func(current)

    for _ in range(iterations):
        prev = current[:]
        prev_value = current_value

        neighbor = random_neighbor(current, bounds, step=0.1)
        neighbor_value = func(neighbor)

        if neighbor_value < current_value:
            current = neighbor
            current_value = neighbor_value

        if abs(current_value - prev_value) < epsilon and distance(current, prev) < epsilon:
            break

    return current, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Випадковий локальний пошук:
    - на кожному кроці випадково генеруємо сусідню точку
    - приймаємо тільки покращення
    - завершуємося, якщо зміни малі.
    """
    current = random_point(bounds)
    current_value = func(current)

    for _ in range(iterations):
        prev = current[:]
        prev_value = current_value

        candidate = random_neighbor(current, bounds, step=0.5)
        candidate_value = func(candidate)

        if candidate_value < current_value:
            current = candidate
            current_value = candidate_value

        if abs(current_value - prev_value) < epsilon and distance(current, prev) < epsilon:
            break

    return current, current_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    """
    Імітація відпалу:
    - дозволяє іноді приймати гірші рішення з ймовірністю, що залежить від температури
    - температура поступово зменшується (охолодження)
    - завершується, коли температура < epsilon або майже немає змін.
    """
    current = random_point(bounds)
    current_value = func(current)

    best = current[:]
    best_value = current_value

    for _ in range(iterations):
        if temp < epsilon:
            break

        prev = current[:]
        prev_value = current_value

        candidate = random_neighbor(current, bounds, step=0.5)
        candidate_value = func(candidate)

        delta = candidate_value - current_value

        if delta < 0:
            # краще рішення — приймаємо завжди
            current = candidate
            current_value = candidate_value
        else:
            # гірше рішення — приймаємо з певною ймовірністю
            if random.random() < math.exp(-delta / temp):
                current = candidate
                current_value = candidate_value

        if current_value < best_value:
            best = current[:]
            best_value = current_value

        temp *= cooling_rate

        if abs(current_value - prev_value) < epsilon and distance(current, prev) < epsilon:
            break

    return best, best_value


if __name__ == "__main__":
    # Межі для функції (двовимірний випадок)
    bounds = [(-5, 5), (-5, 5)]

    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)

