from re import template
from jinja2 import *

file_loader = FileSystemLoader('templates')

env = Environment(loader=file_loader)

def index():
    template = env.get_template('index.html')
    out = template.render(name="trinity")
    return out
    #return "<html><h1>Hello, it's name</h1></html>"
    #with open('templates/index.html') as ss:
    #    return ss.read()

PAGES = {
    '/': index()
}
