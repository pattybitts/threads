from flask import Flask, render_template, request, redirect
import ret, data_storage, log
from cmd import ValidCommands
from Series import Series
from Character import Character
app = Flask(__name__)

@app.route('/')
def main():
    cmd_out = "Command output will appear here."
    return render_template('index_home.html', cmd_out=cmd_out)
    
@app.route('/cmd_in', methods = ['POST'])
def new_cmd_in():
    series_info = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    cmd_string = request.form['cmd_box']
    action, data = process_cmd(cmd_string)
    if action == ret.HOME:
        return render_template('index_home.html', cmd_out=data)
    elif action == ret.EDIT_CHAR:
        character = series_info.find_char(data)
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
        if series_info.find_char(data, True) != ret.ERROR:
            error_msg = "INTERNAL ERROR:\nCharacter matched after processing"
            return render_template('index_home.html', cmd_out=error_msg)
        return render_template('index_char_form.html', action="add", char_name=data)
    error_msg = "INTERNAL ERROR:\nInvalid return from processing"
    return render_template('index_home.html', cmd_out=error_msg)

@app.route('/char_form_in', methods = ['POST'])
def edit_char():
    series_info = data_storage.load_pickle(data_storage.ACTIVE_FILE)
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
        if series_info.replace_char(new_char, request.form['base_name']) != ret.SUCCESS:
            resp = "INTERNAL ERROR:\nUnable to update character " + new_char.name + " in database"
        else:
            resp = "Character " + new_char.name + " successfully updated in database"
            series_info.save(data_storage.ACTIVE_FILE)
    elif request.form['action'] == 'add':
        if series_info.add_char(new_char) != ret.SUCCESS:
            resp = "INTERNAL ERROR:\nUnable to add character " + new_char.name + " in database"
        else:
            resp = "Character " + new_char.name + " successfully added to database"
            series_info.save(data_storage.ACTIVE_FILE)
    return render_template('index_home.html', cmd_out=resp)
    
def process_cmd(cmd_string):
    #check command supported
    cmd_parts = cmd_string.split('=')
    if not ValidCommands.is_valid(cmd_parts[0]):
        return ret.HOME, "Command not supported: " + cmd_parts[0]
    series_info = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    if cmd_parts[0] == 'disp_char':
        character = series_info.find_char(cmd_parts[1])
        if character == ret.ERROR:
            return ret.HOME, "Unable to match character name: " + cmd_parts[1]
        char_text = character.print_info()
        return ret.HOME, char_text
    if cmd_parts[0] == 'gen_archive':
        archive = open("wot_archive.txt", 'wb')
        for c in series_info.characters:
            archive.write(bytearray(c.print_info(), 'utf-8'))
            archive.write(bytearray("\n\n", 'utf-8'))
        archive.close()
        msg = "Generated archive file at wot_archive.txt"
        return ret.HOME, msg
    if cmd_parts[0] == 'gen_list':
        list = open("wot_char_list.txt", 'wb')
        for c in series_info.characters:
            list.write(bytearray(c.name + "\n", 'utf-8'))
        list.close()
        msg = "Generated character list at wot_char_list.txt"
        return ret.HOME, msg
    if cmd_parts[0] == 'edit_char':
        character = series_info.find_char(cmd_parts[1])
        if character == ret.ERROR:
            return ret.HOME, "Unable to match character name: " + cmd_parts[1]
        return ret.EDIT_CHAR, character.name
    if cmd_parts[0] == 'add_char':
        character = series_info.find_char(cmd_parts[1], True)
        if character == ret.ERROR:
            return ret.ADD_CHAR, cmd_parts[1]
        return ret.HOME, "Duplicate character with name: " + character.name \
            + "\nuse the 'edit_char' command to overwrite"
    return ret.HOME, "Valid command entry: " + cmd_string

if __name__ == '__main__':
    app.run()