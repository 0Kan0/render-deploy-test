import dash_bootstrap_components as dbc

from .components import *
from explainerdashboard.custom import *
from src.app import *

class AutoMLReportTab(ExplainerComponent):
    def __init__(self, explainer, title="AutoML Report", name=None,
                    hide_title=True, hide_importances=False, hide_descriptions=False,
                    hide_selector=True, **kwargs):

        super().__init__(explainer, title, name)
        self.report = AutoMLReportComponent(explainer, name=self.name+"0")

    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    self.report.layout(),
                ]),
            ], class_name="mt-4"),
        ], fluid=True)