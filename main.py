import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty

from sudoku import Sudoku
from config import Config as Cfg


class SudokuGame(GridLayout):
    cols = NumericProperty(9)

    def __init__(self, **kwargs):
        super(SudokuGame, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        self.selected_tile = None
        self.grid = None

        self._draw_tiles()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        allowed_keycodes = [str(i) for i in range(1, 10)]

        if keycode[1] == 'backspace':
            self.selected_tile.text = ''
            return

        if keycode[1] not in allowed_keycodes or not self.selected_tile:
            return

        self.selected_tile.text = keycode[1]

    def _draw_tiles(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.cols)]
        for row in range(self.cols):
            for col in range(self.cols):
                tile = SudokuTile(on_release=self._on_release)
                self.grid[row][col] = tile
                self.add_widget(tile)

    def _on_release(self, released):
        if self.selected_tile:
            self.selected_tile.background_color = [0, 0, 0, 1]

        self.selected_tile = released
        self.selected_tile.background_color = [0, 0.69, 1, 1]


class SudokuBoard(Screen):
    elapsed_time = StringProperty('')

    def __init__(self, **kwargs):
        super(SudokuBoard, self).__init__(**kwargs)
        self.start_time = None

    def on_enter(self):
        self.start_time = datetime.datetime.now()
        Clock.schedule_interval(self._update_clock, 1)

    def _update_clock(self, dt):
        current_time = datetime.datetime.now()
        time_delta = current_time - self.start_time
        self.elapsed_time = str(time_delta).split('.')[0]

    def reset_timer(self):
        self.start_time = datetime.datetime.now()
        Clock.schedule_once(self._update_clock)

    def _get_grid(self):
        return self.children[0].children[1].grid

    def clear_board(self):
        grid = self._get_grid()
        for row in range(len(grid)):
            for col in range(len(grid)):
                grid[row][col].text = ''

    def check(self):
        sudoku = Sudoku(self._get_grid())
        sudoku_result = sudoku.check()
        self._show_popup(sudoku_result)

    def solve(self):
        grid = self._get_grid()
        sudoku = Sudoku(grid)
        Clock.schedule_once(lambda dt: sudoku.solve())

    @staticmethod
    def _show_popup(result):
        label_txt = Cfg.SUCCESS.value

        if not result:
            label_txt = Cfg.ERROR.value

        label = Label(text=label_txt)
        popup = Popup(title='Result',
                      content=label,
                      size_hint=(None, None),
                      size=(200, 100))
        popup.open()


class SudokuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SudokuMenu(name='menu'))
        sm.add_widget(SudokuBoard(name='board'))
        return sm


class OutlineButton(Button):
    pass


class SudokuTile(OutlineButton):
    pass


class SudokuMenu(Screen):
    pass


if __name__ == '__main__':
    Config.set('graphics', 'width', Cfg.WIDTH.value)
    Config.set('graphics', 'height', Cfg.HEIGHT.value)
    Config.write()

    app = SudokuApp()
    app.run()
