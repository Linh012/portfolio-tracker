from app import app  #import app package (app folder with __init__.py)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #run flask app
