import dash_bootstrap_components as dbc

from .components import *
from .testAll import *

class CounterfactualsTab(ExplainerComponent):
    def __init__(self, explainer, title="Counterfactuals scenarios", name=None,
                    hide_title=True, hide_importances=False, hide_descriptions=False,
                    hide_selector=True, **kwargs):

        super().__init__(explainer, title, name)
       
        self.counterfactual = CounterfactualsComponent(explainer, name=self.name+"1",
                    hide_selector=hide_selector, **kwargs)

    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    self.counterfactual.layout(),
                ]),
            ], class_name="mt-4"),
        ], fluid=True)