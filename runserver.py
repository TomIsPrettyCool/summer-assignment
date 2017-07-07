import os
from namesfornumbers import app
import webbrowser

print(os.environ.get("FLASK_DEBUG"))

if os.environ.get("FLASK_DEBUG"):
    # Run with a debugger for development
    app.run(debug=True)

else:
    # Open a webbrowser, then run the app normally
    webbrowser.open("http://127.0.0.1:5000/")  # Open the webbrowser
    print("""
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    CLOSE THIS TERMINAL WINDOW WHEN FINISHED.

    Or, Run on a remote server and never
    worry about this again.
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """)
    app.run()  # Run the main HTTP app.
