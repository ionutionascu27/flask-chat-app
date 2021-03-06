import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

'''Write to file separate function'''
def write_to_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(data)

def clear_conversation():
    with open('data/messages.txt', 'w') as file:
        file.write("")

''' Add messages to a dictionary '''
def add_messages(username, message):
    '''Write messages in a text file'''
    write_to_file("data/messages.txt", "At {0} {1} wrote: {2}\n".format(
        datetime.now().strftime("%H:%M:%S"), 
        username.title(), 
        message))
    
def show_items(path):
    '''Read messages from the text file'''
    items = []
    with open(path, 'r') as items_list:
        items = items_list.readlines()
    return items

@app.route('/', methods = ["GET", "POST"])

def index():
    '''Home page with chat instructions'''
    if request.method == "POST":
        if "{}\n".format(request.form['username']) not in show_items("data/users.txt"):
            clear_conversation()
        write_to_file("data/users.txt", request.form['username']+"\n")
        return redirect(request.form['username'])    
    return render_template('index.html')
    
@app.route('/<username>')

def user(username):
    ''' Display chat messages '''
    messages = show_items("data/messages.txt")
    return render_template('chat.html', username = username, chat_messages = messages) 
    
@app.route('/<username>/<message>')   

def send_message(username, message):
    ''' Create new message and redirect to chat page '''
    add_messages(username, message)
    return redirect(username)
    
app.run(host = os.getenv('IP'), port = int(os.getenv('PORT')), debug = True)    