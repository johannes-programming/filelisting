import os as _os

import wonderparse as _wp


def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=list_files,
        prog='filelisting',
        endgame='iterprint',
    )

def list_files(*targets):
    ans = list()
    for target in targets:
        if _os.path.isfile(target):
            ans.append(target)
            continue
        for (root, dirnames, filenames) in _os.walk(target):
            for filename in filenames:
                file = _os.path.join(root, filename)
                ans.append(file)
    return ans  
    
if __name__ == '__main__':
    main() 