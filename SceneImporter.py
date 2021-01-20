import util.ret as ret
import util.data_storage as ds
import util.log as log

from obj.Library import Library
from obj.Series import Series
from obj.Book import Book

class SceneImporter:

    def __init__(self):
        self.library = None
        
        self.save_file = ""
        self.library_file = ""
        self.book_file = ""
        self.series_name = ""
        self.book_name = ""

    def process_save_file(self, save_file):
        data = self.extract_save_data(save_file)
        if data == ret.ERROR:
            return ret.ERROR
        self.library_file = data["library_file"]
        self.book_file = data["book_file"]
        self.series_name = data["series_name"]
        self.book_name = data["book_name"]
    
        self.library = ds.load_pickle(self.library_file)
        if self.library == ret.ERROR or self.library == None:
            self.library = Library()

        series = self.library.get_series(self.series_name)
        if series == ret.ERROR:
            series = Series(self.series_name)
            #assuming adding a series will be byref
            self.library.add_series(series)

        book = series.get_book(self.book_name)
        if book == ret.ERROR:
            book = Book(self.book_name, len(series.books)+1)
            series.add_book(book)

        return ret.SUCCESS

    def extract_save_data(self, save_file_name: str):
        #TODO i need to be more intelligent with my exeptions for try/catch
        try:
            input = open("data\\" + save_file_name, 'r')
            sav_text = input.read()
            data = {}
            data["save_file"] = ds.create_array(sav_text, "save_file")[0]
            data["book_file"] = ds.create_array(sav_text, "book_file")[0]
            data["library_file"] = ds.create_array(sav_text, "library_file")[0]
            data["series_name"] = ds.create_array(sav_text, "series_name")[0]
            data["book_name"] = ds.create_array(sav_text, "book_name")[0]
            data["position"] = ds.create_array(sav_text, "position")[0]
            data["known_names"] = ",".join(ds.create_array(sav_text, "known_names"))
        except:
            return ret.ERROR
        return data