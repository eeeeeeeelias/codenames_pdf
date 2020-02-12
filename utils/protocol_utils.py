import pylatex


COMMAND_NUMBER_WIDTH = '2mm'
RESULT_CELL_WIDTH = '6mm'


def get_protocol_header_row(group_size) -> tuple:
    return (
        pylatex.MultiRow(1, width=COMMAND_NUMBER_WIDTH),  # Team number
        pylatex.MultiRow(1, width='40mm'), # Team
        *[i+1 for i in range(group_size)], # (rivals)
        'Победы',                          # Wins
        '+',                               # Scored
        '—',                               # Conceeded
        '+/—',                             # Difference
        'Фолы',                            # Fouls
        'Место'                            # Place
    )


def draw_protocol_table(
        doc: pylatex.Document,
        teams: list,
        group_size: int,
        circles_number: int,
    ) -> None:
    header_string = '|c|l|{games}||c||{details}'.format(
        games='|c' * group_size,
        details='c|' * 5,
    )
    with doc.create(pylatex.Tabular(header_string)) as table:
        table.add_hline()
        table.add_row(*get_protocol_header_row(group_size))
        table.add_hline()
        for team_id in range(1, group_size + 1):
            team_first, team_second = map(str.strip, teams[team_id-1].split(' - '))
            if circles_number > 1:
                result_cell = pylatex.MultiRow(1, width=RESULT_CELL_WIDTH)
            else:
                result_cell = pylatex.MultiRow(2, width=RESULT_CELL_WIDTH)
            white_cell = pylatex.MultiRow(max(2, circles_number), width=RESULT_CELL_WIDTH)
            self_result_cell = pylatex.MultiRow(1, width=RESULT_CELL_WIDTH, color='gray')
            table.add_row((
                pylatex.MultiRow(max(2, circles_number), data=team_id, width=COMMAND_NUMBER_WIDTH),
                team_first,
                *[result_cell for i in range(team_id - 1)],
                self_result_cell,
                *[result_cell for i in range(group_size - team_id)],
                *[white_cell for i in range(6)],
            ))
            if circles_number > 1:
                table.add_hline(3, 3 + group_size - 1)
            table.add_row((
                '',
                team_second,
                *['' for i in range(team_id - 1)],
                self_result_cell,
                *['' for i in range(team_id, group_size)],
                *['' for i in range(6)],
            ))
            if circles_number == 3:
                table.add_hline(3, 3 + group_size - 1)
                table.add_row((
                    '',
                    '',
                    *['' for i in range(team_id - 1)],
                    self_result_cell,
                    *['' for i in range(team_id, group_size)],
                    *['' for i in range(6)],
                ))
            table.add_hline()


def generate_protocol_doc(
        teams: list,
        group_size: int,
        group_name: str,
        circles_number: int,
    ) -> pylatex.Document:
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = pylatex.Document(
        indent=False, page_numbers=False, geometry_options=geometry_options, fontenc='T1,T2C')
    doc.documentclass = pylatex.Command(
        'documentclass',
        options=['landscape'],
        arguments=['article'],
    )

    doc.append('Протокол группы {}\n\n'.format(group_name))
    draw_protocol_table(doc, teams, group_size, circles_number)
    return doc
