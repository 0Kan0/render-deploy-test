import dash_html_components as html
import dash_bootstrap_components as dbc

from explainerdashboard.custom import *

class FeaturesImportanceBasicTab(ExplainerComponent):
    def __init__(self, explainer, title="Predictions", name=None,
                    hide_title=True, hide_importances=False, hide_descriptions=True, pos_label=None,
                    hide_selector=True, **kwargs):

        super().__init__(explainer, title, name)
        self.importances = ImportancesComponent(
                explainer, name=self.name+"0", hide_selector=True, hide_type=True, hide_depth=True, hide_popout=True)
        self.confusionmatrix = ConfusionMatrixComponent(explainer, name=self.name+"2",
                hide_selector=hide_selector, pos_label=pos_label, **kwargs)
        
        if not self.explainer.descriptions:
            self.hide_descriptions=True

    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    self.importances.layout(),
                ], width=7, style=dict(margin=30)),
                dbc.Col([
                    html.H3("Description"),
                    html.Div("This graph indicates how much each feature contributes to the model prediction. Basically, it determines the degree of usefulness of a specific variable for a current model and prediction."),
                    html.Div("For obtaining the importance or impact of each feature it is calculated the mean absolute SHAP value that shows how much a single feature affected the prediction."),
                    html.Div(f"Clearly {self.explainer.columns_ranked_by_shap()[0]} was the most important"
                            f", followed by {self.explainer.columns_ranked_by_shap()[1]}"
                            f" and {self.explainer.columns_ranked_by_shap()[2]}."),
                ], width=4, style=dict(margin=30)),
            ], class_name="mt-4"),
            dbc.Row([
                dbc.Col([
                    html.H3("Description"),
                    html.Div("This matrix represents the visualization of the performance of the algorithm we used for prediction. Each square have a different meaning: "),
                    html.Div(""),
                    html.Div("- True positive (top left): You predicted to be postive and it's true."),
                    html.Div("- False negative (top right): You predicted to be negative and it's false."),
                    html.Div("- False positive (bottom left): You predicted to be positive and it's false."),
                    html.Div("- True negative (bottom right): You predicted to be negative and it's true."),
                ], width=4, style=dict(margin=30)),
                dbc.Col([
                    self.confusionmatrix.layout(),
                ], width=7, style=dict(margin=30)),
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