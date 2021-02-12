import util.ret as ret
import util.data_storage as ds
import util.log as log
import util.util as util

from obj.Library import Library
from obj.Series import Series
from obj.Book import Book
from obj.Chapter import Chapter
from obj.Scene import Scene
from obj.Character import Character
from obj.Location import Location
from SaveFile import SaveFile

class SceneImporter:

    def __init__(self):
        self.library = None
        
        self.save_file = ""
        self.library_file = ""
        self.book_file = ""
        self.series_name = ""
        self.book_name = ""
        self.page_start = 0
        self.known_names = []
        self.summary_characters = []
        self.outputs = []

    def process_save_file(self, save_file_name):
        save_data = SaveFile.load(save_file_name)
        if not ret.success(save_data):
            self.log("ERROR: unable to open save file: " + save_file_name)
            return ret.ERROR
        self.save_file = save_data.name
        self.library_file = save_data.library_file
        self.book_file = save_data.book_file
        self.series_name = save_data.series_name
        self.book_name = save_data.book_name
        self.page_start = save_data.page_start
        self.library = Library.load(self.library_file)
        if not ret.success(self.library):
            self.library = Library()
            self.library.save(self.library_file)
        return ret.SUCCESS

    def process_scene_data(self, ch_form: str, pe_form: str, lo_form: str, de_form: str, \
        wo_form: str, me_form: str, qu_form: str, fe_form: str, ce_form: str):
        #finding series
        series = self.library.get_series(self.series_name)
        if series == ret.NOT_FOUND:
            series = Series(self.series_name)
            self.library.add_series(series)
        #finding book
        book = series.get_book(self.book_name)
        if book == ret.NOT_FOUND:
            book = Book(self.book_name, len(series.books)+1)
            series.add_book(book)
        #finding chapter
        chapter = book.find_chapter(ch_form)
        if chapter == ret.NOT_FOUND:
            chapter = Chapter(ch_form, len(book.chapters)+1)
            book.add_chapter(chapter)
        #making new scene
        scene_placement = len(chapter.scenes)+1
        scene_name = chapter.name.lower().replace(" ", "_") + "_" + str(scene_placement)
        scene = Scene(scene_name, scene_placement, wo_form, de_form)
        '''
        Removing location tracking for now, until we add universe + locations
        scene_locations = util.split(lo_form, "\\n")
        for sl in scene_locations:
            scene.add_location(Location(sl.strip()))
        '''
        if chapter.add_scene(scene) == ret.DUPLICATE:
            self.log("NOTE: Duplicate Information in Chapter. Will not add scene.")
            return ret.DUPLICATE
        #updating characters with character events
        char_events = util.split(ce_form, "\\n")
        for ce in char_events:
            ce_fields = ce.split(";")
            if len(ce_fields) != 4: 
                self.log("Invalid CE: " + ce)
                continue
            ce_name = ce_fields[0]
            ce_aliases = ce_fields[1].split(",")
            ce_joins = ce_fields[2].split(",")
            ce_tags = ce_fields[3].split(",")
            ce_char = series.match_or_make_char(ce_name, scene)
            if not ret.success(ce_char):
                self.log("Failed to match or make character: " + ce_name)
                continue
            for ce_a in ce_aliases:
                if ce_a == "": continue
                ce_char.add_alias(ce_a, scene)
            for ce_j in ce_joins:
                if ce_j == "": continue
                join_character = Character.match_character(series.characters, ce_j)
                if not ret.success(join_character):
                    self.log("Cannot find Join for CE: " + ce)
                    continue
                ce_char.add_join(ce_j, scene)
            for ce_t in ce_tags:
                if ce_t == "": continue
                ce_char.add_tag(ce_t, scene)
        #adding perspectives
        perspectives = util.split(pe_form, "\\n")
        for p in perspectives:
            pe_char = Character.match_character(series.characters, p)
            if not ret.success(pe_char):
                self.log("Cannot find character for perspective: " + p)
                continue
            scene.add_perspective(pe_char)
        #populating scene included
        #scene quotes
        scene_quotes = util.split(qu_form, "\\n")
        for sq in scene_quotes:
            sq_fields = sq.split(",")
            if len(sq_fields) != 2:
                self.log("Invalid SQ: " + sq)
                continue
            sq_name = sq_fields[0]
            sq_count = int(sq_fields[1])
            sq_char = series.match_or_make_char(sq_name, scene)
            if not ret.success(sq_char):
                self.log("Failed to match or make character: " + sq_name)
                continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sq_char:
                    i["quotes"] += sq_count
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sq_char, "featured": True, "mentions": 0, "quotes": sq_count})
        #scene features
        scene_features = util.split(fe_form, "\\n")
        for sf in scene_features:
            sf_char = series.match_or_make_char(sf, scene)
            if not ret.success(sf_char):
                self.log("Failed to match or make character: " + sf)
                continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sf_char:
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sf_char, "featured": True, "mentions": 0, "quotes": 0})
        #scene mentions
        scene_mentions = util.split(me_form, "\\n")
        for sm in scene_mentions:
            sm_fields = sm.split(",")
            if len(sm_fields) != 2:
                self.log("Invalid SM: " + sm)
                continue
            sm_name = sm_fields[0]
            sm_count = int(sm_fields[1])
            sm_char = series.match_or_make_char(sm_name, scene)
            if not ret.success(sm_char):
                self.log("Failed to match or make character: " + sm_name)
                continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sm_char:
                    i["mentions"] += sm_count
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sm_char, "featured": False, "mentions": sm_count, "quotes": 0})
        return ret.SUCCESS

    def generate_known_names(self):
        try:
            character_list = self.library.get_series(self.series_name).characters
        except:
            self.log("Failed to find character list for series: " + self.series_name)
            return ret.ERROR
        for c in character_list:
            for a in c.aliases:
                self.known_names.append(a[0])
        return ret.SUCCESS

    def generate_summary(self):
        series = self.library.get_series(self.series_name)
        book = series.get_book(self.book_name)
        chapter = book.chapters[len(book.chapters)-1]
        scene = chapter.scenes[len(chapter.scenes)-1]
        self.log("<b>SUMMARY REPORT:</b>")
        self.log("\n<b>Scene Info:</b>")
        self.log("Save Info: " + self.library_file + "; " + self.save_file)
        self.log("Series Info: " + series.name + "; " + book.name + " (" + str(book.placement) + ")")
        self.log("Chapter: " + chapter.name + " (" + str(chapter.placement) + "); Scene: " + scene.name)
        self.log(scene.print_info())
        return ret.SUCCESS

    def save_library(self, new_page_start):
        self.library.save(self.library_file)
        save_file = SaveFile.load(self.save_file)
        if not ret.success(save_file):
            self.log("Unable to load save file: " + self.save_file)
            return ret.ERROR
        save_file.page_start = new_page_start
        save_file.save()
        self.log("Successfully updated library and save file with new scene!")
        return ret.SUCCESS

    def log(self, input_str):
        self.outputs.append(input_str)

    def print_log(self):
        return util.join(self.outputs, "\n")

    #this is a convenience. be quite careful whenever saving data, as it can cause back pain.
    def script(self):
        series = self.library.get_series(self.series_name)
        book = series.get_book(self.book_name)
        scene = book.find_chapter("Riddles").scenes[1]
        for p in scene.perspectives:
            if p.name == "Gollum\r":
                scene.perspectives.remove(p)
        scene.perspectives.append(Character.match_character(series.characters, "Gollum"))
        self.log(scene.print_info())
        self.library.save(self.library_file)