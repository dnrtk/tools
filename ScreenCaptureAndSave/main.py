import os
import toml
from PIL import ImageGrab

CONFIG_FILE_PAHT = './config.toml'

if not os.path.isfile(CONFIG_FILE_PAHT):
    exit()

with open(CONFIG_FILE_PAHT, 'r') as f:
    config = toml.load(f)

while True:
    scname = '{}{:03}.png'.format(config['file']['prefix'], config['file']['number'])
    print('next file: {} '.format(scname), end='')
    scname = os.path.join(config['file']['path'], scname)
    key_in = input()
    if '' != key_in:
        exit()
    ImageGrab.grab(bbox=(config['start']['x'], config['start']['y'], config['end']['x'], config['end']['y']), all_screens=True).save(scname)
    config['file']['number'] += 1
