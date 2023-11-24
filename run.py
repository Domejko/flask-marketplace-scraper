from app import create_app


# Creating Flask instance
app = create_app()

# If it is the main file, then the app.run() function will be executed.
if __name__ == '__main__':
    app.run()
