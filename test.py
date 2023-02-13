import random as r
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,\
    QInputDialog, QListView, QAbstractItemView, QLabel, QListWidget, QListWidgetItem

noses_var = [
    'Pictures/nose1.png',
    'Pictures/nose2.png',
    'Pictures/nose3.png'
]
faces_simp_var = [
    'Pictures/face2.png',
    'Pictures/face4.png',
    'Pictures/face6.png',
    'Pictures/face8.png',
    'Pictures/face10.png',
    'Pictures/face12.png',
    'Pictures/face14.png',
    'Pictures/face16.png'
]
faces_beauty_var = [
    'Pictures/face1.png',
    'Pictures/face3.png',
    'Pictures/face5.png',
    'Pictures/face7.png',
    'Pictures/face9.png',
    'Pictures/face11.png',
    'Pictures/face13.png',
    'Pictures/face15.png'
]
eyes_one_var = [
    'Pictures/eyes3.png',
    'Pictures/eyes4.png'
]
eyes_simp_var =[
    'Pictures/eyes1.png',
    'Pictures/eyes2.png'
]
mouths_var = [
    'Pictures/mouth1.png',
    'Pictures/mouth2.png',
    'Pictures/mouth3.png',
    'Pictures/mouth4.png',
    'Pictures/mouth5.png',
    'Pictures/mouth6.png',
    'Pictures/mouth7.png'
]

kids_sp = []


class Citizen:
    def __init__(self, name, old, happy, modify=None, is_ill=False, bunt=0):
        global noses_var, faces_var, eyes_var, mouths_var
        self.name = name.capitalize()
        self.old = old
        self.happy = happy
        self.modify = modify
        self.is_ill = is_ill
        self.bunt = bunt
        self.days_for_kids = 15
        self.face = faces_simp_var[r.randint(0, len(faces_simp_var) - 1)]
        if self.modify == 'Красивый' or self.modify == 'Сексуальный' or self.modify == 'Гигачад':
            self.face = faces_beauty_var[r.randint(0, len(faces_beauty_var) - 1)]
        self.nose = noses_var[r.randint(0, len(noses_var) - 1)]
        self.eyes = eyes_simp_var[r.randint(0, len(eyes_simp_var) - 1)]
        if self.modify == 'Без глаза':
            self.eyes = eyes_one_var[r.randint(0, len(eyes_one_var) - 1)]
        elif self.modify == 'Без глаз':
            self.eyes = 'Pictures/eyes6.png'
        elif self.modify == 'Слепой':
            self.eyes = 'Pictures/eyes5.png'
        self.mouth = mouths_var[r.randint(0, len(mouths_var) - 1)]
        if self.modify == 'Без челюсти':
            self.mouth = 'Pictures/mouth3.png'
        

    def skip(self):
        self.days_for_kids -= 1
        if self.days_for_kids < 0:
            self.days_for_kids = 0


def new_people():
    len_new_name = r.randint(3, 8)
    new_name = []
    new_old = 16
    new_happy = 100
    new_modify = None
    new_bunt = 0
    new_is_ill = False

    if r.randint(0, 5) == 5:
        new_modify = modifies[r.randint(0, len(modifies) - 1)]

    if r.randint(1, 2) and new_modify == 'Слабый иммунитет':
        new_is_ill = True

    for _ in range(len_new_name):
        new_name.append(rus_alph[r.randint(0, 32)])
    new_name = ''.join(new_name)
    return Citizen(new_name, new_old, new_happy, new_modify, new_is_ill, new_bunt)


class Kid:
    def __init__(self):
        self.days_to_become_adult = 15

    def skip(self):
        self.days_to_become_adult -= 1


class Inventory(QWidget):
    def __init__(self):
        super().__init__()
        global bread
        self.initui()
        
    def initui(self):
        global bread, health, inventory
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.setGeometry(500, 500, 500, 700)
        self.setWindowTitle('Инвентарь')
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(10, 10, 480, 580)
        self.btn_exit = QPushButton(self)
        self.btn_exit.setGeometry(470, 600, 105, 50)
        self.btn_exit.setText('Выход')
        self.btn_exit.clicked.connect(self.exit_to_main)
        for i in inventory:
            newButton = QtWidgets.QPushButton(f'{i}')
            newButton.clicked.connect(lambda x, obj_class=i: self.onClicked(obj_class))
            listWidgetItem = QtWidgets.QListWidgetItem() 
            listWidgetItem.setSizeHint(newButton.sizeHint())
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, newButton)
            self.listWidget.scrollToItem(listWidgetItem)
        
    def onClicked(self, obj):
        global health, bread, inventory, inv, boss_window
        self.use_item_dialog = QMessageBox.question(self, 'SCIFF-17', f"Вы хотите использовать {obj}?",
                                                QMessageBox.Yes | QMessageBox.Cancel)
        if self.use_item_dialog == QMessageBox.Yes:
            if obj == 'Хлеб':
                health += 5
                if health > 20:
                    health = 20
                bread -= 1
                inventory.remove('Хлеб')
                inv.btn_exit.click()
                boss_window.main()
                
                
    def exit_to_main(self):
        global boss_window
        self.close()
        boss_window.show()


