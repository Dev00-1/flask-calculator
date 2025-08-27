from flask import Flask, request, jsonify, render_template
import sympy as sp
import re

app = Flask(__name__)

# Optional: map superscripts and subscripts to normal chars
SUPERSCRIPT_MAP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

def normalize_expression(expr):
    # Replace superscripts like x² → x^2
    expr = expr.translate(SUPERSCRIPT_MAP)
    expr = expr.replace("^", "")  # Python uses ** for power
    expr = expr.translate(SUBSCRIPT_MAP)  # Optional: convert subscripts to normal
    return expr

@app.route("/")
def home():
    return render_template("index.html", result=None)

@app.route("/calculate-ui", methods=["POST"])
def calculate_ui():
    operation = request.form["operation"]
    result = None

    try:
        if operation in ["add", "subtract", "multiply", "divide"]:
            a = float(request.form["a"])
            b = float(request.form["b"])
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                result = a / b
        elif operation in ["differentiate", "integrate"]:
            raw_expr = request.form["expression"]
            raw_var = request.form["variable"]

            expr = normalize_expression(raw_expr)
            var = normalize_expression(raw_var)

            var_symbol = sp.Symbol(var)
            parsed_expr = sp.sympify(expr)

            if operation == "differentiate":
                result = str(sp.diff(parsed_expr, var_symbol))
            else:
                result = str(sp.integrate(parsed_expr, var_symbol))
    except Exception as e:
        result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)