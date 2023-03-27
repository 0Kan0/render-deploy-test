from io import StringIO
import pandas as pd
import dice_ml as dml


from ..testAll import *
from dash.dependencies import Input, Output, State
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from explainerdashboard.custom import *

class AutoMLReportComponent(ExplainerComponent):
    def __init__(self, explainer, title="AutoML Report", name=None, 
                        subtitle="Compare all models used and see which one fits the best", ):

        super().__init__(explainer, title, name)

    def layout(self):
        return dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.H3(self.title, className="card-title", id='automlreport-title-'+self.name),
                    html.H6(self.subtitle, className='card-subtitle')
                ]),
            ]),
            """ dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Iframe(srcDoc=model_report.data, style={'width': '100%', 'height': '1000px'})
                    ]),
                ], class_name="mt-4")
            ]) """
        ], class_name="h-100")

class SelectStudentComponent(ExplainerComponent):

    def __init__(self, explainer, title="Select Random Student", name=None,
                        subtitle="Select from list or pick at random",
                        index_dropdown=True,
                        pos_label=None, index=None, slider= None, labels=None,
                        pred_or_perc='predictions', description=None,
                        **kwargs):
        
        super().__init__(explainer, title, name)
        assert self.explainer.is_classifier, \
            ("explainer is not a ClassifierExplainer ""so the ClassifierRandomIndexComponent "
            " will not work. Try using the RegressionRandomIndexComponent instead.")
        self.index_name = 'random-index-clas-index-'+self.name

        if self.slider is None:
            self.slider = [0.0, 1.0]

        if self.labels is None:
            self.labels = self.explainer.labels

        if self.explainer.y_missing:
            self.hide_labels = True

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.index_selector = IndexSelector(explainer, 'random-index-clas-index-'+self.name,
                                    index=index, index_dropdown=True, **kwargs)

        assert (len(self.slider) == 2 and
                self.slider[0] >= 0 and self.slider[0] <=1 and
                self.slider[1] >= 0.0 and self.slider[1] <= 1.0 and
                self.slider[0] <= self.slider[1]), \
                    "slider should be e.g. [0.5, 1.0]"

        assert all([lab in self.explainer.labels for lab in self.labels]), \
            f"These labels are not in explainer.labels: {[lab for lab in self.labels if lab not in explainer.labels]}!"

        assert self.pred_or_perc in ['predictions', 'percentiles'], \
            "pred_or_perc should either be `predictions` or `percentiles`!"

    def layout(self):
        return dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.H3(f"Select student", id='random-index-clas-title-'+self.name),
                        html.H6(self.subtitle, className='card-subtitle'), 
                    ]), 
                ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        self.index_selector.layout()
                    ], width=8, md=8), 
                    make_hideable(
                        dbc.Col([
                            self.selector.layout()
                        ], md=2), 
                    hide=True),
                ], class_name="mb-2"),

                dbc.Row([
                    dbc.Col([
                        dbc.Button(f"Random student", color="primary", id='random-index-clas-button-'+self.name),
                    ], width=4, md=4), 
                ], class_name="mb-2"),
                
                dbc.Row([
                    make_hideable(
                        dbc.Col([
                            dbc.Label(f"Observed {self.explainer.target}:", id='random-index-clas-labels-label-'+self.name),
                            dcc.Dropdown(
                                id='random-index-clas-labels-'+self.name,
                                options=[{'label': lab, 'value': lab} for lab in self.explainer.labels],
                                multi=True,
                                value=self.labels),
                        ], width=8, md=8),
                        hide=True),
                    make_hideable(
                        dbc.Col([
                            dbc.Label(
                                "Range:", html_for='random-index-clas-pred-or-perc-'+self.name),
                            dbc.Select(
                                id='random-index-clas-pred-or-perc-'+self.name,
                                options=[
                                    {'label': 'probability',
                                        'value': 'predictions'},
                                    {'label': 'percentile',
                                        'value': 'percentiles'},
                                ],
                                value=self.pred_or_perc),
                        ], width=4,
                        id='random-index-clas-pred-or-perc-div-'+self.name),
                        hide=True)
                ], class_name="mb-2"),
                dbc.Row([
                    make_hideable(
                        dbc.Col([
                            html.Div([
                                dbc.Label(id='random-index-clas-slider-label-'+self.name,
                                    children="Predicted probability range:",
                                    html_for='prediction-range-slider-'+self.name),
                                dcc.RangeSlider(
                                    id='random-index-clas-slider-'+self.name,
                                    min=0.0, max=1.0, step=0.01,
                                    value=self.slider,  allowCross=False,
                                    marks={0.0:'0.0', 0.2:'0.2', 0.4:'0.4', 0.6:'0.6', 
                                            0.8:'0.8', 1.0:'1.0'},
                                    tooltip = {'always_visible' : False})
                            ])
                        ]), 
                    hide=True),
                ], justify="start"),
            ]),
        ], class_name="h-100")

    def to_html(self, state_dict=None, add_header=True):
        args = self.get_state_args(state_dict)
        
        html = to_html.card(f"Selected index: <b>{self.explainer.get_index(args['index'])}</b>", title=self.title)
        if add_header:
            return to_html.add_header(html)
        return html

    def component_callbacks(self, app):
        @app.callback(
            Output('random-index-clas-index-'+self.name, 'value'),
            [Input('random-index-clas-button-'+self.name, 'n_clicks')],
            [State('random-index-clas-slider-'+self.name, 'value'),
             State('random-index-clas-labels-'+self.name, 'value'),
             State('random-index-clas-pred-or-perc-'+self.name, 'value'),
             State('pos-label-'+self.name, 'value')])
        def update_index(n_clicks, slider_range, labels, pred_or_perc, pos_label):
            if n_clicks is None and self.index is not None:
                raise PreventUpdate
            if pred_or_perc == 'predictions':
                return self.explainer.random_index(y_values=labels,
                    pred_proba_min=slider_range[0], pred_proba_max=slider_range[1],
                    return_str=True, pos_label=pos_label)
            elif pred_or_perc == 'percentiles':
                return self.explainer.random_index(y_values=labels,
                    pred_percentile_min=slider_range[0], pred_percentile_max=slider_range[1],
                    return_str=True, pos_label=pos_label)

        @app.callback(
            [Output('random-index-clas-slider-label-'+self.name, 'children'),
             Output('random-index-clas-slider-label-tooltip-'+self.name, 'children')],
            [Input('random-index-clas-pred-or-perc-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')]
        )
        def update_slider_label(pred_or_perc, pos_label):
            if pred_or_perc == 'predictions':
                return (
                    "Predicted probability range:",
                    f"Only select a random {self.explainer.index_name} where the "
                    f"predicted probability of {self.explainer.labels[pos_label]}"
                    " is in the following range:"
                )
            elif pred_or_perc == 'percentiles':
                return (
                    "Predicted percentile range:",
                    f"Only select a random {self.explainer.index_name} where the "
                    f"predicted probability of {self.explainer.labels[pos_label]}"
                    " is in the following percentile range. For example you can "
                    "only sample from the top 10% highest predicted probabilities."
                )
            raise PreventUpdate

