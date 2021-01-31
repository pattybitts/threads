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

    def process_save_file(self, save_file_name):
        save_data = ds.load_pickle(save_file_name)
        if save_data == ret.ERROR:
            self.alerts.append("ERROR: unable to open save file: " + save_file_name)
            return ret.ERROR
        self.save_file = save_data.name
        self.library_file = save_data.library_file
        self.book_file = save_data.book_file
        self.series_name = save_data.series_name
        self.book_name = save_data.book_name
        self.position = save_data.position
        self.library = ds.load_pickle(self.library_file)
        if self.library is None or self.library == ret.ERROR:
            self.library = Library()
            self.library.save(self.library_file)
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
        scene_locations = lo_form.split("\n") if lo_form != "" else []
        for sl in scene_locations:
            scene.add_location(Location(sl.strip()))
        chapter.add_scene(scene)
        #updating characters with character events
        char_events = ce_form.split("\n") if ce_form != "" else []
        for ce in char_events:
            ce = ce.strip()
            ce_fields = ce.split(";")
            if len(ce_fields) < 4: 
                self.alerts.append("Invalid CE: " + ce)
                continue
            ce_name = ce_fields[0]
            ce_aliases = ce_fields[1].split(",")
            ce_joins = ce_fields[2].split(",")
            ce_tags = ce_fields[3].split(",")
            ce_char = series.match_or_make_char(ce_name, scene)
            if ce_char == ret.ERROR:
                self.alerts.append("Failed to match or make character: " + ce_name)
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
        #adding primary character
        pr_char = series.match_or_make_char(pr_form, scene)
        if pr_char == ret.ERROR:
            self.alerts.append("Failed to match or make character: " + pr_form)
            scene.set_primary(Character("null"))
        else:
            scene.set_primary(pr_char)
        #populating scene included
        #scene quotes
        scene_quotes = qu_form.split("\n") if qu_form != "" else []
        for sq in scene_quotes:
            sq = sq.strip()
            sq_fields = sq.split(",")
            if len(sq_fields) < 2:
                self.alerts.append("Invalid SQ: " + sq)
                continue
            sq_name = sq_fields[0]
            sq_count = int(sq_fields[1])
            sq_char = series.match_or_make_char(sq_name, scene)
            if sq_char == ret.ERROR:
                self.alerts.append("Failed to match or make character: " + sq_name)
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
        scene_features = fe_form.split("\n") if fe_form != "" else []
        for sf in scene_features:
            sf = sf.strip()
            sf_char = series.match_or_make_char(sf, scene)
            if sf_char == ret.ERROR:
                self.alerts.append("Failed to match or make character: " + sf)
                continue
            found_in_included = False
            for i in scene.included:
                if i["character"] == sf_char:
                    i["featured"] = True
                    found_in_included = True
            if not found_in_included:
                scene.included.append({"character": sf_char, "featured": True, "mentions": 0, "quotes": 0})
        #scene mentions
        scene_mentions = me_form.split("\n") if me_form != "" else []
        for sm in scene_mentions:
            sm = sm.strip()
            sm_fields = sm.split(",")
            if len(sm_fields) < 2:
                self.alerts.append("Invalid SM: " + sm)
                continue
            sm_name = sm_fields[0]
            sm_count = int(sm_fields[1])
            sm_char = series.match_or_make_char(sm_name, scene)
            if sm_char == ret.ERROR:
                self.alerts.append("Failed to match or make character: " + sm_name)
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
            self.alerts.append("Failed to find character list for series: " + self.series_name)
            return ret.ERROR
        for c in character_list:
            for a in c.aliases:
                self.known_names.append(a[0])
        return ret.SUCCESS

    def generate_summary(self):
        self.report += "<b>SUMMARY REPORT:</b>\n"
        self.report += "<b>Non-Fatal Alerts:</b>\n"
        for a in self.alerts:
            self.report += a + "\n"
        self.report += "\n<b>Scene Info:</b>\n"
        self.report += self.library_file + "; " + self.series_name + "; " + self.book_name + "\n"
        book = self.library.get_series(self.series_name).get_book(self.book_name)
        chapter = book.chapters[len(book.chapters)-1]
        scene = chapter.scenes[len(chapter.scenes)-1]
        self.report += chapter.name + " (" + str(chapter.placement) + "); Scene #" + str(scene.placement) + "\n"
        self.report += "Perspective: " + scene.primary.name + "; Words: " + str(scene.wordcount) + "\nLocations: "
        for l in scene.locations:
            self.report += l.name + ", "
        self.report = self.report.rstrip(", ")
        self.report += "\n" + scene.description + "\n\n"
        self.report += "<b>Included Characters:</b>\n"
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

    def save_library(self, new_position):
        self.library.save(self.library_file)
        save_file = ds.load_pickle(self.save_file)
        save_file.position = new_position
        save_file.save()
        self.alerts.append("Successfully updated library and save file with new scene!")
        return ret.SUCCESS