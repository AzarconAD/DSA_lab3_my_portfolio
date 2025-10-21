from flask import Flask, render_template, request

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
            result = 3.14 * radius * radius
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
    stack = Stack()
    output = ""

    for char in expression.replace(" ", ""):
        if char.isalnum():
            output += char
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output += stack.pop()
            stack.pop()
        elif is_operator(char):
            while (not stack.is_empty() and
                   precedence(stack.peek()) >= precedence(char)):
                output += stack.pop()
            stack.push(char)

    while not stack.is_empty():
        output += stack.pop()

    return output


if __name__ == "__main__":
    app.run(debug=True)

