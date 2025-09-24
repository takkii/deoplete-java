import gc
import os
import polars as pl
import re
import sys
import traceback
import warnings

from deoplete.source.base import Base
from operator import itemgetter
from typing import Optional

warnings.filterwarnings('ignore')


# GitHub:
class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name: Optional[str] = 'mikiri'
        self.filetypes: Optional[list] = ['java']
        mark_synbol: Optional[str] = '[polars: ' + str(pl.__version__) + ']'
        self.mark: Optional[str] = str(mark_synbol)
        java_match: Optional[list] = [r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*']
        html_match: Optional[list] = [r'[<a-zA-Z(?: .+?)?>.*?<\/a-zA-Z>]']
        self.input_pattern: Optional[str] = '|'.join(java_match + html_match)
        self.rank: Optional[int] = 500

    def get_complete_position(self, context):
        m = re.search('[a-zA-Z0-9_?!]*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            # It doesn't support python4 yet.
            py_mj: Optional[int] = sys.version_info[0]
            py_mi: Optional[int] = sys.version_info[1]

            # 3.5 and higher, 4.x or less,python version is required.
            if (py_mj == 3 and py_mi > 4) or (py_mj < 4):

                # Settings, $HOME/dict path is true/false folder search.
                loc_t: Optional[str] = 'load/java/'

                paths = [
                    os.path.expanduser(os.path.join(p, loc_t)) for p in [
                        '~/GitHub/dict/', '~/.vim/plugged/dict/',
                        '~/.neovim/plugged/dict/'
                    ]
                ]

                path = next(p for p in paths if os.path.exists(p))
                rb_dict: Optional[str] = 'complete.txt'
                rb_mod_fn = os.path.join(path, rb_dict)

                # Get Receiver/mikiri behavior.
                with open(rb_mod_fn) as r_meth:
                    # polars
                    index_java: Optional[list] = list(r_meth.readlines())
                    pl_java = pl.Series(index_java)
                    data = pl_java.sort()
                    data_py: Optional[list] = [s.rstrip() for s in data]

                    # sorted and itemgetter
                    sorted(data_py, key=itemgetter(0))
                    return data_py

            # Python_VERSION: 3.5 or higher and 4.x or less.
            else:
                raise ValueError("VERSION: 3.5 and higher, 4.x or less")

        # TraceBack.
        except Exception:
            # mikiri file path.
            filepath = os.path.expanduser(
                "~/.vim/plugged/mikiri/rplugin/python3/deoplete/sources/java.py"
            )

            basename_without_ext = os.path.splitext(
                os.path.basename(filepath))[0]
            filename = ("deoplete-" + str(basename_without_ext) + "_log")

            # Load/Create LogFile.
            java: Optional[str] = str(filename)
            db_w: Optional[str] = os.path.expanduser('~/' + filename +
                                                     '/debug.log')

            # Load the dictionary.
            if os.path.isdir(java):
                with open(db_w, 'a') as log_py:
                    traceback.print_exc(file=log_py)

                    # throw except.
                    raise RuntimeError from None

            # mikiri_log Foler not found.
            else:
                raise ValueError("None, Please Check the mikiri_log Folder.")

        # Custom Exception.
        except ValueError as ext:
            print(ext)
            raise RuntimeError from None

        # Once Exec.
        finally:
            # GC collection.
            gc.collect()
