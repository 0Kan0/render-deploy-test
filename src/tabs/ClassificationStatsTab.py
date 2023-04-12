from dash import html
import dash_bootstrap_components as dbc

from explainerdashboard.custom import *

class ClassificationStatsTab(ExplainerComponent):
    def __init__(self, explainer, title="Classification Stats", name=None,
                    hide_title=True, hide_selector=True, 
                    hide_globalcutoff=False,
                    hide_modelsummary=False, hide_confusionmatrix=False,
                    hide_precision=False, hide_classification=False,
                    hide_rocauc=False, hide_prauc=False,
                    hide_liftcurve=False, hide_cumprecision=False,
                    pos_label=None,
                    bin_size=0.1, quantiles=10, cutoff=0.5, **kwargs):

        super().__init__(explainer, title, name)

        self.summary = ClassifierModelSummaryComponent(explainer, name=self.name+"0", 
                hide_selector=hide_selector, pos_label=pos_label, **kwargs)
        self.rocauc = RocAucComponent(explainer, name=self.name+"1",
                hide_selector=hide_selector, pos_label=pos_label, **kwargs)
        self.confusionmatrix = ConfusionMatrixComponent(explainer, name=self.name+"2",
                hide_selector=hide_selector, pos_label=pos_label, **kwargs)
        self.classification = ClassificationComponent(explainer, name=self.name+"3",
                hide_selector=hide_selector, pos_label=pos_label, **kwargs)

        #self.cutoffpercentile = CutoffPercentileComponent(explainer, name=self.name+"4",
         #       hide_selector=hide_selector, pos_label=pos_label, cutoff=cutoff, **kwargs)
        #self.cutoffconnector = CutoffConnector(self.cutoffpercentile,
         #       [self.summary, self.precision, self.confusionmatrix, self.liftcurve, 
          #       self.cumulative_precision, self.classification, self.rocauc, self.prauc])

    def layout(self):
        return dbc.Container([
                make_hideable(
                    dbc.Row(
                        html.H2('Model Performance:'), class_name="mt-4 gx-4"),
                    hide=self.hide_title),
            dbc.Row([
                    make_hideable(dbc.Col(self.summary.layout()),
                                  hide=self.hide_modelsummary),
                    make_hideable(dbc.Col(self.confusionmatrix.layout()),
                                  hide=self.hide_confusionmatrix),
                    ], class_name="mt-4 gx-4"),
            dbc.Row([
                make_hideable(dbc.Col(self.rocauc.layout()),
                              hide=self.hide_rocauc),
                make_hideable(dbc.Col(self.classification.layout()),
                              hide=self.hide_classification),
            ], class_name="mt-4 gx-4")
        ], fluid=True)