import csv


def read_file(f_name: str) -> list:
    """ Считывает файл в список """
    with open(
        f_name, "r", encoding="utf-8", newline=""
    ) as f_csv:  # считывает Corp_S и создает форму класса f_csv
        df = csv.reader(f_csv, delimiter=";")  # ; как конец сущности
        df = list(df)
        return df


def dep_structure(df: list):
    """ Первая опция в меню: вывод структуры департаментов """
    columns = df[0]
    records = df[1:]
    idx_d = columns.index("Департамент")  # находим индекс департамента из 1 строки
    idx_o = columns.index("Отдел")  # находим индекс отдела из 1 строки
    dic = dict()
    for record in records:
        if record[idx_d] not in dic.keys():
            dic[record[idx_d]] = set()
        dic[record[idx_d]].add(record[idx_o])
    for k, v in dic.items():
        print(k)
        for otdel in v:
            print("   " + otdel)


def form_otchet(df: list) -> dict:
    """ Формирование отчета по департаментам для 1 и 2 опции """
    columns = df[0]
    records = df[1:]
    idx_d = columns.index("Департамент")
    idx_o = columns.index("Оклад")
    dic = dict()
    for record in records:
        dep = record[idx_d]
        oklad = int(record[idx_o])
        if record[idx_d] in dic.keys():

            if oklad > dic[dep]["Макс. оклад"]:
                dic[dep]["Макс. оклад"] = oklad

            if oklad < dic[dep]["Мин. оклад"]:
                dic[dep]["Мин. оклад"] = oklad

            dic[dep]["Сред. оклад"] = round(
                (dic[dep]["Сред. оклад"] * dic[dep]["Численность"] + oklad)
                / (dic[dep]["Численность"] + 1)
            )
            dic[dep]["Численность"] += 1
        else:
            dic[dep] = {
                "Численность": 1,
                "Мин. оклад": oklad,
                "Сред. оклад": oklad,
                "Макс. оклад": oklad,
                "Департамент": dep,
            }

    return dic


def print_form(dic):
    """Выводит на печать отчет по департаментам"""
    for k, v in dic.items():
        print(
            f"{k} Численность: {v['Численность']}",
            f"Мин оклад: {v['Мин. оклад']}, Сред. оклад: ",
            f"{v['Сред. оклад']}, Макс. оклад: {v['Макс. оклад']}",
        )


def save_form(dic: dict):
    """Третья опция в меню: сохраняет отчет по департаментам в виде csv-файла"""
    with open("saved_form.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "Департамент",
                "Численность",
                "Мин. оклад",
                "Сред. оклад",
                "Макс. оклад",
            ],
        )
        w.writeheader()  # используем список из ключей словаря в качестве названия колонок
        for v in dic.values():
            w.writerow(v)  # сохраняем в колонки значения из словаря


def options():
    """Вывод меню для пользователя"""
    print("\033[35m{}".format("*" * 40))
    print("*" * 10, " " * 6, "Меню", " " * 6, "*" * 10)
    print("*" * 40)
    print("\033[1m{}".format("Выберите нужный пункт меню:"))
    print("\033[0m{}".format("1. Вывод департамента и команд"))
    print("2. Вывод сводного отчёта по департаментам")
    print("3. Сохранить сводный отчёт по департаментам в виде csv-файла.")
    print("*" * 40)


def correct_user_option() -> int:
    """Ввод числа пользователем и проверка корректности"""
    spisok_dopustimih = [1, 2, 3]
    option = input("Выберите 1, 2 или 3: ")
    if (
        option.isdecimal() and int(option) in spisok_dopustimih
    ):  # проверка на десятиричность и что число из {1,2,3}
        return int(option)
    else:
        print("Неверный ввод. Попробуйте ещё раз!")
        return correct_user_option()


def main_function():
    """Основная функция. Тут вся логика программы"""
    options()
    user_option = correct_user_option()
    df = read_file("Corp_Summary.csv")

    if user_option == 1:
        dep_structure(df)
    elif user_option == 2:
        dic = form_otchet(df)
        print_form(dic)
    else:
        dic = form_otchet(df)
        save_form(dic)
        print("сохранено!")


if __name__ == "__main__":
    main_function()
