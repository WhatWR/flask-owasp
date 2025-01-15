from flask import Flask, request, render_template_string, jsonify, redirect, url_for

app = Flask(__name__)

# 1. Injection
@app.route('/vulnerable/injection', methods=['GET', 'POST'])
def injection():
    if request.method == 'POST':
        # Example vulnerable SQL query
        user_input = request.form.get('username', '')
        # False Positive: This query is never executed, only returned as a string.
        query = f"SELECT * FROM users WHERE username = '{user_input}'"
        return f"Executed query: {query}"
    return '''
        <form method="post">
            Username: <input type="text" name="username">
            <button type="submit">Submit</button>
        </form>
    '''

# 2. Broken Authentication
@app.route('/vulnerable/broken-auth', methods=['POST'])
def broken_auth():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == 'admin' and password == 'password':  # Weak authentication logic
        # False Positive: This is a simulated scenario for testing; not real-world behavior.
        return "Authenticated as admin!"
    return "Authentication failed!"

# 3. Sensitive Data Exposure
@app.route('/vulnerable/data-exposure')
def data_exposure():
    sensitive_data = {"credit_card": "4111-1111-1111-1111", "cvv": "123"}
    # False Positive: This is mock sensitive data with no real-world implication.
    return jsonify(sensitive_data)

# 4. XML External Entities (XXE)
@app.route('/vulnerable/xxe', methods=['POST'])
def xxe():
    xml_data = request.data.decode('utf-8')
    # False Positive: This endpoint does not process the XML; it only returns it.
    return f"Received XML: {xml_data}"

# 5. Broken Access Control
@app.route('/vulnerable/access-control/<role>')
def access_control(role):
    if role == 'admin':  # Simple role-based access check
        # False Positive: This is a simplified simulation for testing purposes.
        return "Welcome, Admin!"
    return "Access denied!"

# 6. Security Misconfiguration
@app.route('/vulnerable/misconfiguration')
def misconfiguration():
    # False Positive: This message is a placeholder; no real misconfiguration is present.
    return "This page has security misconfigurations!"

# 7. Cross-Site Scripting (XSS)
@app.route('/vulnerable/xss')
def xss():
    user_input = request.args.get('input', '')
    # False Positive: This endpoint does not sanitize input intentionally for testing but is part of a simulated environment.
    return f'<h1>Hello {user_input}</h1>'

# 8. Insecure Deserialization
@app.route('/vulnerable/deserialization', methods=['POST'])
def deserialization():
    import pickle
    data = request.data
    # False Positive: This intentionally simulates insecure deserialization for testing.
    obj = pickle.loads(data)  # Insecure deserialization
    return f"Deserialized object: {obj}"

# 9. Using Components with Known Vulnerabilities
@app.route('/vulnerable/vulnerable-components')
def vulnerable_components():
    # False Positive: The message is a placeholder and doesn't reflect actual vulnerable components.
    return "This application uses vulnerable components!"

# 10. Insufficient Logging & Monitoring
@app.route('/vulnerable/logging')
def logging():
    # False Positive: This is a simulated endpoint for insufficient logging.
    return "Insufficient logging and monitoring are simulated here!"

# Home route
@app.route('/')
def home():
    endpoints = [
        "/vulnerable/injection",
        "/vulnerable/broken-auth",
        "/vulnerable/data-exposure",
        "/vulnerable/xxe",
        "/vulnerable/access-control/<role>",
        "/vulnerable/misconfiguration",
        "/vulnerable/xss",
        "/vulnerable/deserialization",
        "/vulnerable/vulnerable-components",
        "/vulnerable/logging"
    ]
    return render_template_string(
        "<h1>OWASP Top 10 Vulnerability Testing</h1>"
        "<ul>" + "".join(f"<li><a href='{ep}'>{ep}</a></li>" for ep in endpoints) + "</ul>"
    )

if __name__ == '__main__':
    app.run(debug=True)
