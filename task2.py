# Індивідуальна робота. Завдання 2.
# Локальний пошук для мінімізації функції Сфери.


import random
import math
import sys


def _configure_utf8_output():
    """
    На деяких Windows-консолях кодування може бути не UTF-8, через що
    друк українських літер викликає UnicodeEncodeError.
    """
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


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


def _max_range(bounds):
    return max(high - low for (low, high) in bounds)


def _best_of_neighbors(func, x, bounds, step, samples=20):
    """Повертає (кращий_сусід, значення) серед samples випадкових сусідів."""
    best_x = None
    best_val = float("inf")
    for _ in range(samples):
        cand = random_neighbor(x, bounds, step=step)
        val = func(cand)
        if val < best_val:
            best_val = val
            best_x = cand
    return best_x, best_val


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Алгоритм підйому на гору (тут – спуск до мінімуму):
    - стартує з випадкової точки
    - на кожній ітерації обирає найкращого з кількох сусідів
    - якщо покращення немає — зменшує крок (адаптивний step)
    - завершується, якщо крок або покращення стає дуже малим.
    """
    step = _max_range(bounds) * 0.2  # стартовий крок ~ 20% діапазону
    neighbor_samples = 30

    current = random_point(bounds)
    current_value = func(current)
    best = current[:]
    best_value = current_value

    for _ in range(iterations):
        prev_value = best_value

        neighbor, neighbor_value = _best_of_neighbors(
            func, current, bounds, step=step, samples=neighbor_samples
        )

        if neighbor_value + epsilon < current_value:
            current = neighbor
            current_value = neighbor_value
            if current_value < best_value:
                best = current[:]
                best_value = current_value
        else:
            step *= 0.5  # немає покращення — робимо менший крок

        if best_value < epsilon:
            break
        if abs(prev_value - best_value) < epsilon and step < epsilon:
            break

    return best, best_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Випадковий локальний пошук:
    - переважно шукає локально (сусіди), але інколи робить глобальний рестарт
    - приймає тільки покращення
    - зменшує крок з часом, щоб "доточувати" розв'язок.
    """
    step = _max_range(bounds) * 0.5
    restart_prob = 0.05

    best = random_point(bounds)
    best_value = func(best)
    current = best[:]
    current_value = best_value

    for _ in range(iterations):
        prev_best = best_value

        if random.random() < restart_prob:
            candidate = random_point(bounds)
        else:
            candidate = random_neighbor(current, bounds, step=step)

        candidate_value = func(candidate)

        if candidate_value < current_value:
            current = candidate
            current_value = candidate_value

        if current_value < best_value:
            best = current[:]
            best_value = current_value

        step *= 0.995  # повільне зменшення кроку

        if best_value < epsilon:
            break
        if abs(prev_best - best_value) < epsilon and step < epsilon:
            break

    return best, best_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=3000, temp=1000, cooling_rate=0.995, epsilon=1e-6):
    """
    Імітація відпалу:
    - дозволяє іноді приймати гірші рішення з ймовірністю, що залежить від температури
    - температура поступово зменшується (охолодження)
    - завершується, коли температура < epsilon або майже немає змін.
    """
    # Щоб уникати невдалих стартів, робимо кілька перезапусків
    restarts = 5

    global_best = None
    global_best_value = float("inf")

    for _ in range(restarts):
        current = random_point(bounds)
        current_value = func(current)

        best = current[:]
        best_value = current_value

        t = float(temp)
        step = _max_range(bounds) * 0.5  # початковий розмір кроку

        for _ in range(iterations):
            if t < epsilon:
                break

            prev_best = best_value

            # Беремо найкращого з кількох кандидатів (краще ніж 1 випадковий сусід)
            candidate, candidate_value = _best_of_neighbors(
                func, current, bounds, step=step, samples=15
            )

            delta = candidate_value - current_value

            if delta < 0:
                current = candidate
                current_value = candidate_value
            else:
                # приймаємо гірші рішення з певною ймовірністю
                if random.random() < math.exp(-delta / t):
                    current = candidate
                    current_value = candidate_value

            if current_value < best_value:
                best = current[:]
                best_value = current_value

            # охолодження і зменшення кроку
            t *= cooling_rate
            step = max(_max_range(bounds) * 0.0005, step * cooling_rate)

            if best_value < epsilon:
                break
            if abs(prev_best - best_value) < epsilon and step < epsilon:
                break

        if best_value < global_best_value:
            global_best = best[:]
            global_best_value = best_value

        if global_best_value < epsilon:
            break

    return global_best, global_best_value


if __name__ == "__main__":
    _configure_utf8_output()

    # Межі для функції (двовимірний випадок)
    bounds = [(-5, 5), (-5, 5)]

    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", f"{hc_value:.6e}")

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", f"{rls_value:.6e}")

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", f"{sa_value:.6e}")

