import util.ret as ret
import util.data_storage as ds
import util.log as log
import util.util as util

from obj.Library import Library

class Analysis:

    def __init__(library_file):
        self.library = Library.load(library_file)

    def generate_book_report(book_name):
        pass
        