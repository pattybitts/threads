from flask import Flask, render_template, request, redirect

import util.ret as ret
import util.data_storage as ds
import util.log as log
import util.util as util

from SceneImporter import SceneImporter
from obj.Library import Library
from obj.Series import Series
from obj.Book import Book
from obj.Character import Character
from Query import Query
app = Flask(__name__)

@app.route('/')
def main():
    cmd_out = "Command output will appear here."
    return render_template('index_home.html', cmd_out=cmd_out)
    
@app.route('/cmd_in', methods = ['POST'])
def new_cmd_in():
    save_str = request.form['save_box']
    cmd_str = request.form['cmd_box']
    action, importer = process_cmd(cmd_str, save_str)
    if action == ret.HOME:
        resp = importer.get_output()
        return render_template('index_home.html', cmd_out=resp, cmd_in=cmd_str)
    elif action == ret.EDIT_CHAR:
        #not supported in modern paradigm yet!
        resp = "Not yet supported in modern paradigm!"
        return render_template('index_home.html', cmd_out=resp)
        """
        character = Character.match_character(series.characters, data)
        if character == ret.ERROR:
            error_msg = "INTERNAL ERROR:\nValid character name not found after processing"
            return render_template('index_home.html', cmd_out=error_msg)
        return render_template('index_char_form.html', \
            action="edit", \
            char_name=character.name, \
            char_aliases=character.print_aliases(), \
            char_tier=character.tier, \
            char_gender=character.gender, \
            char_tags=character.print_tags(), \
            char_r=character.color["r"], \
            char_g=character.color["g"], \
            char_b=character.color["b"])
        """
    elif action == ret.ADD_CHAR:
        #not supported in modern paradigm yet!
        resp = "Not yet supported in modern paradigm!"
        return render_template('index_home.html', cmd_out=resp)
        """
        if Character.match_character(series.characters, data, True) != ret.ERROR:
            error_msg = "INTERNAL ERROR:\nCharacter '" + data + "' matched after processing"
            return render_template('index_home.html', cmd_out=error_msg)
        return render_template('index_char_form.html', action="add", char_name=data)
        """
    elif action == ret.GRAPH_TOOL:
        return render_template('index_graph_tool.html', x_val='', y_val='')
    elif action == ret.TEXT_TOOL:
        return render_template('index_text_tool.html', \
            save_file=importer.save_file, \
            book_file=importer.book_file, \
            position=importer.position, \
            known_names=util.join(importer.known_names))
    elif not ret.success(action):
        return render_template('index_home.html', cmd_out=importer.get_output())
    error_msg = "INTERNAL ERROR:\nInvalid return from processing"
    return render_template('index_home.html', cmd_out=error_msg)

@app.route('/char_form_in', methods = ['POST'])
def edit_char():
    #not supported in modern paradigm yet!
    resp = "Not yet supported in modern paradigm!"
    return render_template('index_home.html', cmd_out=resp)
    """
    series = ds.load_pickle(ds.ACTIVE_FILE)
    new_char = Character(request.form['name_box'], \
        request.form['alias_box'], \
        request.form['gender'], \
        request.form['tier_box'], \
        request.form['r_box'], \
        request.form['g_box'], \
        request.form['b_box'], \
        request.form['tag_box'], \
        )
    if request.form['action'] == 'edit':
        if series.replace_char(new_char, request.form['base_name']) != ret.SUCCESS:
            resp = "INTERNAL ERROR:\nUnable to update character " + new_char.name + " in database"
        else:
            resp = "Character " + new_char.name + " successfully updated in database"
            series.save(ds.ACTIVE_FILE)
    elif request.form['action'] == 'add':
        if series.add_char(new_char) != ret.SUCCESS:
            resp = "INTERNAL ERROR:\nUnable to add character " + new_char.name + " in database"
        else:
            resp = "Character " + new_char.name + " successfully added to database"
            series.save(ds.ACTIVE_FILE)
    return render_template('index_home.html', cmd_out=resp)
    """

