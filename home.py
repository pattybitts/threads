from flask import Flask, render_template, request, redirect
import ret
from cmd import ValidCommands
from Series import Series
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

if __name__ == '__main__' and 0:
   app.run()

if 0:
    action, data = process_cmd("disp_chare=Rand")
    print(action)
    print(data)

if 1:
    s = Series("characters.json")