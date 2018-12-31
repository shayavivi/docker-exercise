import os
from celery import Celery

from model import Session, ClientData

app = Celery('tasks', broker='amqp://{0}:{1}@{2}:{3}'.format(os.environ.get('USER', 'admin'), os.environ.get('PASS', 'mypass'), os.environ.get('HOSTNAME', 'localhost'), os.environ.get('PORT', '5672'))  # create celery worker server, broker is RabbitMQ


@app.task
def mul():
    session = Session()
    # select the rows that doesn't have result
    for datarow in session.query(ClientData).all():
        if not datarow.result:
            datarow.result = mul_data(datarow.rawData)  # add result to the data row
            session.add(datarow)  # update the datarow in the DB
            session.commit()  # commit all changes to DB

    session.close()


def mul_data(rawdata):  # multiplies the numbers in the raw data and returns the result
    temp_mul = 1
    lenthd = len(rawdata)
    cutarr = rawdata[1:lenthd-1]  # remove edges
    numarr = cutarr.split(',')  # split by ',' to get the numbers
    for x in numarr:
        temp_mul = temp_mul * int(x)  # multiply the numbers
    return temp_mul


