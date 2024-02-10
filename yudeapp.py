from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get user input keyword name
    name = request.form['name']

    selected_file = request.form['file']  # Retrieve the selected Excel file
    # Load the selected Excel file
    df = pd.read_excel(selected_file, skiprows = 1)

    # Filter data based on keyword in the 'Name' column
    result = df[df['中文姓名'].str.contains(name, case=False, na=False)]
    result_english = df[df['英文姓名'].str.contains(name, case=False, na=False)]
    if result.empty and result_english.empty:
        message = "無相關編號 '{}'.".format(name)
        return render_template('result.html', message=message)
    else:
        if result.empty:
           result_html = result_english.to_html(index=False)
        else:
           result_html = result.to_html(index=False)      

        return render_template('result.html', data=result_html)

if __name__ == '__main__':
    app.run(debug=True)