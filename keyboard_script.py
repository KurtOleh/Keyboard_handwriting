from math import fabs
from tkinter import messagebox as mb
import keyboard
import threading
import pickle
import time

etalon1, etalon2 = [], []


class WriteDown:
    def __init__(self):
        self.started_at = time.time()
        self.interval_pr = time.time()
        self.time_betw_keys = []
        self.key_hold_time = []
        self.first_time = True
        self.task = threading.Thread(target=self.tracking)
        self.task.start()

    def tracking(self):
        global etalon1, etalon2
        keyboard.hook(self.print_pressed_keys)
        keyboard.wait('Esc')

        etalon1, etalon2 = [], []
        Processing(self.time_betw_keys, self.key_hold_time)

    def print_pressed_keys(self, button):
        if button.event_type is 'down':
            self.started_at = time.time()
            if self.first_time is False:
                self.time_betw_keys.append(time.time() - self.interval_pr)
            else:
                self.first_time = False

        if button.event_type is 'up':
            self.interval_pr = time.time()
            self.key_hold_time.append(time.time() - self.started_at)


class Processing:
    def __init__(self, time_betw_keys, key_hold_time):
        self.time_betw_keys = time_betw_keys
        self.key_hold_time = key_hold_time
        self.new_time_betw_keys, self.new_key_hold_time = [], []
        self.expected_value1, self.expected_value2 = [], []
        self.dis1, self.dis2 = [], []
        self.Tp1, self.Tp2 = [], []
        self.argument_check()

    def argument_check(self):
        count1, count2 = 0, 0
        temp_arr1, temp_arr2 = [], []

        for i in range(len(self.time_betw_keys)):
            for j, value1 in enumerate(self.time_betw_keys):
                if j is not count1:
                    temp_arr1.append(value1)
            self.new_time_betw_keys.append(temp_arr1)
            temp_arr1 = []
            count1 += 1

        for i in range(len(self.key_hold_time)):
            for j, value2 in enumerate(self.key_hold_time):
                if j is not count2:
                    temp_arr2.append(value2)
            self.new_key_hold_time.append(temp_arr2)
            temp_arr2 = []
            count2 += 1

        self.math_expected()


    def math_expected(self):
        try:
            sum_total1, sum_total2 = 0, 0

            for list1 in self.new_time_betw_keys:
                for value1 in list1:
                    sum_total1 += value1
                self.expected_value1.append(sum_total1 / (len(self.new_time_betw_keys) - 1))
                sum_total1 = 0

            for list2 in self.new_key_hold_time:
                for value2 in list2:
                    sum_total2 += value2
                self.expected_value2.append(sum_total2 / (len(self.new_key_hold_time) - 1))
                sum_total2 = 0

            self.dispersion()
        except (ZeroDivisionError, ValueError):
            mb.showerror("Ошибка", "Ошибка ввода данных!")
            exit()


    def dispersion(self):
        sum_total1, sum_total2 = 0, 0

        for index1, list1 in enumerate(self.new_time_betw_keys):
            for value1 in list1:
                sum_total1 += (value1 - self.expected_value1[index1]) ** 2
            self.dis1.append((sum_total1 / (len(self.new_time_betw_keys) - 2)) ** 0.5)
            sum_total1 = 0

        for index2, list2 in enumerate(self.new_key_hold_time):
            for value2 in list2:
                sum_total2 += (value2 - self.expected_value2[index2]) ** 2
            self.dis2.append((sum_total2 / (len(self.new_key_hold_time) - 2)) ** 0.5)
            sum_total2 = 0

        self.student_ratio()


    def student_ratio(self):
        for index1, value1 in enumerate(self.time_betw_keys):
            self.Tp1.append(fabs((value1 - self.expected_value1[index1]) / self.dis1[index1]))

        for index2, value2 in enumerate(self.key_hold_time):
            self.Tp2.append(fabs((value2 - self.expected_value2[index2]) / self.dis2[index2]))

        self.check()



    def check(self):
        Tk = 0.83   # (0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83, 0.83)
        # print("Практический коэффициент Стьюдента: Интервал - {}".format(self.Tp1))
        # print("Практический коэффициент Стьюдента: Удержание - {}".format(self.Tp2))
        try:
            for index1, value1 in enumerate(self.Tp1):
                if value1 < Tk:     # [len(self.time_betw_keys) - 6]:
                    etalon1.append(self.time_betw_keys[index1])

            for index2, value2 in enumerate(self.Tp2):
                if value2 < Tk:     # [len(self.time_betw_keys) - 6]:
                    etalon2.append(self.key_hold_time[index2])
        except IndexError:
            mb.showerror("Ошибка", "Index out of range!")
            exit()


class Training:
    def __init__(self, password):
        self.password = password
        self.save_etalon()

    def save_etalon(self):
        with open('pass_etalon.pickle', 'rb') as file:
            data_read = pickle.load(file)

        # print(data_read)
        data = dict(data_read)
        data[self.password] = (etalon1, etalon2)
        # data = {self.password: (etalon1, etalon2)}

        with open('pass_etalon.pickle', 'wb') as filew:
            pickle.dump(data, filew)

        # print(self.password)


class Authentication:
    def __init__(self, password):
        self.password = password
        self.result1 = False
        self.result2 = False
        self.auth = False

    def validation_check(self) -> bool:
        sum_total = 0
        with open('pass_etalon.pickle', 'rb') as file:
            data_read = pickle.load(file)

        data = dict(data_read)
        # print(data)

        for i in data_read.keys():
            if i == self.password:
                try:
                    min_etalon1 = min(data.get(self.password)[0])
                    max_etalon1 = max(data.get(self.password)[0])

                    for j in etalon1:
                        sum_total += j
                    middle_etalon1 = sum_total / len(etalon1)
                    sum_total = 0

                    if min_etalon1 < middle_etalon1 < max_etalon1:
                        self.result1 = True

                    min_etalon2 = min(data.get(self.password)[1])
                    max_etalon2 = max(data.get(self.password)[1])

                    for j in etalon2:
                        sum_total += j
                    middle_etalon2 = sum_total / len(etalon2)

                    if min_etalon2 < middle_etalon2 < max_etalon2:
                        self.result2 = True

                    if self.result1 is self.result2 is True:
                        self.auth = True
                except (ZeroDivisionError, ValueError):
                    return False

                # print(etalon1)
                # print(etalon2)
                # print(middle_etalon1)
                # print(middle_etalon2)
                break

        return self.auth

# WriteDown()