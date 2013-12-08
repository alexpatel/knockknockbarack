from build import build, add_jokes
import app

build.build()
build.add_jokes(10)
app.app.run()