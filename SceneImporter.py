import util.ret as ret
import util.data_storage as ds
import util.log as log

from obj.Library import Library
from obj.Series import Series
from obj.Book import Book
from obj.Chapter import Chapter
from obj.Scene import Scene
from obj.Character import Character
from obj.Location import Location

class SceneImporter:

    def __init__(self):
        self.library = None
        
        self.save_file = ""
        self.library_file = ""
        self.book_file = ""
        self.series_name = ""
        self.book_name = ""
        self.position = 0
        self.known_names = []
        self.summary_characters = []
        self.alerts = []

    def process_save_file(self, save_file_name: str, tool_position=-1):
        #I NEED to clean this try_catch atrocity
        try:
            input = open("data\\" + save_file_name, 'r')
            sav_text = input.read()
        except:
            return ret.ERROR
        self.save_file = ds.create_array(sav_text, "save_file")[0]
        self.library_file = ds.create_array(sav_text, "library_file")[0]
        self.book_file = ds.create_array(sav_text, "book_file")[0]
        self.series_name = ds.create_array(sav_text, "series_name")[0]
        self.book_name = ds.create_array(sav_text, "book_name")[0]
        #I think this is where we'd like to overwrite save file?
        if int(tool_position) >= 0:
            self.position = tool_position
        else:
            self.position = ds.create_array(sav_text, "position")[0]
        return ret.SUCCESS

    def process_scene_data(self, ch_form: str, pr_form: str, lo_form: str, de_form: str, \
        wo_form: str, me_form: str, qu_form: str, ce_form: str):
        #finding library
        self.library = ds.load_pickle(self.library_file)
        if self.library == ret.ERROR or self.library == None:
            self.library = Library()
        #finding series
        series = self.library.get_series(self.series_name)
        if series == ret.ERROR:
            series = Series(self.series_name)
            self.library.add_series(series)
        #finding book
        book = series.get_book(self.book_name)
        if book == ret.ERROR:
            book = Book(self.book_name, len(series.books)+1)
            series.add_book(book)
        #finding chapter
        chapter = book.get_chapter(ch_form)
        if chapter == ret.ERROR:
            chapter = Chapter(ch_form, len(book.chapters)+1)
            book.add_chapter(chapter)
        #making new scene
        scene_placement = len(chapter.scenes)+1
        scene_name = chapter.name + "_" + str(scene_placement)
        scene = Scene(scene_name, scene_placement, wo_form, pr_form, de_form)
        scene_locations = lo_form.split()
        for sl in scene_locations:
            scene.add_location(Location(sl))
        #updating characters with character events
        char_events = ce_form.split()
        for ce in char_events:
            ce_fields = ce.split(";")
            if len(ce_fields) < 4: 
                self.alerts.append("Invalid CE: " + ce)
                continue
            ce_name = ce_fields[0]
            ce_aliases = ce_fields[1].split(",")
            ce_joins = ce_fields[2].split(",")
            ce_tags = ce_fields[3].split(",")
            character = Character.match_character(series.characters, ce_name)
            if character == ret.ERROR:
                character = Character(ce_name)
                character.add_alias(ce_name, scene)
                if not series.add_character(character): 
                    self.alerts.append("Failed to add character for CE: " + ce)
                    continue
            for ce_a in ce_aliases:
                character.add_alias(ce_a, scene)
            for ce_j in ce_joins:
                join_character = Character.match_character(series.characters, ce_j)
                if join_character == ret.ERROR:
                    self.alerts.append("Cannot find Join for CE: " + ce)
                    continue
                character.add_join(ce_j, scene)
            for ce_t in ce_tags:
                character.add_tag(ce_t, scene)
            #first time using 'in' like this, somewhat dubious
            if not character in self.summary_characters: self.summary_characters.append(character)
        #populating scene included
        included = []
        scene_mentions = me_form.split()
        for sm in scene_mentions:
            sm_fields = sm.split(",")
            if len(sm_fields) < 2:
                self.alerts.append("Invalid SM: " + sm)
                continue
            sm_name = sm_fields[0]
            sm_count = int(sm_fields[1])
            sm_char = Character.match_character(series.characters, sm_name)
            if sm_char == ret.ERROR:
                character = Character(sm_name)
                character.add_alias(sm_name, scene)
                if not series.add_character(character):
                    self.alerts.append("Failed to add character for SM: " + sm)
                    continue
            found_in_included = False
            for i in included:
                if i["character"] == sm_char:
                    i["mentions"] += sm_count
                    found_in_included = True
            if not found_in_included:
                included.append({"character": sm_char, "featured": False, "mentions": sm_count, "quotes": 0})
            if not sm_char in self.summary_characters: self.summary_characters.append(sm_char)
        #just noting here, we could methodize this (it would be shorter, not neater I think)
        scene_quotes = qu_form.split()
        for sq in scene_quotes:
            sq_fields = sq.split(",")
            if len(sq_fields) < 2:
                self.alerts.append("Invalid SQ: " + sq)
                continue
            sq_name = sq_fields[0]
            sq_count = int(sq_fields[1])
            sq_char = Character.match_character(series.characters, sq_name)
            if sq_char == ret.ERROR:
                character = Character(sq_name)
                character.add_alias(sq_name, scene)
                if not series.add_character(character):
                    self.alerts.append("Failed to add character for SQ: " + sq)
                    continue
            found_in_included = False
            for i in included:
                if i["character"] == sq_char:
                    i["quotes"] += sm_count
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                included.append({"character": sq_char, "featured": True, "mentions": 0, "quotes": sq_count})
            if not sq_char in self.summary_characters: self.summary_characters.append(sq_char)
        #creating updated known_names
        for c in series.characters:
            for a in c.aliases:
                self.known_names.append(a[0])
        return ret.SUCCESS