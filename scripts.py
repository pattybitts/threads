import ret, data_storage, log, copy, re
from cmd import ValidCommands
from Series import Series
from Book import Book
from Chapter import Chapter
from Viewpoint import Viewpoint
from Character import Character

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

if 0:
    booklist = []
    book = Book("Original", 1)
    booklist.append(copy.deepcopy(book))
    book = Book("Edit", 2)
    booklist.append(copy.deepcopy(book))
    log.db("book", booklist[0].title)
    log.db("copied_book", booklist[1].title)

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
        character = series.find_char(cells[1])
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
            character = series.find_char(char_name)
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

if 1:
    series = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    query_list = []
    for character in series.characters:
        if character.tier_value() > 3:
            query_list.append(character)
    for book in series.books:
        for chapter in book.chapters:
            for viewpoint in chapter.viewpoints:
                for character in query_list:
                    





