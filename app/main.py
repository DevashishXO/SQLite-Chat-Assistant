from flask import Flask, request, render_template_string
from app.nlp import NLPToSQL
from app.db import Database 

app = Flask(__name__)
nlp = NLPToSQL()
db = Database()

HTML_TEMPLATE = """
!DOCTYPE html>
<html>
<head><title> Chat Assistant </title></head>
<body>
    <h1> Database Chat Assistant</h1>
    <form method="POST">
        <input type="text" name="query" placeholder= "Enter your query..." size="50">
        <button type="submit">Ask</button>
    </form>
    {% if response %}
        <h3> Response: </h3>
        <pre>{{ response }}</pre>
    {% endif %}
    {% if error %}
        <p style = "color:red;">{{ error }} </p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_query = request.form['query']
        try:
            sql = nlp.query_to_sql(user_query)
            result = db.execute_query(sql)
            if 'error' in result:
                return render_template_string(HTML_TEMPLATE, error = result['error'])
            if not result['data']:
                return render_template_string(HTML_TEMPLATE, error = "No data found")
            
            response = " | ".join(result['columns']) + "\n"
            response += "-"*50 + "\n"
            for row in result['data']:
                response += " | ".join(str(cell) for cell in row) + "\n"
                return render_template_string(HTML_TEMPLATE, response = response)
            
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error = f"Error: {str(e)}")
        
    return render_template_string(HTML_TEMPLATE)

                
