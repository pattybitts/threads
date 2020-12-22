from flask import Flask, render_template, request, redirect

import util.ret as ret
import util.data_storage as ds
import util.log as log

from obj.Series import Series
from obj.Character import Character
from Query import Query
app = Flask(__name__)

@app.route('/')
def main():
    cmd_out = "Command output will appear here."
    return render_template('index_home.html', cmd_out=cmd_out)
    
@app.route('/cmd_in', methods = ['POST'])
def new_cmd_in():
    series = ds.load_pickle(ds.ACTIVE_FILE)
    cmd_string = request.form['cmd_box']
    action, data = process_cmd(cmd_string)
    if action == ret.HOME:
        return render_template('index_home.html', cmd_out=data)
    elif action == ret.EDIT_CHAR:
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
            char_tags=character.print_tags(),
            char_r=character.color["r"], \
            char_g=character.color["g"], \
            char_b=character.color["b"])
    elif action == ret.ADD_CHAR:
        if Character.match_character(series.characters, data, True) != ret.ERROR:
            error_msg = "INTERNAL ERROR:\nCharacter '" + data + "' matched after processing"
            return render_template('index_home.html', cmd_out=error_msg)
        return render_template('index_char_form.html', action="add", char_name=data)
    elif action == ret.GRAPH_TOOL:
        return render_template('index_graph_tool.html', x_val='', y_val='')
    elif action == ret.TEXT_TOOL:
        return render_template('index_text_tool.html', book_file=data["book_file"], position=data["position"], known_names=data["known_names"])
    elif action == ret.ERROR:
        error_msg = str(data)
        return render_template('index_home.html', cmd_out=error_msg)
    error_msg = "INTERNAL ERROR:\nInvalid return from processing"
    return render_template('index_home.html', cmd_out=error_msg)

@app.route('/char_form_in', methods = ['POST'])
def edit_char():
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

@app.route('/new_graph', methods = ['POST'])
def new_graph():
    filter_text = str.strip(request.form['filter_box'])
    filters = filter_text.split("\n")
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']
    query = Query(x_axis, y_axis, filters)
    query.make_query_list()
    return render_template('index_graph_tool.html', x_val=x_axis, y_val=y_axis, query_output=query.query_log, filter_text=filter_text)

def process_cmd(cmd_string):
    #check command supported
    cmd_parts = cmd_string.split('=')
    series = ds.load_pickle(ds.ACTIVE_FILE)
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
    if cmd_parts[0] == 'disp_char':
        character = Character.match_character(series.characters, cmd_parts[1])
        if character == ret.ERROR:
            return ret.ERROR, "Unable to match character name: " + cmd_parts[1]
        char_text = character.print_info()
        return ret.HOME, char_text
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
    if cmd_parts[0] == 'text_tool':
        #TODO i need to be more intelligent with my exeptions for try/catch
        try:
            input = open("data\\" + str(cmd_parts[1]), 'r')
            sav_text = input.read()
        except:
            return ret.ERROR, "Unable to read file data\\" + str(cmd_parts[1])
        try:
            data = {}
            data["book_file"] = ds.create_array(sav_text, "book_file")[0]
            data["series_obj"] = ds.create_array(sav_text, "series_obj")[0]
            data["book_name"] = ds.create_array(sav_text, "book_name")[0]
            data["position"] = ds.create_array(sav_text, "position")[0]
            data["known_names"] = ",".join(ds.create_array(sav_text, "known_names"))
        except:
            return ret.ERROR, "Invalid formatting in file data\\" +str(cmd_parts[1])
        return ret.TEXT_TOOL, data
    return ret.ERROR, "Unsupported command entry: " + cmd_string
    
if __name__ == '__main__':
    app.run()