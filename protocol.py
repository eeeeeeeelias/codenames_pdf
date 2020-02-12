 #! ./usr/bin/python3
# -*- coding: utf-8 -*-
import os

from utils import get_teams_list, read_circles_number, read_group_name, read_group_size
from utils import generate_protocol_doc

if __name__ == '__main__':
    group_name = read_group_name()
    teams_file = 'list_{}.txt'.format(group_name)
    print('Составы команд будут подгружены из файла {}'.format(teams_file))

    group_size = read_group_size()

    circles_number = read_circles_number()

    dst_path = 'out/protocol{}{}_{}'.format(group_name, group_size, circles_number)
    print('Протокол появится в файле {}.pdf'.format(dst_path))

    teams = get_teams_list(teams_file)

    protocol_doc = generate_protocol_doc(teams, group_size, group_name, circles_number)

    try:
        os.mkdir('out')
    except FileExistsError:
        pass
    protocol_doc.generate_pdf(dst_path, clean_tex=False)
    os.remove('{}.tex'.format(dst_path))
    print('Протокол выгружен в файл {}.pdf'.format(dst_path))
