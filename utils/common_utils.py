"""Additional functions for protocol and schedule methods."""

MAX_CIRCLES_NUMBER = 3
MAX_GROUPS_NUMBER = 4

def get_teams_list(teams_file):
    """Read list of strings 'First participant - second participant' from teams_file."""
    teams_list = []
    with open(teams_file, 'r') as f_in:
        for line in f_in:
            teams_list.append(line.strip())
    return teams_list


def read_group_name() -> str:
    """Read group name (A, B ... MAX_GROUPS_NUMBER) from standard input."""
    while True:
        group_name = input(
            'Введите номер группы (A..{}): '.format(
                chr(ord('A') + MAX_GROUPS_NUMBER - 1)
            )
        )
        if group_name.upper() not in set(
                chr(ord('A') + i) for i in range(MAX_GROUPS_NUMBER)
        ):
            continue
        else:
            return group_name.upper()

def read_group_size() -> int:
    """Read size of group from standard input."""
    while True:
        group_size = input('Введите число команд в группе: ')
        if not group_size.isdigit():
            continue
        else:
            return int(group_size)

def read_circles_number() -> int:
    """Read number of round-robin circles (1, ..., MAX_CIRCLES_NUMBER) from standard input."""
    while True:
        circles_number = input('Введите количество кругов: ')
        if not circles_number.isdigit():
            continue
        elif not 1 <= int(circles_number) <= MAX_CIRCLES_NUMBER:
            continue
        else:
            return int(circles_number)


def read_break_time(rounds_number: int, circles_number: int) -> int:
    """Read index of round you want to claim a break from standard input."""
    break_time_input_help_string = (
        'Введите через пробел тур, после которого нужно сделать перерыв'
        '\n(0 -- без перерыва): ')
    while True:
        break_time = input(break_time_input_help_string)
        if not break_time.isdigit():
            continue
        break_time = int(break_time)
        if not 0 <= break_time <= rounds_number * circles_number - 1:
            continue
        return break_time


def get_match_info(schedule: list, round_id: int, team_id: int) -> (int, int, int):
    """Return 1st team id, 2nd team id, seat number"""
    first_team, second_team = -1, -1
    for game in schedule[str(round_id)]:
        if game['first'] == team_id and game['second'] == team_id:
            raise Exception('You cannot play with yourself')
        elif game['first'] == team_id or game['second'] == team_id:
            if first_team != -1 or second_team != -1:
                raise Exception('No more than one game in one round')
            first_team, second_team = game['first'], game['second']
            seat_id = game['seat']
        else:
            continue
    if first_team == -1 or second_team == -1:
        raise Exception('You need to have a rival')
    return first_team, second_team, seat_id
