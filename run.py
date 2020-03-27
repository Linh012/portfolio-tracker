from app import app  # from app package (app folder with __init__.py)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)  # runs app

    # debug True = automatically updates web app when code is edited
    # host='0.0.0.0'
    # port=5000
