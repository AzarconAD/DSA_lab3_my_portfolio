from flask import Flask, render_template, request, jsonify

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node


    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None


    def print_stack(self):
        if self.top is None:
            print("Stack is empty")
        else:
            current = self.top
            print("Stack elements (top → bottom):")
            while current:
                print(current.data)
                current = current.next

    def is_empty(self):
        return self.top is None

class SongNode:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0

    def add_song(self, title, artist, duration):
        new_song = SongNode(title, artist, duration)
        if not self.head:
            self.head = new_song
            self.current = self.head
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_song
        self.size += 1

    def display_playlist(self):
        songs = []
        current = self.head
        index = 1
        while current:
            songs.append({
                'index': index,
                'title': current.title,
                'artist': current.artist,
                'duration': current.duration,
                'is_current': current == self.current
            })
            current = current.next
            index += 1
        return songs

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current

    def previous_song(self):
        if self.current and self.current != self.head:
            current = self.head
            while current.next != self.current:
                current = current.next
            self.current = current
        return self.current

    def get_current_song(self):
        return self.current

    def get_playlist_size(self):
        return self.size

# Initialize playlist with some songs
playlist = Playlist()
playlist.add_song("Blinding Lights", "The Weeknd", "3:20")
playlist.add_song("Save Your Tears", "The Weeknd", "3:35")
playlist.add_song("Levitating", "Dua Lipa", "3:23")
playlist.add_song("Stay", "The Kid LAROI & Justin Bieber", "2:21")
playlist.add_song("Good 4 U", "Olivia Rodrigo", "2:58")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/works/toUpperCase', methods=['GET', 'POST'])
def touppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/works/areaCircle', methods=['GET', 'POST'])
def areaCircle():
    result = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', ''))
            if radius < 0:
                result = "Radius cannot be negative"
            else:
                result = f"{3.14 * radius * radius:.2f}"
        except ValueError:
            result = "Invalid input. Please enter a numeric value."
    return render_template('areacircle.html', result=result)

@app.route('/works/areaTriangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', ''))
            height = float(request.form.get('height', ''))
            result = 0.5 * base * height
        except ValueError:
            result = "Invalid input. Please enter numeric values."
    return render_template('areatriangle.html', result=result)

@app.route('/works/infixToPostfix', methods=['GET', 'POST'])
def infix_to_postfix_page():
    infix = None
    postfix = None

    if request.method == 'POST':
        infix = request.form['expression']
        postfix = infix_to_postfix(infix)

    return render_template('infixToPostfix.html', infix=infix, postfix=postfix)

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/', '%'):
        return 2
    if op == '^':
        return 3
    return 0


def is_operator(c):
    return c in "+-*/%^"


def infix_to_postfix(expression):
    if not expression:
        return ""
        
    stack = Stack()
    output = ""
    expression = expression.replace(" ", "")
    
    for char in expression:
        if char.isalnum():
            output += char
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output += stack.pop()
            if stack.is_empty():
                return "Error: Mismatched parentheses"
            stack.pop()
        elif is_operator(char):
            while (not stack.is_empty() and 
                   stack.peek() != '(' and 
                   precedence(stack.peek()) >= precedence(char)):
                output += stack.pop()
            stack.push(char)
        else:
            return f"Error: Invalid character '{char}'"
    
    while not stack.is_empty():
        if stack.peek() == '(':
            return "Error: Mismatched parentheses"
        output += stack.pop()
    
    return output

def validate_infix_expression(expression):
    """Basic validation for infix expressions"""
    expression = expression.replace(" ", "")
    if not expression:
        return False, "Expression cannot be empty"
    
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/%^()")
    if any(char not in valid_chars for char in expression):
        return False, "Expression contains invalid characters"
    
    return True, "Valid"

@app.route('/works/playlist')
def playlist_page():
    songs = playlist.display_playlist()
    current_song = playlist.get_current_song()
    return render_template('playlist.html', 
                         songs=songs, 
                         current_song=current_song,
                         playlist_size=playlist.get_playlist_size())

@app.route('/works/playlist/next', methods=['POST'])
def next_song():
    playlist.next_song()
    return jsonify({
        'current_song': {
            'title': playlist.current.title,
            'artist': playlist.current.artist,
            'duration': playlist.current.duration
        } if playlist.current else None
    })

@app.route('/works/playlist/previous', methods=['POST'])
def previous_song():
    playlist.previous_song()
    return jsonify({
        'current_song': {
            'title': playlist.current.title,
            'artist': playlist.current.artist,
            'duration': playlist.current.duration
        } if playlist.current else None
    })

@app.route('/works/playlist/add', methods=['POST'])
def add_song():
    title = request.form.get('title')
    artist = request.form.get('artist')
    duration = request.form.get('duration')
    
    if title and artist and duration:
        playlist.add_song(title, artist, duration)
    
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)