class CounterfactualsComponent(ExplainerComponent):

    def __init__(self, explainer, title="Counterfactuals scenarios", name=None,
                        subtitle="What can a student improve?",
                        index_dropdown=True, index=None,
                        **kwargs):
        
        super().__init__(explainer, title, name)

        self.index_selector = IndexSelector(explainer, 'random-index-clas-index-'+self.name,
                                    index=index, index_dropdown=index_dropdown, **kwargs)

    def layout(self):
        return dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.H3(f"Select student and number of counterfactual scenarios", id='random-index-clas-title-'+self.name),
                        html.H6(self.subtitle, className='card-subtitle'), 
                    ]), 
                ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        self.index_selector.layout()
                    ], width=8, md=8), 
                ], class_name="mb-2"),

                dbc.Row([
                    dbc.Col([
                        dbc.Input(id="input",
                                  placeholder="Enter the number of scenarios between 1 and 10",
                                  type="number",
                                  debounce=True,
                                  min=1,
                                  max=10,
                                  value=None)
                    ], width=8, md=8),
                ], class_name="mb-2"),

                dbc.Row([
                    dbc.Col([
                        dbc.Button(f"Generate scenarios", color="primary", id="button"),
                    ], width=4, md=4), 
                ], class_name="mb-2"),

                dbc.Spinner(dbc.Row([
                    dash_table.DataTable(id='tbl', data=None, style_table={'overflowX': 'scroll'})
                ], class_name="mb-2")),
            ]),
        ], class_name="h-100")

    def to_html(self, state_dict=None, add_header=True):
        args = self.get_state_args(state_dict)
        
        html = to_html.card(f"Selected index: <b>{self.explainer.get_index(args['index'])}</b>", title=self.title)
        if add_header:
            return to_html.add_header(html)
        return html

    def component_callbacks(self, app):
        @app.callback(
            Output('tbl', 'data'),
            Output('tbl', 'columns'),
            [State('random-index-clas-index-'+self.name, 'value'),
            State('input', 'value')],
            [Input('button', 'n_clicks')]
        )

        def generate_scenarios(index, input, n_clicks):
            if (index is None or input is None or n_clicks is None):
                return None
            
            else:
                df_student = df
                df_student = df_student.drop(columns=["Target"]).loc[[index]]

                data = dml.Data(dataframe=df, continuous_features=["Unemployment rate", "Inflation rate", "GDP", 
                                                                "Curricular units 1st sem (grade)", "Curricular units 2nd sem (grade)", 
                                                                "Previous qualification (grade)", "Admission grade"], outcome_name="Target")
                
                model = dml.Model(model=trained_model, backend="sklearn")

                exp = dml.Dice(data, model)

                dice_exp = exp.generate_counterfactuals(df_student, total_CFs=input, desired_class=1)

                cf_object = dice_exp.cf_examples_list[0].final_cfs_df

                cf_object_to_csv = cf_object.to_csv(index=False)
                cf_object_to_csv = pd.read_csv(StringIO(cf_object_to_csv))

                data = cf_object_to_csv.to_dict('records')
                columns = [{"name": i, "id": i} for i in cf_object_to_csv.columns]

                return data, columns