from explainerdashboard import ClassifierExplainer, ExplainerHub, ExplainerDashboard
from supervised.automl import AutoML
from dash import Dash
from pathlib import Path
from tabs.AutoMLReportTab import AutoMLReportTab
from tabs.ClassificationStatsTab import ClassificationStatsTab
from tabs.CounterfactualsTab import CounterfactualsTab
from tabs.FeaturesImportancesTab import FeaturesImportanceBasicTab, FeaturesImportanceExpertTab
from tabs.WhatIfTab import WhatIfBasicTab, WhatIfExpertTab
from data.features_description import features_description
import shutil
from tabs.testAll import *

app = Dash(__name__)
server = app.server

explainer1 = ClassifierExplainer.from_file("src/dashboard1_explainer.dill")
explainer2 = ClassifierExplainer.from_file("src/dashboard2_explainer.dill")

db1 = ExplainerDashboard(explainer1, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer (Basic Interface)", 
                        tabs=[FeaturesImportanceBasicTab, WhatIfBasicTab],
                        description="In this dashboard, you can access the following tabs: Prediction and What If...")

db2 = ExplainerDashboard(explainer2, header_hide_selector=True, hide_poweredby=True, title="AutoML Student Dropout Explainer (Advanced Interface)", 
                        tabs=[AutoMLReportTab, FeaturesImportanceExpertTab, ClassificationStatsTab, WhatIfExpertTab, CounterfactualsTab],
                        description="In this dashboard, you can access the following tabs: AutoML Report, Feature Importances, Classificaction Stats, What If... and Counterfactual Scenarios.")

hub = ExplainerHub([db1, db2], title="Students Academic Failure Prediction Tool", 
                    description="The dataset was created in a project that aims to contribute to the reduction of academic dropout and failure in higher education, by using machine learning techniques to identify students at risk at an early stage of their academic path, so that strategies to support them can be put into place. The dataset includes information known at the time of student enrollment – academic path, demographics, and social-economic factors. The problem is formulated as a three category classification task (dropout, enrolled, and graduate) at the end of the normal duration of the course.\n Link to the dataset: https://www.kaggle.com/datasets/ankanhore545/dropout-or-academic-success")

hub.run(port='8080')
""" for x in range(1, 999):
    try:
        shutil.rmtree('AutoML_' + str(x))

    except:
        break """

if __name__ == "__main__":
    app.run(debug=False, port='8080')