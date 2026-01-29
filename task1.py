# Індивідуальна робота. Завдання 1.
# Жадібний алгоритм для складання розкладу занять (задача покриття множини).

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
        # Якщо не вийшло — продовжуємо без падіння
        pass


class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = set(can_teach_subjects)
        # Предмети, які реально будуть призначені в розкладі
        self.assigned_subjects = set()

    def __repr__(self):
        return f"Teacher({self.first_name} {self.last_name}, {self.age})"


def create_schedule(subjects, teachers):
    """
    Жадібний алгоритм для покриття всіх предметів викладачами.
    На кожному кроці обираємо викладача, який:
      1) покриває найбільшу кількість ще не покритих предметів;
      2) при рівності – наймолодший за віком.
    """
    uncovered_subjects = set(subjects)
    selected_teachers = []

    while uncovered_subjects:
        best_teacher = None
        best_cover_count = 0

        for teacher in teachers:
            # Предмети, які може покрити цей викладач серед ще не покритих
            can_cover = teacher.can_teach_subjects & uncovered_subjects
            cover_count = len(can_cover)

            if cover_count == 0:
                continue

            if best_teacher is None:
                best_teacher = teacher
                best_cover_count = cover_count
            else:
                # більше предметів → кращий
                if cover_count > best_cover_count:
                    best_teacher = teacher
                    best_cover_count = cover_count
                # при однаковій кількості — молодший
                elif cover_count == best_cover_count and teacher.age < best_teacher.age:
                    best_teacher = teacher
                    best_cover_count = cover_count

        # Якщо ніхто більше не може покрити нові предмети — провал
        if best_teacher is None:
            return None

        # Призначаємо викладачу нові предмети
        new_subjects = best_teacher.can_teach_subjects & uncovered_subjects
        best_teacher.assigned_subjects |= new_subjects

        # Вилучаємо ці предмети з ще не покритих
        uncovered_subjects -= new_subjects

        # Додаємо викладача в розклад, якщо ще не додали
        if best_teacher not in selected_teachers:
            selected_teachers.append(best_teacher)

    return selected_teachers


if __name__ == '__main__':
    _configure_utf8_output()

    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Список викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    schedule = create_schedule(subjects, teachers)

    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            if teacher.assigned_subjects:
                print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}\n")
            else:
                print("   Викладає предмети: (не призначено)\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")

