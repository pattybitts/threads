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
        self.report = ""

    def process_save_file(self, save_file_name: str, tool_position=-1):
        #I NEED to clean this try_catch atrocity
        try:
            input = open("data\\" + save_file_name, 'r')
            sav_text = input.read()
        except:
            self.alerts.append("ERROR: unable to open save file: save_file_name")
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
        wo_form: str, me_form: str, qu_form: str, fe_form: str, ce_form: str):
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
        scene_name = chapter.name.lower().replace(" ", "_") + "_" + str(scene_placement)
        scene = Scene(scene_name, scene_placement, wo_form, de_form)
        pr_char = Character.match_character(series.characters, pr_form)
        if pr_char == ret.ERROR:
            pr_char = Character(pr_form)
            pr_char.add_alias(pr_form, scene)
            if not series.add_character(pr_char): 
                self.alerts.append("Failed to add character for PR: " + pr_form)
        scene.set_primary(pr_char)
        scene_locations = lo_form.split("\n")
        for sl in scene_locations:
            scene.add_location(Location(sl))
        chapter.add_scene(scene)
        #updating characters with character events
        char_events = ce_form.split("\n")
        for ce in char_events:
            ce_fields = ce.split(";")
            if len(ce_fields) < 4: 
                self.alerts.append("Invalid CE: " + ce)
                continue
            ce_name = ce_fields[0]
            ce_aliases = ce_fields[1].split(",")
            ce_joins = ce_fields[2].split(",")
            ce_tags = ce_fields[3].split(",")
            ce_char = Character.match_character(series.characters, ce_name)
            if ce_char == ret.ERROR:
                ce_char = Character(ce_name)
                ce_char.add_alias(ce_name, scene)
                if not series.add_character(ce_char): 
                    self.alerts.append("Failed to add character for CE: " + ce)
                    continue
            for ce_a in ce_aliases:
                if ce_a == "": continue
                ce_char.add_alias(ce_a, scene)
            for ce_j in ce_joins:
                if ce_j == "": continue
                join_character = Character.match_character(series.characters, ce_j)
                if join_character == ret.ERROR:
                    self.alerts.append("Cannot find Join for CE: " + ce)
                    continue
                ce_char.add_join(ce_j, scene)
            for ce_t in ce_tags:
                if ce_t == "": continue
                ce_char.add_tag(ce_t, scene)
            #first time using 'in' like this, somewhat dubious
            #if not ce_char in self.summary_characters: self.summary_characters.append(character)
        #populating scene included
        scene.included = []
        scene_mentions = me_form.split("\n")
        for sm in scene_mentions:
            sm_fields = sm.split(",")
            if len(sm_fields) < 2:
                self.alerts.append("Invalid SM: " + sm)
                continue
            sm_name = sm_fields[0]
            sm_count = int(sm_fields[1])
            sm_char = Character.match_character(series.characters, sm_name)
            if sm_char == ret.ERROR:
                sm_char = Character(sm_name)
                sm_char.add_alias(sm_name, scene)
                if not series.add_character(sm_char):
                    self.alerts.append("Failed to add character for SM: " + sm)
                    continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sm_char:
                    i["mentions"] += sm_count
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sm_char, "featured": False, "mentions": sm_count, "quotes": 0})
            #if not sm_char in self.summary_characters: self.summary_characters.append(sm_char)
        #just noting here, we could methodize this (it would be shorter, not neater I think)
        scene_quotes = qu_form.split("\n")
        for sq in scene_quotes:
            sq_fields = sq.split(",")
            if len(sq_fields) < 2:
                self.alerts.append("Invalid SQ: " + sq)
                continue
            sq_name = sq_fields[0]
            sq_count = int(sq_fields[1])
            sq_char = Character.match_character(series.characters, sq_name)
            if sq_char == ret.ERROR:
                sq_char = Character(sq_name)
                sq_char.add_alias(sq_name, scene)
                if not series.add_character(sq_char):
                    self.alerts.append("Failed to add character for SQ: " + sq)
                    continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sq_char:
                    i["quotes"] += sm_count
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sq_char, "featured": True, "mentions": 0, "quotes": sq_count})
            #if not sq_char in self.summary_characters: self.summary_characters.append(sq_char)
        scene_features = fe_form.split("\n")
        for sf in scene_features:
            sf_char = Character.match_character(series.characters, sf)
            if sf_char == ret.ERROR:
                sf_char = Character(sf_char)
                sf_char.add_alias(sf_char.name, scene)
                if not series.add_character(sf_char):
                    self.alerts.append("Failed to add character for SF: " + sf)
                    continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sf_char:
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sf_char, "featured": True, "mentions": 0, "quotes": 0})
            #if not sf_char in self.summary_characters: self.summary_characters.append(sf_char)
            
        return ret.SUCCESS

    def generate_known_names(self):
        try:
            character_list = self.library.get_series(self.series_name).characters
        except:
            self.alerts.append("Failed to find character list for series: " + self.series_name)
            return ret.ERROR
        for c in character_list:
            for a in c.aliases:
                self.known_names.append(a[0])
        return ret.SUCCESS

    def generate_summary(self):
        self.report += "SUMMARY REPORT:\n"
        self.report += "Non-Fatal Alerts:\n"
        for a in self.alerts:
            self.report += a + "\n"
        self.report += "\nScene Info:\n"
        self.report += self.library_file + "; " + self.series_name + "; " + self.book_name + "\n"
        book = self.library.get_series(self.series_name).get_book(self.book_name)
        chapter = book.chapters[len(book.chapters)-1]
        scene = chapter.scenes[len(chapter.scenes)-1]
        self.report += chapter.name + " (" + str(chapter.placement) + "); Scene #" + str(scene.placement) + "\n"
        self.report += "Prespective: " + scene.primary.name + "; Words: " + str(scene.wordcount) + "\nLocations: "
        for l in scene.locations:
            self.report += l.name + ", "
        self.report += "\n" + scene.description + "\n\n"
        self.report += "Included Characters:\n"
        for i in scene.included:
            character = i["character"]
            featured_str = "Featured" if i["featured"] else "Mentioned"
            self.report += character.name + " (" + featured_str + ", Words: " + str(i["quotes"]) + ", Calls: " + str(i["mentions"]) + ")\n"
            for a in character.aliases:
                if a[1] == scene:
                    self.report += "New Alias: " + a[0] + "\n"
            for j in character.joins:
                if j[1] == scene:
                    self.report += "New Join: " + j[0].name + "\n"
            for t in character.tags:
                if t[1] == scene:
                    self.report += "New Tag: " + t[0] + "\n"
            self.report += "\n"
        return ret.SUCCESS