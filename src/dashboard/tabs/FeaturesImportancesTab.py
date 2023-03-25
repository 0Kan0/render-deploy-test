import dash_html_components as html
import dash_bootstrap_components as dbc

from explainerdashboard.custom import *

class FeaturesImportanceBasicTab(ExplainerComponent):
    def __init__(self, explainer, title="Feature Importances", name=None,
                    hide_title=True, hide_importances=False, hide_descriptions=True,
                    hide_selector=True, **kwargs):

        super().__init__(explainer, title, name)
        self.importances = ImportancesComponent(
                explainer, name=self.name+"0", hide_selector=True, hide_type=True, hide_depth=True, hide_popout=True)
        
        if not self.explainer.descriptions:
            self.hide_descriptions=True

    def layout(self):
        return dbc.Container([
            dbc.Row([
                make_hideable(
                    dbc.Col([
                        self.importances.layout(),
                    ], width=7, style=dict(margin=30))),
                     dbc.Col([
                        html.H3("Description"),
                        html.Div("This graph indicates how much each feature contributes to the model prediction. Basically, it determines the degree of usefulness of a specific variable for a current model and prediction."),
                ], width=4, style=dict(margin=30)),
            ], class_name="mt-4"),
        ], fluid=True)
    

class FeaturesImportanceExpertTab(ExplainerComponent):
    def __init__(self, explainer, title="Feature Importances", name=None,
                    hide_title=True, hide_importances=False, hide_descriptions=True,
                    hide_selector=True, **kwargs):

        super().__init__(explainer, title, name)
        self.importances = ImportancesComponent(
                explainer, name=self.name+"0", hide_selector=True, hide_popout=True)
        
        if not self.explainer.descriptions:
            self.hide_descriptions=True

    def layout(self):
        return dbc.Container([
            dbc.Row([
                make_hideable(
                    dbc.Col([
                        self.importances.layout(),
                    ])),
            ], class_name="mt-4"),
        ], fluid=True)