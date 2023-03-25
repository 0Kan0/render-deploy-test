from explainerdashboard import ClassifierExplainer, ExplainerDashboard, ExplainerHub
from dash import Dash

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from dashboard.tabs.testAll import *
from dashboard.tabs.AutoMLReportTab import *
from dashboard.tabs.FeaturesImportancesTab import *
from dashboard.tabs.ClassificationStatsTab import *
from dashboard.tabs.WhatIfTab import *
from dashboard.tabs.CounterfactualsTab import *

app = Dash(__name__)
server = app.server

explainer = ClassifierExplainer(model, X_test, y_test, labels=["Dropout", "No dropout"], target="Target")

db1 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer basic", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab])

db2 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer expert", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab])

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", description="")

hub.run()