from explainerdashboard import ClassifierExplainer, ExplainerDashboard, ExplainerHub
from dash import Dash
from supervised.automl import AutoML
import sys
import os
import dill
from tabs.testAll import *
from tabs.AutoMLReportTab import AutoMLReportTab
from tabs.ClassificationStatsTab import ClassificationStatsTab
from tabs.CounterfactualsTab import CounterfactualsTab
from tabs.FeaturesImportancesTab import FeaturesImportanceBasicTab, FeaturesImportanceExpertTab
from tabs.WhatIfTab import WhatIfBasicTab, WhatIfExpertTab

app = Dash(__name__)
server = app.server

explainer = ClassifierExplainer(model, X_test, y_test, labels=["Dropout", "No dropout"], target="Target", shap="Linear",
                                precision='float32')


db1 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer basic", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab])

db2 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer expert", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab])

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", description="")


if __name__ == "__main__":
    app.run_server(debug=False)