class Boss(QWidget):
    def __init__(self):
        super().__init__()
        global homes, people, bread, health
        self.boss_health = r.randint(6, 10)
        self.boss_dead = False
        self.main_dead = False
        self.initui()

    def initui(self):
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setGeometry(500, 500, 800, 1000)
        self.setWindowTitle('Нападение босса')
        self.attack_btn = QPushButton(self)
        self.attack_btn.setGeometry(50, 250, 140, 130)
        self.attack_btn.setText('Атака')
        self.attack_btn.setFont(font)
        self.attack_btn.clicked.connect(self.attack)
        
        self.mercy_btn = QPushButton(self)
        self.mercy_btn.setText('Договор')
        self.mercy_btn.setGeometry(295, 250, 140, 130)
        self.mercy_btn.setFont(font)
        self.mercy_btn.clicked.connect(self.mercy)
        
        self.inventory_btn = QPushButton(self)
        self.inventory_btn.setText('Инвентарь')
        self.inventory_btn.setGeometry(540, 250, 140, 130)
        self.inventory_btn.setFont(font)
        self.inventory_btn.clicked.connect(self.inventory)
        
        self.information_lbl = QLabel(self)
        self.information_lbl.setGeometry(20, 20, 900, 180)
        
        self.boss_inf = QLabel(self)
        self.boss_inf.setText(f'На вас напал босс! У босса {self.boss_health} очков здоровья')
        self.boss_inf.setGeometry(20, 370, 900, 180)
        self.boss_health_lbl = QLabel(self)
        self.boss_health_lbl.setGeometry(450, 20, 300, 30)
        self.boss_health_lbl.setText(f'Здоровье босса: {self.boss_health}')
        self.main()
        
    def main(self):
        global health, people
        if health <= 0:
            self.main_dead = True
        if self.boss_health <= 0:
            self.finish()
        if self.main_dead is True:
            self.close()
            ex.show()
            ex.die()
            ex.info_label.setText('Вы погибли от босса')
        self.information_lbl.setText(f'У вас есть:\n{health} личного здоровья\n{bread} хлеба\n{len(people)} людей\n{homes} домов')
        self.boss_health_lbl.setText(f'Здоровье босса: {self.boss_health}')
    def closeEvent(self, event):
        self.show()
        
    def attack(self):
        global health
        damage = r.randint(1, 5)
        miss = r.randint(0, 4)
        chance = r.randint(1, 100)
        if chance  <= 20:
            crit = r.randint(1, 100)
            if crit <= 10:
                self.boss_health -= 2
                self.boss_inf.setText('Вы попали по боссу\nВы снесли ему 2 очка здоровья')
                crit = r.randint(1, 100)
            if crit <= 5:
                self.boss_health -= 3
                self.boss_inf.setText('Вы попали по боссу\nВы снесли ему 3 очка здоровья')
                crit = r.randint(1, 100)
            if crit <= 2:
                self.boss_health -= 4
                self.boss_inf.setText('Вы попали по боссу\nВы снесли ему 4 очка здоровья')
                crit = r.randint(1, 100)
            if crit <= 1:
                self.boss_health -= 5
                self.boss_inf.setText('Вы попали по боссу\nВы снесли ему 5 очков здоровья')
                crit = r.randint(1, 100)
            else:
                self.boss_health -= 1
                self.boss_inf.setText('Вы попали по боссу\nВы снесли ему 1 очко здоровья')
                crit = r.randint(1, 100)
        else:
            if miss == 0:
                self.boss_inf.setText(f'Вы промахнулись по боссу. \nБосс нанес вам {damage} урона')
                health -= damage
            elif miss == 1:
                self.boss_inf.setText(f'Вы попали по боссу\nНо не смогли пробить броню. \nБосс нанес вам {damage} урона')
                health -= damage
            elif miss == 2:
                 self.boss_inf.setText(f'Вы бы попали по боссу и даже\n пробили бы, но он увернулся.\nБосс нанес вам {damage} урона')
                 health -= damage
            elif miss == 3:
                self.boss_inf.setText(f'Вы попали по боссу, но он отразил\nВаш удар. Босс нанес вам {damage} урона')
                health -= damage
            else:
                 self.boss_inf.setText(f'Вы промахнулись по боссу\nНо он тоже промахнулся. \nБосс не нанес вам никакого урона')
        self.main()
                 
    def mercy(self):
        global people
        try:
            chance = r.randint(1, 100)
            if chance <= 10:
                r_chance = r.randint(0, 1)
                victim = r.randint(1, len(people) - 1)
                if r_chance == 1:
                    self.boss_inf.setText(f'Вы договорились с боссом\nНо взамен он взял {victim} людей и съел')
                    for i in range(victim):
                        people.remove(people[r.randint(0, len(people) - 1)])
                    self.finish()
                else:
                    self.boss_inf.setText(f'Вы договорились с боссом\nИ никто не пострадал')
                    self.finish()
            else:
                r_chance = r.randint(0, 1)
                victim = r.randint(1, len(people) - 1)
                if r_chance == 1:
                    self.boss_inf.setText(f'Вы не договорились с боссом\nИ он взял {victim} людей и съел')
                    for i in range(victim):
                        people.remove(people[r.randint(0, len(people) - 1)])
                else:
                    self.boss_inf.setText(f'Вы  не договорились с боссом\nНо никто не пострадал')
            self.main()
        except ValueError:
            victim = 1
            people.remove(people[0])
            self.close()
            ex.show()
            ex.die()
            ex.info_label.setText('Ваше поселение погибло от босса')
    
    def inventory(self):
        global inv
        inv = Inventory()
        inv.show()
    
    def finish(self):
        global steps
        self.close()
        ex.show()
        win = QMessageBox(self)
        win.setText('Вы победили босса!\nНаграда 25 шагов!')
        win.addButton(QPushButton('Круто'), QMessageBox.YesRole)
        ret = win.exec_()
        steps += 25


