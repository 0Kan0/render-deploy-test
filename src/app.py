from explainerdashboard import ClassifierExplainer, ExplainerHub, ExplainerDashboard
from supervised.automl import AutoML
from dash import Dash
from pathlib import Path
from tabs.AutoMLReportTab import AutoMLReportTab
from tabs.ClassificationStatsTab import ClassificationStatsTab
from tabs.CounterfactualsTab import CounterfactualsTab
from tabs.FeaturesImportancesTab import FeaturesImportanceBasicTab, FeaturesImportanceExpertTab
from tabs.WhatIfTab import WhatIfBasicTab, WhatIfExpertTab

app = Dash(__name__)
server = app.server

path = Path.cwd() / ""

explainer = ClassifierExplainer.from_file(path/"dashboard1_explainer.dill")

db1 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer basic", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab])

db2 = ExplainerDashboard(explainer, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer expert", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab])

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", description="")

if __name__ == "__main__":
    app.run_server(debug=False)