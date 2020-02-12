 #! ./usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os


from utils import get_teams_list
from utils import read_break_time, read_circles_number
from utils import read_group_name, read_group_size
from utils import generate_schedule_doc


if __name__ == '__main__':
    group_name = read_group_name()
    teams_file = 'list_{}.txt'.format(group_name)
    print('Составы команд будут подгружены из файла {}'.format(teams_file))

    group_size = read_group_size()
    ROUNDS_NUMBER = group_size if group_size % 2 != 0 else group_size - 1

    circles_number = read_circles_number()

    break_time = read_break_time(ROUNDS_NUMBER, circles_number)

    dst_path = 'out/schedule{}{}_{}'.format(group_name, group_size, circles_number)
    print('Расписание появится в файле {}.pdf'.format(dst_path))

    teams = get_teams_list(teams_file)
    schedule_json_name = 'sources/schedule_{}.json'.format(
        group_size if group_size % 2 == 0 else group_size + 1)
    print('Расписание будет подгружено из файла {}'.format(schedule_json_name))
    with open(schedule_json_name, 'r') as f_in:
        schedule = json.load(f_in)


    schedule_doc = generate_schedule_doc(
        schedule,
        teams,
        group_size,
        group_name,
        circles_number,
        ROUNDS_NUMBER,
        break_time
    )

    try:
        os.mkdir('out')
    except FileExistsError:
        pass
    schedule_doc.generate_pdf(dst_path, clean_tex=False)
    os.remove('{}.tex'.format(dst_path))
    print('Расписание выгружено в файл {}.pdf'.format(dst_path))
