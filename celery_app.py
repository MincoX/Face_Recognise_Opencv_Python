from __future__ import absolute_import
from __future__ import unicode_literals
from celery import Celery

app = Celery(
    '02.face_server_opencv_company',
    broker='redis://49.232.19.51:63791/1',
    backend='redis://49.232.19.51:63791/2',
    include=['asynchronous.tasks']
)
app.conf.update(result_expires=3600, )

if __name__ == '__main__':
    app.start()
