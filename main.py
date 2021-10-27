binary_matrix = lambda n: [[int(k) for k in "{0:b}".format(i).zfill(n)] for i in range(2**n - 1, 0, -1)]

indexes = {
    "init": 0,
    "handle": 2,
    "r#async": 4,
}

keys = list(indexes.keys())
values = list(indexes.values())

def get_arg_section(list, section_name):
    start = indexes.get(section_name)
    if start is not None and len(list) >= start + 2 and list[start] + list[start + 1]:
        tmp = f'{section_name}: '
        section_name = section_name.replace('r#', '')
        if list[start]:
            tmp += f'input: ${section_name[0]}i:ty{", " if list[start + 1] else ""}'
        if list[start + 1]:
            tmp += f'output: ${section_name[0]}o:ty'
        return f'{tmp}{", " if sum(list[start + 2:]) else ""}'
    return ''

def map_notes(row):
    if sum(row) == len(row):
        return 'all'
    notes = 'no '
    for ind, v in enumerate(row):
        notes += f"${keys[values.index(ind // 2 * 2)].replace('r#', '')[0]}{'o' if ind % 2 else 'i'}, " if not v else ""
    return str(notes).removesuffix(', ')

def map_args(row):
    args = 'title: $t:literal, '
    args += get_arg_section(row, 'init')
    args += get_arg_section(row, 'handle')
    args += get_arg_section(row, 'r#async')
    return args

def map_vars(row):
    vars = '$t, '
    suffix = ''
    for ind, v in enumerate(row):
        var = f"${keys[values.index(ind // 2 * 2)].replace('r#', '')[0]}{'o' if ind % 2 else 'i'}"
        if v:
            vars += f"stringify!({var}), "
            suffix += f'{var}, '
        else:
            vars += '"", '
    return (vars + suffix).removesuffix(', ')

def get_macro_case(num, note, args, declaration):
    print(f'// #{num}: {note}')
    print(f'({args}) => ' + '{')
    print(f'    gstd::metadata!({declaration});')
    print('};')

def create_macro(ind, row):
    note = map_notes(row)
    args = map_args(row)
    declaration = map_vars(row)
    get_macro_case(ind + 1, note, args, declaration)

if __name__ == '__main__':
    matrix = binary_matrix(6)
    for ind, row in enumerate(matrix):
        create_macro(ind, row)
