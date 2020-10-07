#!C:\Users\Peter\Desktop\capstone_pokemon_bci\test-env\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyboy==1.2.5','console_scripts','pyboy'
__requires__ = 'pyboy==1.2.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyboy==1.2.5', 'console_scripts', 'pyboy')()
    )
