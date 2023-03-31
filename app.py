from website import create_app

app = create_app()

"""""
@app.route('/')
def home():  # put application's code here
    return 'Hello VWM3!'
"""""

if __name__ == '__main__':
    app.run(debug=True)
