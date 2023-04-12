from dash import html
import dash_bootstrap_components as dbc

from explainerdashboard.custom import *
from .components import SelectStudentComponent

class WhatIfBasicTab(ExplainerComponent):
    def __init__(self, explainer, title="What if...", name=None,
                        hide_whatifindexselector=False, hide_inputeditor=False,
                        hide_whatifprediction=False, hide_whatifcontributiongraph=False, 
                        hide_whatifpdp=False, hide_whatifcontributiontable=False,
                        hide_title=True, hide_selector=True, index_check=True,
                        n_input_cols=4, sort='importance', **kwargs):

        super().__init__(explainer, title, name)

        self.input = FeatureInputComponent(explainer, name=self.name+"0",
                        hide_selector=hide_selector, n_input_cols=self.n_input_cols,
                        **update_params(kwargs, hide_index=False))
        
        self.index = SelectStudentComponent(explainer, name=self.name+"1",
                    hide_selector=hide_selector, **kwargs)
        self.prediction = ClassifierPredictionSummaryComponent(explainer, name=self.name+"2",
                    feature_input_component=self.input,
                    hide_star_explanation=True,
                    hide_selector=hide_selector, **kwargs)
        self.contribution = ShapContributionsGraphComponent(explainer, name=self.name+"3",
                    hide_selector=hide_selector, **kwargs)
        self.index_connector = IndexConnector(self.index, [self.input, self.contribution], 
                                    explainer=explainer if index_check else None)

    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3("Description"),
                    html.Div("Select the student you want to see via the dropdown box or select it randomly."),
                ], width=4, style=dict(margin=30)),    

                dbc.Col([
                    self.index.layout(),
                ], width=7, style=dict(margin=30)),
            ], class_name="mt-4"),

            dbc.Row([ 
                dbc.Col([
                    self.prediction.layout(),
                ], width=7, style=dict(margin=30)), 

                dbc.Col([
                    html.H3("Description"),
                    html.Div("This graph shows the percentage or probability of dropout and no dropout of the selected student above."),
                ], width=4, style=dict(margin=30)),
            ], class_name="mt-4"),

            dbc.Row([
                dbc.Col([
                    html.H3("Description"),
                    html.Div("Change the different values of the variables of a student to see how the percentages of the previous graph vary."),
                ], width=4, style=dict(margin=30)),

                dbc.Col([
                    self.input.layout(),
                ], width=7, style=dict(margin=30)),             
            ], class_name="mt-4"),

            dbc.Row([ 
                dbc.Col([
                    self.contribution.layout(),
                ], width=7, style=dict(margin=30)), 

                dbc.Col([
                    html.H3("Description"),
                    html.Div("This graph shows how much each variable contributes."),
                ], width=4, style=dict(margin=30)),
            ], class_name="mt-4"),
        ], fluid=True)
    

class WhatIfExpertTab(ExplainerComponent):
    def __init__(self, explainer, title="What if...", name=None,
                        hide_whatifindexselector=False, hide_inputeditor=False,
                        hide_whatifprediction=False, hide_whatifcontributiongraph=False, 
                        hide_whatifpdp=False, hide_whatifcontributiontable=False,
                        hide_title=True, hide_selector=True, index_check=True,
                        n_input_cols=4, sort='importance', **kwargs):

        super().__init__(explainer, title, name)

        self.input = FeatureInputComponent(explainer, name=self.name+"0",
                        hide_selector=hide_selector, n_input_cols=self.n_input_cols,
                        **update_params(kwargs, hide_index=False))
        
        self.index = SelectStudentComponent(explainer, name=self.name+"1",
                    hide_selector=hide_selector, **kwargs)
        self.prediction = ClassifierPredictionSummaryComponent(explainer, name=self.name+"2",
                    feature_input_component=self.input,
                    hide_star_explanation=True,
                    hide_selector=hide_selector, **kwargs)
        self.contribution = ShapContributionsGraphComponent(explainer, name=self.name+"3",
                    hide_selector=hide_selector, **kwargs)
        self.index_connector = IndexConnector(self.index, [self.input, self.contribution], 
                                    explainer=explainer if index_check else None)

    def layout(self):
        return dbc.Container([
            dbc.Row([
                    dbc.Col(
                        self.index.layout()),
                    dbc.Col(
                            self.prediction.layout()), 
                    ], class_name="mt-4 gx-4"),
            dbc.Row([
                    dbc.Col(
                            self.input.layout()),     
                    dbc.Col(
                            self.contribution.layout()),         
                    ], class_name="mt-4 gx-4")
        ], fluid=True)