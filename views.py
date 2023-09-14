from flask import render_template
from flask.views import View

class ListView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)


class DetailView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self, id):
        item = self.model.query.get_or_404(id)
        return render_template(self.template, item=item)