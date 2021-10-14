from website import create_app

app = create_app()

# Only runs webserver when executing main.py, not when called somewhere else
if __name__ == '__main__':
    app.run(debug=True)