class InterView(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
    
    def initui(self):
        self.setGeometry(500, 500, 800, 1000)


class WindowJobs(QWidget):
    def __init__(self):
        super().__init__()
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(0, 0, 500, 500)
        self.btn_exit = None
        self.initui()

    def initui(self):
        self.setWindowTitle('Меню людей')
        self.setGeometry(500, 500, 800, 800)
        self.btn_exit = QPushButton(self)
        self.btn_exit.setGeometry(550, 600, 105, 50)
        self.btn_exit.setText('Выход')
        for i in people:
            newButton = QtWidgets.QPushButton(f'[{people.index(i) + 1}] {i.name}')
            newButton.clicked.connect(lambda x, obj_class=i: self.onClicked(obj_class))
            listWidgetItem = QtWidgets.QListWidgetItem() 
            listWidgetItem.setSizeHint(newButton.sizeHint())
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, newButton)
            self.listWidget.scrollToItem(listWidgetItem)
        
    def onClicked(self, obj):
        self.inter = InterView()
        self.inter.setWindowTitle(f'Досье {obj.name}')
        self.label_name = QLabel(self.inter)
        self.label_name.setGeometry(10, 10, 800, 50)
        self.label_name.setText(f'Имя: {obj.name}')
        self.label_old = QLabel(self.inter)
        self.label_old.setGeometry(10, 60, 800, 50)
        self.label_old.setText(f'Возраст: {obj.old}')
        self.label_happy = QLabel(self.inter)
        self.label_happy.setGeometry(10, 110, 800, 50)
        self.label_happy.setText(f'Счастье: {obj.happy}')
        self.label_modify = QLabel(self.inter)
        self.label_modify.setGeometry(10, 160, 800, 50)
        self.label_modify.setText(f'Без модификатора')
        if obj.modify is not None:
            self.label_modify.setText(f'Модификатор: {obj.modify}')
        self.label_is_ill = QLabel(self.inter)
        self.label_is_ill.setGeometry(10, 210, 800, 50)
        self.label_is_ill.setText('Здоровый')
        if obj.is_ill:
            self.label_is_ill.setText('Больной')
        self.label_bunt = QLabel(self.inter)
        self.label_bunt.setGeometry(10, 260, 800, 50)
        self.label_bunt.setText(f'Очки бунта: {obj.bunt}')
        self.button_exit = QPushButton(self.inter)
        self.button_exit.setGeometry(550, 900, 105, 50)
        self.button_exit.setText('Выход')
        self.button_exit.clicked.connect(self.inter.close)
        self.wood_png = QLabel(self.inter)
        self.wood_pixmap = QtGui.QPixmap('Pictures/wood.png')
        smaller_pixmap = self.wood_pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.wood_png.setPixmap(smaller_pixmap)
        self.wood_png.move(380, 0)
        self.face_png = QLabel(self.inter)
        self.face_pixmap = QtGui.QPixmap(obj.face)
        smaller_pixmap = self.face_pixmap.scaled(270, 295, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.face_png.setPixmap(smaller_pixmap)
        self.face_png.move(430, 170)
        self.eyes_png = QLabel(self.inter)
        self.eyes_pixmap = QtGui.QPixmap(obj.eyes)
        smaller_pixmap = self.eyes_pixmap.scaled(180, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.eyes_png.move(485, 220)
        self.eyes_png.setPixmap(smaller_pixmap)
        self.mouth_png = QLabel(self.inter)
        self.mouth_pixmap = QtGui.QPixmap(obj.mouth)
        smaller_pixmap = self.mouth_pixmap.scaled(120, 120, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.mouth_png.move(510, 300)
        self.mouth_png.setPixmap(smaller_pixmap)
        self.nose_png = QLabel(self.inter)
        self.nose_pixmap = QtGui.QPixmap(obj.nose)
        smaller_pixmap = self.nose_pixmap.scaled(78, 78, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.nose_png.move(550, 270)
        self.nose_png.setPixmap(smaller_pixmap)
        self.inter.show()
        

class MainGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.people = people
        self.initui()

    def initui(self):
        self.setWindowTitle('SCIFF-17')
        self.setGeometry(0, 0, 684, 654)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.info_label = QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.info_label.setFont(font)
        self.info_label.setGeometry(6, 12, 700, 200)
        self.info_label.setText(f'У вас есть {steps} шагов, {homes} домов, {len(people)} человек, {len(kids_sp)}'
                                f' детей.\n'
                                f'Статус Чумы - {chuma}, Статус Гриппа - {gripp}, Статус Простуды - {prostuda}.\n'
                                f'Осталось {food} дней до смерти от голода.\n Осталось {water} дней до смерти от обезвоживания.'
                                f'\nПрошло {days} дней, {month} месяцов')
        self.eat_btn = QPushButton(self)
        self.eat_btn.setGeometry(25, 200, 90, 80)
        self.eat_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eat_btn.setText('Еда')
        self.eat_btn.clicked.connect(self.food)
        self.eat_btn.setFont(font)
        self.drink_btn = QPushButton(self)
        self.drink_btn.setGeometry(145, 200, 90, 80)
        self.drink_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.drink_btn.setText('Вода')
        self.drink_btn.clicked.connect(self.water)
        self.drink_btn.setFont(font)
        self.people_btn = QPushButton(self)
        self.people_btn.setGeometry(265, 200, 90, 80)
        self.people_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.people_btn.setText('Дитя')
        self.people_btn.clicked.connect(self.people_add)
        self.people_btn.setFont(font)
        self.home_btn = QPushButton(self)
        self.home_btn.setGeometry(385, 200, 90, 80)
        self.home_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.home_btn.setText('Дом')
        self.home_btn.clicked.connect(self.home)
        self.home_btn.setFont(font)
        self.jobs_btn = QPushButton(self)
        self.jobs_btn.setGeometry(505, 200, 90, 80)
        self.jobs_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.jobs_btn.setText('Люди')
        self.jobs_btn.clicked.connect(self.jobs)
        self.jobs_btn.setFont(font)
        self.skip_btn = QPushButton(self)
        self.skip_btn.setGeometry(625, 200, 90, 80)
        self.skip_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.skip_btn.setText('Далее')
        self.skip_btn.clicked.connect(self.skip)
        self.skip_btn.setFont(font)
        self.exit_btn = QPushButton(self)
        self.exit_btn.setGeometry(550, 630, 150, 100)
        self.exit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_btn.setText('Выход')
        self.exit_btn.clicked.connect(self.check_exit)
        self.exit_btn.setFont(font)
        self.nick = QInputDialog(self)
        nick = self.nick.getText(self, 'SCIFF-17', 'Введите название поселения: ')
        while nick[0] == '':
            nick = self.nick.getText(self, 'SCIFF-17', 'Введите название поселения: ')
        self.main()

    def check_exit(self):
        self.message_about_exit = QMessageBox(self)
        button_to_answer = QMessageBox.question(self, 'SCIFF-17', "Вы уверены, что хотите выйти?",
                                                QMessageBox.Yes | QMessageBox.Cancel)
        if button_to_answer == QMessageBox.Yes:
            self.close()

    def main(self):
        global steps, homes, people, kids_sp, chuma, gripp, prostuda, food, water, days, month, homes, people_once
        if (water < 0) and food > 0:
            self.info_label.setText('Ваше посление умерло от обезвоживания')
            self.die()
        elif (water > 0) and food < 0:
            self.info_label.setText('Ваше посление умерло от голода')
            self.die()
        elif water < 0 and food < 0:
            self.info_label.setText('Ваше поселение умерло от голода и обезвоживания')
            self.die()
        else:
            if homes > 0:
                if days == 30 and people_once:
                    for i in range(homes):
                        kids_sp.append(Kid())
                    people_once = False
            self.info_label.setText(f'У вас есть {steps} шагов, {homes} домов, {len(people)} человек, {len(kids_sp)}'
                                    f' детей.\n'
                                    f'Статус Чумы - {chuma}, Статус Гриппа - {gripp}, Статус Простуды - {prostuda}.\n'
                                    f'Осталось {food} дней до смерти от голода.\nОсталось {water} '
                                    f'дней до смерти от обезвоживания.'
                                    f'\nПрошло {days} дней, {month} месяцов')

    def skip(self):
        global days, steps, month, food, water, kids_sp, people_once, bread
        if len(kids_sp) > 0:
            for i in kids_sp:
                i.skip()
                if i.days_to_become_adult <= 0:
                    people.append(new_people())
                    kids_sp.remove(i)
        days += 1
        steps += 8
        food -= 1
        water -= 1
        people_once = True
        if bread < 3:
            bread = 3
        if days == 31:
            days = 1
            month += 1
        if month % 2 != 0 and days == 1:
            self.boss()
        self.main()

    def food(self):
        global food, steps, price_fw
        if steps >= price_fw:
            food = 2
            steps -= price_fw
        self.main()

    def water(self):
        global water, steps, price_fw
        if steps >= price_fw:
            water = 2
            steps -= price_fw
        self.main()

    def die(self):
        global food, water
        food = 0
        water = 0
        self.eat_btn.hide()
        self.drink_btn.hide()
        self.skip_btn.hide()
        self.people_btn.hide()
        self.home_btn.hide()
        self.jobs_btn.hide()

    def people_add(self):
        global kids_sp, steps, price_people
        if steps >= price_people:
            kids_sp.append(Kid())
            steps -= price_people
        self.main()

    def jobs(self):
        self.jobs_menu = WindowJobs()
        self.jobs_menu.btn_exit.clicked.connect(self.jobs_menu.close)
        self.jobs_menu.show()

    def home(self):
        global homes, steps, price_home
        if steps >= price_home:
            homes += 1
            steps -= price_home
        self.main()
    
    def boss(self):
        global people, homes, bread, boss_window
        health = 20
        boss_window.show()
        

rus_alph = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

modifies = [
    'Умный',
    'Находчивый',
    'Красивый',
    'Недостаток кальция',
    'Слепой',
    'Без руки',
    'Без ноги',
    'Без рук и ног',
    'Без глаза',
    'Без глаз',
    'Без некоторых внутренних органов',
    'Без челюсти',
    'Пьяница',
    'Слабак',
    'Доходяга',
    'Сильный',
    'Мудрый',
    'Сексуальный',
    'Гигачад',
    'Генетический урод',
    'Везучий',
    'Невезучий'
]


people = []
for _ in range(50):
    people.append(new_people())

days = 0
steps = 800
homes = 0
food = 200
water = 200
chuma = 0
gripp = 0
prostuda = 0
month = 0
price_fw = 2
price_people = 8
price_home = 10
people_once = True
bread = 3
health = 20
inventory = ['Хлеб', 'Хлеб', 'Хлеб']

# while True:
#     print(f'Дней: {days}')
#     print(f'Детей: {kids}')
#     action = input('>> ')
#
#     if action.lower() == 'дитя':
#         kids += 1
#         kids_sp.append(Kid())
#
#     if action.lower() == 'далее':
#         if kids > 0:
#             for i in kids_sp:
#                 i.skip()
#         days += 1
#
#     if action.lower() == 'выход':
#         break

# НЕ БАГ А ФИЧА
#def skip(self):
#        self.days_to_become_adult -= 1
#        if self.days_to_become_adult < 0:
#            self.days_to_become_adult = 0
#        if self.days_to_become_adult == 0:
#            people.append(new_people())
#            kids_sp.remove(self)
#    .


app = QApplication(sys.argv)
ex = MainGame()
ex.show()
inv = Inventory()
boss_window = Boss()
sys.exit(app.exec_())
