import logging
import gradio as gr
from nlp import NLPToSQL
from db import Database

nlp = NLPToSQL()
db = Database()

logging.basicConfig(level=logging.INFO)

def chatbot(user_query):
    try:
        sql = nlp.query_to_sql(user_query)
        logging.info(f"Generated SQL: {sql}")
        result = db.execute_query(sql)

        if 'error' in result:
            return f"❌ Error: {result['error']}"
        if not result['data']:
            return "⚠️ No data found."

        # Formatting SQL output
        response = f"**Query:**\n```\n{sql}\n```\n\n"
        response += "**Result:**\n"
        response += "<table style='width:100%; border-collapse: collapse;'>"
        response += "<tr style='background-color: #f2f2f2;'>"
        for col in result['columns']:
            response += f"<th style='border: 1px solid #ddd; padding: 8px;'>{col}</th>"
        response += "</tr>"
        for row in result['data']:
            response += "<tr>"
            for cell in row:
                response += f"<td style='border: 1px solid #ddd; padding: 8px;'>{cell}</td>"
            response += "</tr>"
        response += "</table>"
        return response

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return f"❌ Error: {str(e)}"

demo = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(lines=2, placeholder="Ask your database anything..."),
    outputs="markdown",
    title="SQL Chat Assistant",
    description="Enter a natural language question, and get the corresponding SQL query & result."
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)



# Flask-based application can also be used

# import logging
# from flask import Flask, request, render_template_string
# from .nlp import NLPToSQL
# from .db import Database

# app = Flask(__name__)
# nlp = NLPToSQL()
# db = Database()

# logging.basicConfig(level=logging.INFO)

# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html>
# <head><title> Chat Assistant </title></head>
# <body>
#     <h1> Database Chat Assistant</h1>
#     <form method="POST">
#         <input type="text" name="query" placeholder= "Enter your query..." size="50">
#         <button type="submit">Ask</button>
#     </form>
#     {% if response %}
#         <h3> Response: </h3>
#         <pre>{{ response }}</pre>
#     {% endif %}
#     {% if error %}
#         <p style = "color:red;">{{ error }} </p>
#     {% endif %}
# </body>
# </html>
# """

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == 'POST':
#         user_query = request.form['query']
#         try:
#             sql = nlp.query_to_sql(user_query)
#             logging.info(f"Generated SQL: {sql}")
#             result = db.execute_query(sql)
#             if 'error' in result:
#                 return render_template_string(HTML_TEMPLATE, error=result['error'])
#             if not result['data']:
#                 return render_template_string(HTML_TEMPLATE, error="No data found")
            
#             response = " | ".join(result['columns']) + "\n"
#             response += "-"*50 + "\n"
#             for row in result['data']:
#                 response += " | ".join(str(cell) for cell in row) + "\n"
#             return render_template_string(HTML_TEMPLATE, response=response)
            
#         except Exception as e:
#             logging.error(f"Error: {str(e)}")
#             return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}")
        
#     return render_template_string(HTML_TEMPLATE)

# if __name__ == "__main__":
#     app.run(debug=True)