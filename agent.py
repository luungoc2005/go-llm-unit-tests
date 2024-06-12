def read_file(path, start_line, end_line):
    with open(path, 'r') as f:
        lines = f.readlines()
    return lines[start_line-1:end_line]

def write_file(path, content, start_line, end_line):
    with open(path, 'r') as f:
        lines = f.readlines()
    lines[start_line-1:end_line] = content
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

