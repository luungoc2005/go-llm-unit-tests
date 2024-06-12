import os
from typing import Iterable

def breadth_first_file_scan(root) -> Iterable[str]:
    """
    This function was obtained from https://stackoverflow.com/questions/49654234/is-there-a-breadth-first-search-option-available-in-os-walk-or-equivalent-py
    It traverses the directory tree in breadth first order.
    """
    dirs = [root]
    # while we has dirs to scan
    while len(dirs):
        next_dirs = []
        for parent in dirs:
            # scan each dir
            for f in os.listdir(parent):
                # if there is a dir, then save for next ittr
                # if it  is a file then yield it (we'll return later)
                ff = os.path.join(parent, f)
                if os.path.isdir(ff):
                    next_dirs.append(ff)
                else:
                    yield ff

        # once we've done all the current dirs then
        # we set up the next itter as the child dirs
        # from the current itter.
        dirs = next_dirs