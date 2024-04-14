
from windows.modules.window import Window
from windows.tab1 import Tab1
from windows.tab2 import Tab2

if __name__ == '__main__':
    window = Window('Сигналы в волноводе')

    tabs_controller = window.create_tabs_controller(window.root, 400, 100)
    tabs_controller.pack()

    tab1 = Tab1(window, tabs_controller)
    tab1.pack()
    tab1.run()

    tab2 = Tab2(window, tabs_controller)
    tab2.pack()
    tab2.run()

    tabs_controller.add(tab1.frame.root, 'Траектории лучей')
    tabs_controller.add(tab2.frame.root, 'Спектр сигнала')

    window.run()


