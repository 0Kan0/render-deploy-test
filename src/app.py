from explainerdashboard import ClassifierExplainer, ExplainerHub, ExplainerDashboard
from supervised.automl import AutoML
from dash import Dash
from pathlib import Path
from tabs.AutoMLReportTab import AutoMLReportTab
from tabs.ClassificationStatsTab import ClassificationStatsTab
from tabs.CounterfactualsTab import CounterfactualsTab
from tabs.FeaturesImportancesTab import FeaturesImportanceBasicTab, FeaturesImportanceExpertTab
from tabs.WhatIfTab import WhatIfBasicTab, WhatIfExpertTab
import shutil
from tabs.testAll import *

app = Dash(__name__)
server = app.server

explainer1 = ClassifierExplainer.from_file("src\dashboard1_explainer.dill")
explainer2 = ClassifierExplainer.from_file("src\dashboard2_explainer.dill")


db1 = ExplainerDashboard(explainer1, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer basic", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab])

db2 = ExplainerDashboard(explainer2, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer expert", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab])

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", description="")

shutil.rmtree('AutoML_1')

hub.run()

if __name__ == "__main__":
    app.run_server(debug=False)