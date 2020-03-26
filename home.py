from flask import Flask, render_template, request, redirect
import ret, data_storage, log
from cmd import ValidCommands
from Series import Series
from Character import Character
app = Flask(__name__)

@app.route('/')
def main():
    no_cmd = "Command output will appear here."
    return render_template('index_home.html', cmd_out=no_cmd)
    
@app.route('/new_cmd', methods = ['POST'])
def new_cmd_in():
    cmd_string = request.form['cmd_box']
    action, data = process_cmd(cmd_string)
    if action == ret.HOME:
        return render_template('index_home.html', cmd_out=data)
    
def process_cmd(cmd_string):
    #check syntax
    if cmd_string.find('=') < 0:
        return ret.HOME, "Invalid command entry: " + cmd_string
    #check command supported
    cmd_parts = cmd_string.split('=')
    if not ValidCommands.is_valid(cmd_parts[0]):
        return ret.HOME, "Command not supported: " + cmd_parts[0]

    return ret.HOME, "Valid command entry: " + cmd_string

if __name__ == '__main__':
    if 0:
        app.run()

    if 0:
        action, data = process_cmd("disp_chare=Rand")
        print(action)
        print(data)

    if 0:
        with open("characters.json") as file:
            full_text = file.read()
            character_list = data_storage.create_array(full_text, "Characters")

            for c in character_list:
                new_char = Character(c)
                log.out("\n" + new_char.string() + "\n")

    if 1:
        series_info = Series("books.json", "arcs.json", "characters.json", "wot.o")
        for c in series_info.characters:
            log.out(c.string())

        series_info = Series.import_object("wot.o")
        for c in series_info.characters:
            log.out(c.string())