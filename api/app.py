from main import create_app
import os
from main import db

from main.utilities.sensor_sockets import call_sensors
import threading

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    db.create_all()
    threading.Thread(target=call_sensors, args=(app,)).start()
    app.run(debug=True, port=os.getenv('PORT'))
