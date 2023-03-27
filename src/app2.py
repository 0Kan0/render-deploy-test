""" from explainerdashboard import ClassifierExplainer, ExplainerDashboard, ExplainerHub
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

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

explainer = ClassifierExplainer(model, X_test, y_test, labels=["Dropout", "No dropout"], target="Target")


db1 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer basic", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab])

db2 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer expert", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab])

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", description="")
hub.to_yaml("hub.yaml", pickle_type="dill")

hub.run() """