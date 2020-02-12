import pylatex

from .common_utils import get_match_info

SCHEDULE_HEADER = ('Тур', 'Соперники', 'Стол', 'Первый ход')
GROUP_SEATS_NUMBER = 5
BREAK_ROW = (pylatex.MultiColumn(4, data='Перерыв 15 минут! Время чилить и флексить'),)


def compile_seat_name(group_name: str, seat_id: int) -> str:
    return '{}{}'.format(
        group_name,
        seat_id + GROUP_SEATS_NUMBER * (ord(group_name) - ord('A'))
    )


def print_schedule_header(
        document: pylatex.Document,
        group_name: str,
        team: str) -> None:
    document.append('Ваша команда: {}\n'.format(team.replace(' - ', ' — ')))
    document.append('Ваша группа: {}. '.format(group_name))
    document.append('Ваши игры:\n')


def get_who_begins_string(is_first: bool) -> str:
    return 'вы' if is_first else 'не вы'


def draw_schedule_table(
        doc: pylatex.Document,
        schedule: list,
        teams: list,
        rounds_number: int,
        group_size: int,
        team_id: int,
        circles_number: int,
        group_name: str,
        break_time,
    ) -> None:
    with doc.create(pylatex.Tabular('|l|l|l|l|')) as table:
        table.add_hline()
        table.add_row(*SCHEDULE_HEADER)
        table.add_hline()
        total_round_id = 0
        for round_id in range(1, rounds_number + 1):
            total_round_id += 1
            first_team, second_team, seat_id = get_match_info(schedule, round_id, team_id)
            if first_team > group_size or second_team > group_size:
                # Do not play this round, have a rest.
                table.add_row((round_id, 'Вы отдыхаете', '—', '—'))
            else:
                is_first = (first_team == team_id)
                rival_id = second_team if is_first else first_team
                table.add_row((
                    round_id,
                    teams[rival_id-1].replace(' - ', ' — '),
                    compile_seat_name(group_name, seat_id) if round_id > 1 else '',
                    get_who_begins_string(is_first),
                ))
            table.add_hline()
            if total_round_id == break_time:
                table.add_row(BREAK_ROW)
                table.add_hline()
        if circles_number == 1:
            return
        for round_id in range(1, rounds_number + 1):
            total_round_id += 1
            first_team, second_team, seat_id = get_match_info(schedule, round_id, team_id)
            if first_team > group_size or second_team > group_size:
                # Do not play this round, have a rest.
                table.add_row((round_id + rounds_number, 'Вы отдыхаете', '—', '—'))
            else:
                is_first = (first_team == team_id)
                rival_id = second_team if is_first else first_team
                table.add_row((
                    round_id + rounds_number,
                    teams[rival_id-1].replace(' - ', ' — '),
                    compile_seat_name(group_name, seat_id),
                    get_who_begins_string(not is_first),
                ))
            table.add_hline()
            if total_round_id == break_time:
                table.add_row(BREAK_ROW)
                table.add_hline()
        if circles_number == 2:
            return
        for round_id in range(1, rounds_number + 1):
            total_round_id += 1
            first_team, second_team, seat_id = get_match_info(schedule, round_id, team_id)
            if first_team > group_size or second_team > group_size:
                # Do not play this round, have a rest.
                table.add_row((round_id + rounds_number * 2, 'Вы отдыхаете', '—', '—'))
            else:
                is_first = (first_team == team_id)
                rival_id = second_team if is_first else first_team
                table.add_row((
                    round_id + rounds_number * 2,
                    teams[rival_id-1].replace(' - ', ' — '),
                    compile_seat_name(group_name, seat_id),
                    get_who_begins_string(is_first),
                ))
            table.add_hline()
            if total_round_id == break_time:
                table.add_row(BREAK_ROW)
                table.add_hline()


def get_page_capacity(group_size: int, circles_number: int) -> int:
    wrong_group_size_message = 'We suppose group_size as [5, 12]'
    if circles_number == 1:
        if 9 <= group_size <= 12:
            return 3
        elif 7 <= group_size <= 8:
            return 3
        elif 5 <= group_size <= 6:
            return 4
        else:
            raise NotImplementedError(wrong_group_size_message)
    elif circles_number == 2:
        if 11 <= group_size <= 12:
            return 1
        elif 7 <= group_size <= 10:
            return 2
        elif 5 <= group_size <= 6:
            return 3
        else:
            raise NotImplementedError(wrong_group_size_message)
    elif circles_number == 3:
        if 9 <= group_size <= 12:
            return 1
        elif 5 <= group_size <= 8:
            return 2
        else:
            raise NotImplementedError(wrong_group_size_message)
    else:
        raise NotImplementedError('We dunno how to process more 2 circles... Yet :)')


def generate_schedule_doc(
        schedule: list,
        teams: list,
        group_size: int,
        group_name: str,
        circles_number: int,
        rounds_number: int,
        break_time: int,
    ) -> pylatex.Document:
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = pylatex.Document(
        indent=False,
        page_numbers=False,
        geometry_options=geometry_options,
        fontenc='T1,T2C')

    page_capacity = get_page_capacity(rounds_number, circles_number)
    for team_id in range(1, group_size + 1):
        print_schedule_header(doc, group_name, teams[team_id - 1])
        draw_schedule_table(
            doc,
            schedule,
            teams,
            rounds_number,
            group_size,
            team_id,
            circles_number,
            group_name,
            break_time,
        )
        doc.append('\nЖелаем приятно провести время :)')
        if team_id % page_capacity == 0:
            if team_id != group_size:
                doc.append(pylatex.NewPage())
        else:
            doc.append('\n' * 4)
    return doc
