import os
import toml
from PIL import ImageGrab
import flet as ft

CONFIG_FILE_PAHT = './config.toml'

class Config():
    def __init__(self, file_path:str=CONFIG_FILE_PAHT):
        if not os.path.isfile(file_path):
            exit()
        self.all_config = toml.load(file_path)
        self.file_path = file_path
        self.config = self.all_config['area'][0]

    def save(self, file_path:str=None):
        if None != file_path:
            self.file_path = file_path
        with open(self.file_path, 'wt') as f:
            toml.dump(self.all_config, f)
    
    def get_all(self) -> list:
        return self.all_config['area']

    def get_current(self) -> dict:
        return self.config

    def set_current(self, area_name):
        print(area_name)
        for cfg in self.get_all():
            if area_name == cfg['name']:
                self.config = cfg
                print(self.config)
                return
        self.config = self.all_config['area'][0]

    def get_current_value(self, name):
        return self.config[name]

    def set_current_value(self, name, value):
        self.config[name] = value

g_cfg = Config()


class FletMain():
    def __init__(self):
        pass

    def flet_main(self, page: ft.Page):
        self.page = page
        page.window_width = 300
        page.window_height = 500
        page.window_resizable = True

        # config selector
        self.create_selector()
        page.add(self.select_config)

        # position
        self.create_position_field()
        page.add(ft.Row(controls=[self.start_x_field, self.start_y_field]))
        page.add(ft.Row(controls=[self.width_field, self.height_field]))

        # filename
        self.create_filename_field()
        self.create_save_btn()
        # page.add(ft.Row(controls=[self.path_field, self.prefix_field, self.number_field]))
        page.add(self.path_field)
        page.add(self.prefix_field)
        page.add(ft.Row(controls=[self.number_field, self.save_btn]))

        # key event handler
        page.on_keyboard_event = self.on_keyboard_handler

        # window update
        page.update()

    def update(self):
        self.start_x_field.value = g_cfg.get_current_value('start_x')
        self.start_y_field.value = g_cfg.get_current_value('start_y')
        self.width_field.value = g_cfg.get_current_value('width')
        self.height_field.value = g_cfg.get_current_value('height')
        self.path_field.value = g_cfg.get_current_value('path')
        self.prefix_field.value = g_cfg.get_current_value('prefix')
        self.number_field.value = g_cfg.get_current_value('number')
        self.page.update()

    def create_selector(self):
        def select_config_change(e):
            g_cfg.set_current(e.data)
            self.update()
        names = [ft.dropdown.Option(cfg['name']) for cfg in g_cfg.get_all()]
        self.select_config = ft.Dropdown(options=names, value=names[0], autofocus=False, width=210, on_change=select_config_change)

    def create_position_field(self):
        def position_field_change(e):
            label = e.control.label
            g_cfg.set_current_value(label, e.control.value)
        field_width = 100
        self.start_x_field = ft.TextField(label='start_x', width=field_width, value=g_cfg.get_current_value('start_x'), on_change=position_field_change)
        self.start_y_field = ft.TextField(label='start_y', width=field_width, value=g_cfg.get_current_value('start_y'), on_change=position_field_change)
        self.width_field = ft.TextField(label='width', width=field_width, value=g_cfg.get_current_value('width'), on_change=position_field_change)
        self.height_field = ft.TextField(label='height', width=field_width, value=g_cfg.get_current_value('height'), on_change=position_field_change)

    def create_filename_field(self):
        def filename_field_change(e):
            label = e.control.label
            g_cfg.set_current_value(label, e.control.value)
        self.path_field = ft.TextField(label='path', width=210, value=g_cfg.get_current_value('path'), on_change=filename_field_change)
        self.prefix_field = ft.TextField(label='prefix', width=210, value=g_cfg.get_current_value('prefix'), on_change=filename_field_change)
        self.number_field = ft.TextField(label='number', width=100, value=g_cfg.get_current_value('number'), on_change=filename_field_change)

    def create_save_btn(self):
        def save_btn_click(e):
            g_cfg.save()
        self.save_btn = ft.ElevatedButton('Save', width=100, on_click=save_btn_click)

    def on_keyboard_handler(self, e: ft.KeyboardEvent):
        # print(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")
        if ' ' == e.key:
            os.makedirs(g_cfg.get_current_value('path'), exist_ok=True)
            scname = '{}{:03}.png'.format(g_cfg.get_current_value('prefix'), g_cfg.get_current_value('number'))
            scname = os.path.join(g_cfg.get_current_value('path'), scname)
            bbox = (
                g_cfg.get_current_value('start_x'),
                g_cfg.get_current_value('start_y'),
                g_cfg.get_current_value('start_x') + g_cfg.get_current_value('width'),
                g_cfg.get_current_value('start_y') + g_cfg.get_current_value('height'),
            )
            ImageGrab.grab(bbox=bbox, all_screens=True).save(scname)
            key = 'number'
            g_cfg.set_current_value(key, g_cfg.get_current_value(key) + 1)
            print('save {}'.format(scname))
            self.update()

g_flt = FletMain()

def main():
    ft.app(target=g_flt.flet_main)

if __name__ == '__main__':
    main()
