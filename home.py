from flask import Flask, render_template, request, redirect
import ret, ValidCommands
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
    if not check_syntax(cmd_string):
        return ret.HOME, "Invalid command entry: " + cmd_string
    else:
        return ret.HOME, "Valid command entry: " + cmd_string

def check_syntax(cmd_string):
    if cmd_string.find('=') < 0:
        return False
    cmd_parts = cmd_string.split("=")
    if not ValidCommands.is_valid(cmd_parts[0]):
        return False

if __name__ == '__main__':
   app.run()