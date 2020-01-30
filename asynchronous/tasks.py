from celery import Task

from celery_app import app
from opencv_server.recognise import Recognise


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        '''成功执行的函数'''
        print(retval)
        print(task_id)
        print(args)
        print(kwargs)
        get_res(retval)


def on_failure(self, exc, task_id, args, kwargs, einfo):
    '''失败执行的函数'''
    print("callback failure function")


@app.task(base=CallbackTask)
def add(x, y):
    return x + y


def get_res(x):
    print(f'* ******************** {x}')


@app.task
def recognise(path):
    """
    识别任务
    :param path:
    :return:
    """

    result = Recognise.run(path)

    return result
