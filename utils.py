def print_field(g):
    line = '+' + '---+' * (len(g)  if isinstance(g, list) else g.field_size)

    field = g if isinstance(g, list) else g.get_field()

    print('Field:')
    print(line)
    for row in field:
        print(end='|')
        for cell in row:
            print('  ' if cell is None else (' X' if cell else ' O'), end=' |')
        print('\n' + line)
