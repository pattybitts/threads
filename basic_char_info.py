from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index_home.html')
    
@app.route('/disp_char_info', methods = ['POST'])
def disp_char_info():
    char_name = request.form['char_name_box']
    char_info = get_char_info(char_name)
    return render_template('index_char_info.html', char_name=char_name, char_info=char_info)
    
def get_char_info(char_name):
    if char_name == "Rand al'Thor":
        return "def goob"
    else:
        return "maybe goob"

if __name__ == '__main__':
    app.run()