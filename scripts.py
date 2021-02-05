import copy, re

import util.data_storage as ds
import util.log as log
import util.util as util

from obj.Library import Library
from obj.Series import Series
from obj.Character import Character
from SaveFile import SaveFile

#testing new util.strip method
if 0:
    test_str = ","
    test_arr = util.split(test_str, ",")
    log.out(str(test_arr))

#reading save file (this should be in home.py!!)
if 0:
    save_file = ds.load_pickle("data\\eotw.sav")
    log.out(save_file.print())

#creating a new save file
if 1:
    save_file = SaveFile("data\\eotw.sav", "static/eotw_shortened.txt", "data\\library_2_5", "The Wheel of Time", "The Eye of the World", 0)
    log.out(save_file.print_info())
    save_file.save()

#getting library object and info
if 0:
    library = ds.load_pickle("data\\library_1_19")
    log.out(library.get_info())

#creating new library object
if 0:
    new_library = Library()
    log.out(new_library.get_info())
    new_library.save("data\\library_1_19")

#playing around with opening/reading save files
if 0:
    try:
        input = open("data\\eotw.sav", 'r')
        sav_text = input.read()
    except:
        log.banner("Failed to read input file")
    not_names = ds.create_array(sav_text, "not_names")
    log.banner(str(not_names[0]))

#object recreation with new structure
if 0:
    old_series = ds.load_pickle("data\\wot_0")
    new_series = Series("The Wheel of Time")
    for c in old_series.characters:
        log.out(c.print_info())
        new_char = Character(c.name, c.print_aliases(), c.gender, c.color["r"], c.color["g"], c.color["b"], c.print_tags())
        new_series.add_char(copy.copy(new_char))
    new_series.save("data\\wot_0")

#we'll use this as our working template for imports?
if 0:
    import util.log as log
    from obj.TestClass import TestClass
    tc = TestClass()
    log.banner(tc.print())

#parsing eotw txt to remove extra whitespace
#NOTE: modified again to reformat two in stunning_journey
if 0:
    input = open("input_files\\Two", 'r')
    full_text = input.read()
    mod_text = re.sub("\s*\n\n+\s*", "\n", full_text, 1000000)
    mod_text = re.sub("[.?!]\s+", ".\n", full_text, 1000000)
    output = open("input_files\\Two", 'wb')
    output.write(bytearray(mod_text, 'utf-8'))
    output.close()

#trying to test how python manages pointers in circular references
if 0:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    log.banner(series.books[0])

#character object cleanup
if 0:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    new_series = Series()
    new_series.books = series.books
    new_characters = []
    n_lit = "\n"
    for c in series.characters:
        new_character = Character(c.name, n_lit.join(c.aliases), c.gender, c.tier, c.color["r"], c.color["g"], c.color["b"], n_lit.join(c.tags))
        new_characters.append(copy.copy(new_character))
    new_series.characters = new_characters
    new_series.save(data_storage.ACTIVE_FILE)

if 0:
    print(str.isnumeric("35"))

if 0:
    filter_list = ["name>=rand"]
    query = Query("x_characters", "y_wordcount", filter_list)
    query.make_query_list()
    log.banner(query.query_log)

#object cleanup - load saved object, then rebuild with constructors
if 0:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    eotw = data_storage.load_pickle("data\\eotw")
    new_series = Series()
    new_series.add_book(eotw)
    new_series.characters = series.characters
    new_series.save(data_storage.ACTIVE_FILE)

#preliminary query test - display featured word counts for S, A, B characters
if 0:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    query_list = []
    wordcounts = {}
    for character in series.characters:
        if Character.tier_value(character.tier) > 2:
            query_list.append(character)
            wordcounts[character.name] = 0
    for book in series.books:
        for chapter in book.chapters:
            for viewpoint in chapter.viewpoints:
                for character in query_list:
                    if viewpoint.is_featured(character.name):
                        wordcounts[character.name] += int(viewpoint.wordcount)
    log.banner("Character Featured Word Counts, Tier B and Higher, Eye of the World")
    for x in wordcounts:
        log.out(x + ": " + str(wordcounts[x]))

#import book, viewpoints, words, characters to series class
if 0:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    input = open("eotw.txt", 'r')
    full_text = input.read()
    lines = full_text.split("\n")
    book = Book("Eye of the World", 1)
    ch_count = 0
    vp_count = 0
    chapter = None
    for line in lines:
        cells = line.split(",")
        num_cells = len(cells)
        character = Character.match_character(series.characters, cells[1])
        ch_name = cells[0]
        if ch_name != '':
            vp_count = 1
        else:
           vp_count += 1
        if character == ret.ERROR:
            log.out("Unable to locate character: " + cells[1])
            continue
        viewpoint = Viewpoint(vp_count, character, cells[2])
        for i in range(3, num_cells):
            char_name = cells[i]
            if char_name == '':
                break
            character = Character.match_character(series.characters, char_name)
            if character == ret.ERROR:
                log.out("Unable to locate character: " + cells[i])
                continue
            viewpoint.add_featured(copy.copy(character))
        #at this point the viewpoint object is complete
        if ch_name != '':
            if not chapter is None:
                book.add_chapter(copy.copy(chapter))
            vp_re = re.match("(\S+): (.*)", str(cells[0]))
            if not vp_re:
                log.out("Unable to match chapter name: " + str(cells[0]))
                continue
            if vp_re.group(1) == "Prologue":
                ch_count = 0
                ch_title = vp_re.group(0)
            else:
                ch_count += 1
                ch_title = vp_re.group(2)
            chapter = Chapter(ch_title, ch_count)
        if not chapter is None:
            chapter.add_viewpoint(copy.copy(viewpoint))
    book.add_chapter(copy.copy(chapter))
    for ch in book.chapters:
        log.out(ch.print_chapter())
    series.save("wot")
    data_storage.dump_pickle(book, "eotw")

#deepcopy test
if 0:
    booklist = []
    book = Book("Original", 1)
    booklist.append(copy.deepcopy(book))
    book = Book("Edit", 2)
    booklist.append(copy.deepcopy(book))
    log.db("book", booklist[0].title)
    log.db("copied_book", booklist[1].title)
    
#eliminate allegiance property and instead add "Darkfriend" tag to shadow allies
if 0:
    series_info = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    new_series_info = Series()
    for c in series_info.characters:
        new_char = Character(c.name, c.print_aliases(), c.gender, c.tier, c.color["r"], c.color["g"], c.color["b"], c.print_tags())
        if c.allegiance == "Shadow":
            new_char.tags.append("Darkfriend")
        new_series_info.add_char(new_char)
    new_series_info.save("wot_0")