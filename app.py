from flask import Flask, render_template, request

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

if __name__ == "__main__":
    app.run(debug=True)