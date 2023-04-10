from website import create_app

app = create_app()
print("App created!")

if __name__ == '__main__':
    print("Been in main.")
    app.run(debug=True)
