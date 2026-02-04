import os as _os

import wonderparse as _wp


def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=file_list,
        prog='filelisting',
        endgame='iterprint',
    )

def file_list(*paths):
    return list(file_generator(*paths))

def file_generator(*paths):
    ans = list()
    for raw_path in paths:
        path = raw_path
        path = _os.path.expanduser(path)
        path = _os.path.expandvars(path)
        if _os.path.isfile(path):
            yield path
            continue
        for (root, dirnames, filenames) in _os.walk(path):
            for filename in filenames:
                file = _os.path.join(root, filename)
                yield file
    
if __name__ == '__main__':
    main() 