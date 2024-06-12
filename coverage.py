import os
import subprocess
import tempfile

AST_BIN_PATH = os.getenv("AST_BIN_PATH", "./ast")

def find_all_files(directory):
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            if file.endswith('.go') and not file.endswith('_test.go'):
                path = os.path.join(root, file)
                path = path.replace("\\", "/")
                yield path

def find_least_coverage(directory):
    directory = os.path.abspath(directory)
    go_mod_file = os.path.join(directory, "go.mod")
    if not os.path.exists(go_mod_file):
        raise ValueError(f"Directory {directory} is not a Go module")
    # get package name
    with open(go_mod_file, 'r') as f:
        lines = f.readlines()
    package = lines[0].split(" ")[1].strip()
    print('Package name:', package)
    # create temporary file
    tmp_file = tempfile.mktemp(".out")
    subprocess.call(["go", "test", "./...", "-coverprofile", tmp_file], cwd=directory)
    with open(tmp_file, 'r') as f:
        # run go test and write the output to the temporary file
        lines = f.readlines()
    os.remove(tmp_file)
    # parse the output
    # the fields are: name.go:line.column,line.column numberOfStatements count
    # https://github.com/golang/go/blob/0104a31b8fbcbe52728a08867b26415d282c35d2/src/cmd/cover/profile.go#L56
    coverage = {}
    for line in lines[1:]:
        parts_1 = line.split(":")
        filename = parts_1[0]

        # get real file name from package name
        if filename.startswith(package):
            filename = filename[len(package)+1:]
            filename = os.path.join(directory, filename)
            filename = filename.replace("\\", "/")

        parts_2 = parts_1[1].split(" ")
        line1, line2 = parts_2[0].split(",")
        line1, line2 = int(line1.split('.')[0]), int(line2.split('.')[0]) # convert to line numbers
        number_of_statements, count = int(parts_2[1]), int(parts_2[2])

        if filename not in coverage:
            coverage[filename] = {
                "total": 0,
                "covered": 0,
                "uncovered": [],
            }
        coverage[filename]["total"] += 1
        if count == 0:
            coverage[filename]["uncovered"].append((line1, line2))
        else:
            coverage[filename]["covered"] += 1
        # print(line1, line2, number_of_statements, count)

    result = {}
    # find all go files in the repository
    for filename in find_all_files(directory):
        print('Counting coverage for', filename)
        result[filename] = {
            'total': 0,
            'covered': 0,
            'uncovered': [],
        }
        if filename in coverage:
            result[filename] = coverage[filename]
    # sort the result by least coverage
    return dict(sorted(result.items(), key=\
        lambda item: item[1]['covered'] / item[1]['total'] 
        if item[1]['total'] > 0 
        else 0, reverse=True))

if __name__ == '__main__':
    REPO_PATH = "./go-querystring"
    coverage = find_least_coverage(REPO_PATH)
    for file, count in coverage.items():
        print(f"{file}: {count}")