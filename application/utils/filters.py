from dateutil import parser
from datetime import datetime
from urllib import parse

def format_date(epoch):
    date = datetime.fromtimestamp(epoch/1000).strftime('%d-%m-%Y %H:%M:%S')
    return date

def remove_slashes(astring):
    return astring.replace("/", "-")

def aws_batch_id_encode(id):
    # AWS double encodes id in url
    return parse.quote(parse.quote(id, safe=""), safe="")