@app.route('/generate_summary', methods = ['POST'])
def generate_summary():
    #there's room to do this more sanely with ONE output stream
    importer = SceneImporter()
    status = importer.process_save_file(request.form['sf_form'])
    if status == ret.SUCCESS:
        status = importer.process_scene_data(request.form['ch_form'], request.form['pr_form'], \
            request.form['lo_form'], request.form['de_form'], \
            request.form['wo_form'], request.form['me_form'], \
            request.form['qu_form'], request.form['fe_form'], \
            request.form['ce_form'])
    if status == ret.SUCCESS:
        status = importer.generate_summary()
    if status == ret.SUCCESS:
        resp = importer.report
    else:
        resp = "ERROR: FAILED TO IMPORT"
        for a in importer.outputs:
            resp += "\n" + a

    if request.form['ss_form'] == "saved":
        status = importer.save_library(request.form['po_form'])
        if status == ret.SUCCESS:
            resp = importer.report
            return render_template('index_text_tool.html', \
                save_status="saved", \
                save_file=request.form['sf_form'], \
                book_file=request.form['bf_form'], \
                known_names=request.form['kn_form'], \
                log=request.form['lg_form'], \
                position=request.form['po_form'], \
                report=resp)

    return render_template('index_text_tool.html', \
        save_status="reviewing", \
        save_file=request.form['sf_form'], \
        book_file=request.form['bf_form'], \
        known_names=request.form['kn_form'], \
        log=request.form['lg_form'], \
        position=request.form['po_form'], \
        chapter=request.form['ch_form'], \
        primary=request.form['pr_form'], \
        locations=request.form['lo_form'], \
        description=request.form['de_form'], \
        wordcount=request.form['wo_form'], \
        mentions=request.form['me_form'], \
        quotes=request.form['qu_form'], \
        features=request.form['fe_form'], \
        char_events=request.form['ce_form'], \
        report=resp)

"""
@app.route('/new_graph', methods = ['POST'])
def new_graph():
    filter_text = str.strip(request.form['filter_box'])
    filters = filter_text.split("\n")
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']
    query = Query(x_axis, y_axis, filters)
    query.make_query_list()
    return render_template('index_graph_tool.html', x_val=x_axis, y_val=y_axis, query_output=query.query_log, filter_text=filter_text)
"""

def process_cmd(cmd_str, save_str):
    importer = SceneImporter()
    cmd_parts = util.split(cmd_str, '=')
    if len(cmd_parts) < 1:
        importer.outputs.append("No command entry in: " + cmd_str)
        return ret.ERROR, importer
    status = importer.process_save_file(save_str)
    if not ret.success(status):
        importer.outputs.append("Unable to import save file: " + save_str)
        return ret.ERROR, importer
    if cmd_parts[0] == 'disp_char':
        if len(cmd_parts) < 2: 
            importer.outputs.append("No character name provided in: " + cmd_str)
            return ret.BAD_INPUT, importer
        series = importer.library.get_series(importer.series_name)
        character = Character.match_character(series.characters, cmd_parts[1])
        #and now this is where loose is needed (future TODO)
        if not ret.success(character):
            importer.outputs.append("Unable to match character: " + cmd_parts[1])
            return ret.ERROR, importer
        importer.outputs.append(character.print_info())
        return ret.HOME, importer
    if cmd_parts[0] == 'disp_chapter':
        if len(cmd_parts) < 2: 
            importer.outputs.append("No chapter name provided in: " + cmd_str)
            return ret.BAD_INPUT, importer
        book = importer.library.get_series(importer.series_name).get_book(importer.book_name)
        chapter = book.find_chapter(cmd_parts[1])
        if not ret.success(chapter):
            importer.outputs.append("Unable to find chapter: " + cmd_parts[1])
            return ret.ERROR, importer
        importer.outputs.append(chapter.print_info())
        for s in chapter.scenes:
            importer.outputs.append(s.print_info())
        return ret.HOME, importer
    """
    This all to be updated and added once we have our text tool functioning
    if cmd_parts[0] == 'add_char':
        character = Character.match_character(series.characters, cmd_parts[1], True)
        if character == ret.ERROR:
            return ret.ADD_CHAR, cmd_parts[1]
        return ret.ERROR, "Duplicate character with name: " + character.name \
            + "\nuse the 'edit_char' command to overwrite"
    if cmd_parts[0] == 'edit_char':
        character = Character.match_character(series.characters, cmd_parts[1])
        if character == ret.ERROR:
            return ret.ERROR, "Unable to match character name: " + cmd_parts[1]
        return ret.EDIT_CHAR, character.name
    if cmd_parts[0] == 'list_chars':
        msg = "Character List:\n"
        for c in series.characters:
            msg += c.name + "\n"
        msg.rstrip()
        return ret.HOME, msg
    if cmd_parts[0] == 'gen_archive':
        archive = open("data\\wot_archive.txt", 'wb')
        for c in series.characters:
            archive.write(bytearray(c.print_info(), 'utf-8'))
            archive.write(bytearray("\n\n", 'utf-8'))
        for b in series.books:
            archive.write(bytearray("(Book) " + b.title + " (" + str(b.number) + ")\n\n", 'utf-8'))
            for c in b.chapters:
                archive.write(bytearray(c.print_chapter() + "\n", 'utf-8'))
        archive.close()
        msg = "Generated archive file at data\\wot_archive.txt"
        return ret.HOME, msg
    if cmd_parts[0] == 'graph_tool':
        msg = ""
        return ret.GRAPH_TOOL, msg
    """
    if cmd_parts[0] == 'text_tool':
        status = importer.generate_known_names()
        return ret.TEXT_TOOL, importer
    return ret.ERROR, "Unsupported command entry: " + cmd_string
    
if __name__ == '__main__':
    app.run()