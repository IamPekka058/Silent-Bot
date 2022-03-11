from flask import Flask, render_template
import resources.oauth as oauth

app = Flask("__main__", template_folder="./modules/webservice/templates/")

def initWebsite():
    @app.route('/')
    def indexPage():
        return render_template('index.html', discord_url=oauth.OAuth.discord_login_url)

    @app.route('/login')
    def loginPage():
        return('Success')

def runWebsite():
    initWebsite()
    app.run() 