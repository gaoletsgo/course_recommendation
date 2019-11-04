import dash
# import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.tools as tls
import plotly.graph_objects as go 
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_table
import pickle
from dash.exceptions import PreventUpdate
# from dash_canvas import DashCanvas
import base64




from Data import Data
import seaborn as sns
import sklearn as sk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_similarity_score
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import pdist, jaccard
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

data = Data("dataset/UQDataset_5_5639_m.csv")
c2s = data.get_int_dataset(data.get_all_course2student())
s2c = data.get_int_dataset(data.get_all_student2course())
# full_table = pd.DataFrame(data.get_fulltable())

code2ind = pickle.load(open("temp/course_code_to_index.txt", "rb"))
code2name = pickle.load(open("temp/course_code_to_name.txt","rb"))
ind2code = pickle.load(open("temp/course_index_to_code.txt","rb"))

model = pickle.load(open("temp/model.txt", "rb"))

all_courses = data.get_courses()

sig_course = [15 ,25, 23, 20, 38, 39, 18, 47, 72, 65, 90, 24, 80, 89, 10, 97, 68, 30, 64, 44, 28, 60, 81, -1]



# scale the value.
s2c[(s2c<4) & (s2c>0)] = 1
s2c[(s2c<6) & (s2c>3)] = 2
s2c[s2c>5] = 3

# statistics of all course number, grade distribution.
tot_students = []
for n in range(0, len(c2s)):
    tot_students.append(len(np.where(s2c[:,n]!=0)[0]))

df_c2s_int = pd.DataFrame(data.get_int_dataset(c2s))
df_s2c_int = pd.DataFrame(data.get_int_dataset(s2c))
df_s2c_int.columns = data.get_courses()

# course correlation matrix.
corr_mat = df_s2c_int.corr()
course_distance = pd.DataFrame(pairwise_distances(corr_mat, metric="correlation"))
# student similarity matrix.
bin_s2c = df_s2c_int
bin_s2c[bin_s2c!=0] = 1
bin_s2c = pd.DataFrame(bin_s2c)
student_distance = pd.DataFrame(pairwise_distances(bin_s2c, metric="hamming"))
jac_sim = pd.DataFrame(1-student_distance)

course_clustering_dist = pickle.load(open("temp/course_distance.txt", "rb"))
student_clustering_dist = pickle.load(open("temp/student_distance.txt", "rb"))

course_index = pd.Index(course_clustering_dist["labels"], name="labels").value_counts()
c_stat = pd.DataFrame(
    {"labels": course_index.index.to_list(),"count": course_index.values}
)
student_index = pd.Index(student_clustering_dist["labels"], name="labels").value_counts()
s_stat = pd.DataFrame(
    {"labels": student_index.index.to_list(), "count": student_index.values}
)



# clustering = AgglomerativeClustering(n_clusters=8, affinity="precomputed", linkage="complete").fit(course_distance)

# plot_mat = course_distance.iloc[:, 3:10]
# plot_mat[17] = clustering.labels_


def get_course_grades(course_index):
    fail = len(np.where(s2c[:, course_index] == 1)[0])
    credit = len(np.where(s2c[:, course_index] == 2)[0])
    dist = len(np.where(s2c[:, course_index] == 3)[0])
    return [fail, credit, dist]




app = dash.Dash(__name__ , meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.layout = html.Div(
    [   
        html.Div(  #row
            [
                html.Div(  #sleelct-window
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-1",
                            children=[

                                dcc.Tab(
                                    label="View Data",
                                    value="tab-1",
                                    children=[
                                        html.Div(
                                            [
                                                html.Div("Overview: "),
                                                dcc.RadioItems(
                                                    
                                                    options=[
                                                        {"label": "Data table", "value":"dt"},
                                                        {"label": "Data statistac", "value":"vd-stat"},
                                                    ],
                                                    value="dt",
                                                    style={"display": "inline"}
                                                
                                                ),
                                                html.Div("View Course: "),
                                                html.Div("Input Course Code : "),
                                                dcc.Input(
                                                    placeholder="course code",
                                                    type="text",
                                                
                                                    id="pie-course-code"
                                                ),
                                                html.Button("View", id="view-course"),
                                            ]
                                        )
                                    ],
                                ),
                                dcc.Tab(
                                    label="Heatmap",
                                    value="tab-2",
                                    children=[
                                        html.Div([
                                            html.P("Choose to view correlation heatmap:"),
                                            html.Button("Course", id="hm-course",n_clicks_timestamp=0, style={"margin-left":"60%"}),
                                            dcc.Input(
                                                type="text",
                                                value="0",
                                                id="s-range-1",
                                                style={"width":"30%"}
                                            ),
                                            dcc.Input(
                                                type="text",
                                                value="100",
                                                id="s-range-2",
                                                style={"width": "30%"}
                                            ),
                                            html.Button("Student", id="hm-student",n_clicks_timestamp=0, style={"margin-left":"5%"}),
                                        ])
                                    ]
                                ),
                                dcc.Tab(
                                    label="Clustering",
                                    value="tab-3",
                                    children=[
                                        html.Div(
                                            [
                                                html.P("Choose to view clustering results: "),
                                                 dcc.RadioItems(
                                                    id="clu-cs",
                                                    options=[
                                                        {"label": "Course Clustering", "value": "c"},
                                                        {"label": "Student Clustering", "value": "s"},
                                                    ],
                                                    value="c"
                                                ),

                                                dcc.Dropdown(
                                                    id="clu-drop",
                                                    options=[
                                                        {"label": "Parallel Coordinates", "value":"pc"},
                                                        {"label": "Statistics", "value":"sta"},
                                                        {"label": "Silhouette Coefficient", "value": "sil"}
                                                    ],
                                                    value="pc"
                                                ),

                                               
                                            ]
                                        )
                                    ]
                                ),
                                # dcc.Tab(
                                #     label="Association Rules",
                                #     value="tab-4",
                                #     children=[
                                #         html.Div(
                                #             [

                                #             ]
                                #         )
                                #     ]
                                # ),
                            ],
                            style={"font-size": "14px","text-align": "center"}
                        ),
                    ],
                    className="four columns pretty_container"
                ),

                dcc.Loading(
                    className = "eight columns pretty_container",
                    id="loading",
                    style={"margin-left":"10px", "height": "70%"},
                    children=[
                        html.Div(dcc.Graph(style={"height": "800px"},figure=go.Figure(data=[go.Pie(labels=data.get_courses(), values=tot_students, hole=.2)]))),
                    ]
                ),
                # html.Div( # plot-window
                #     [

                        
                        # html.Div(
                        #     [
                        #         dash_table.DataTable(
                        #             columns=[{"name": i, "id": i} for i in df_s2c_int.columns],
                        #             data= df_s2c_int.to_dict("records"),
                        #             style_table={
                        #                 "maxHeight": "300",
                        #                 "maxWidth": "500",
                        #                 "overflow": "scroll"
                        #             }
                        #         )
                        #     ]
                        # ),

                        # html.Div(
                        #     [

                        #         dcc.Graph(figure=go.Figure(data=[go.Pie(labels=data.get_courses(), values=tot_students, hole=.2)])),
                        #         dcc.Graph(
                        #             figure=go.Figure(
                        #                 data=[
                        #                     go.Pie(labels=["Fail","Credit","Distinct+"], values=get_course_grades(4), hole=.2)
                        #                     ],
                        #                 layout=go.Layout(
                        #                     title=all_courses[4]+"  Total students: "+str(tot_students[4])
                        #                 ),
                        #             ),
                        #             id="1-course",
                        #         )
                        #     ]
                        # ),
                        # html.Div(
                        #     [
                        #         dcc.Graph( figure=go.Figure(data=go.Heatmap(z=corr_mat))),
                        #     ],
                        #     id="heatmap",

                        # ),
                        
                        # html.Div(
                        #     [
                        #         dcc.Graph( figure=px.parallel_coordinates(plot_mat, color=17)),
                                
                        #     ],
                        #     id="cluster-plot",
                        # ),
                        
                        # html.Div(
                        #     [
                        #         dcc.Graph(figure=px.box(df_s2c_int, x="comp4500_comp7500", y="infs3200_infs7907")),
                                
                        #     ] ,
                        #     id="boxplot", 
                        # ),
                        
                        # html.Div(
                        #     [
                        #         # dcc.Graph(id="heatmap", figure=go.Figure(data=go.Heatmap(z=corr_mat)))
                        #     ]  
                        # ),
                        
                        # html.Div(
                        #     [
                        #         # dcc.Graph(id="heatmap", figure=go.Figure(data=go.Heatmap(z=corr_mat)))
                        #     ]  
                        # )
                #     ],

                #     className = "eight columns pretty_container",
                #     id = "plot-window right-column",
                #     style={"margin-left":"10px"}
                # )
            ],
            className="row flex-display",
        ),

        # recommendation
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Input your enrolment history: "),
                        html.Div(
                            [
                                html.P("Input course code: "),
                                dcc.Input(
                                    placeholder="code,code,code...",
                                    value="",
                                    id="rec-code"
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.P("Input course grade: "),
                                dcc.Input(
                                    placeholder="grade,grade,grade...",
                                    value="",
                                    id="rec-grade"
                                )
                            ]
                        ),
                        html.Button(
                            "Recommend Courses",
                            id="rec-btn"
                        )
                    ],
                    className="four columns"
                ),

                # results
                html.Div(
                    [

                    ],
                    id="rec-result",
                    className = "eight columns"
                )
            ],
            id="recom",
            className = "pretty_container row"
        )
     
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)




@app.callback(
    Output("loading", "children"),
    [Input("tabs", "value"),
    Input("hm-student", "n_clicks_timestamp"),
    Input("hm-course", "n_clicks_timestamp"),
    Input("view-course", "n_clicks"),
    Input("clu-cs", "value"),
    Input("clu-drop", "value")],
    [State("s-range-1", "value"), State("s-range-2", "value"), State("pie-course-code", "value")]
)

def switch_page(value, s,c,view_course,ratio_clu,drop_clu,range_1, range_2,course_code):
    if value == "tab-1":
        if course_code is None:
            return html.Div(dcc.Graph(style={"height": "800px"},figure=go.Figure(data=[go.Pie(labels=data.get_courses(), values=tot_students, hole=.2)],
            layout=go.Layout(
                title="Dataset Overview"
            )))),
        else:
            index = int(code2ind[course_code])
            return html.Div(
                dcc.Graph(
                    style={"height": "800px"},
                    figure=go.Figure(
                        data=[go.Pie(labels=["Fail","Credit","Distinct+"],values=get_course_grades(index), hole=.2)],
                        layout=go.Layout(
                            title=all_courses[index]+"  Total students: "+str(tot_students[index])
                        )
                    )

                )
            ),
    elif value == "tab-2":
        if int(c) >= int(s):
            return html.Div(
                    [
                        dcc.Graph( style={"height": "800px"},figure=go.Figure(data=go.Heatmap(z=corr_mat),layout=go.Layout(title="Course Correlation Heatmap"))),
                    ],
                    id="heatmap",

                    ),
        elif int(s) > int(c):
            y_label = np.arange(int(range_1), int(range_2)).astype(str)
            return html.Div(
                    [   
                       
                        dcc.Graph( style={"height": "800px"},figure=go.Figure(data=go.Heatmap(z=jac_sim[int(range_1):int(range_2)],y=y_label),layout=go.Layout(title="Student Similarity Heatmap"))),
                    ],
                    id="heatmap",

                ),
    elif value == "tab-3":

        if ratio_clu == "c":
            if drop_clu == "pc":
                # pca = PCA(n_components= 0.6)
                # pca.fit(cours)
                return html.Div(
                    [
                        dcc.Graph(
                            figure=px.parallel_coordinates(course_clustering_dist.iloc[:,sig_course], color="labels"),
                        )
                    ]
                )
            elif drop_clu == "sta":
                return html.Div(
                    [
                        dcc.Graph(
                            figure=px.bar(c_stat, x="labels", y="count")
                        )
                    ]
                )
            elif drop_clu == "sil":
                encoded_image = base64.b64encode(open("img/c_cluster.png", 'rb').read())
                return html.Div(
                    [
                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
                    ]
                )
        elif ratio_clu ==  "s":
            if drop_clu == "pc":
                return html.Div(
                    [
                        dcc.Graph(
                            figure=px.parallel_coordinates(student_clustering_dist, color="labels"),
                        )
                    ]
                ) 
            elif drop_clu == "sta":
               
                return html.Div(
                        [
                            dcc.Graph(
                                figure=px.bar(s_stat, x="labels", y="count")
                            )
                        ]
                    )

            elif drop_clu == "sil":
                encoded_image = base64.b64encode(open("img/s_cluster.png", 'rb').read())
                return html.Div(
                    [
                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
                    ]
                )

@app.callback(
    Output("rec-result", "children"),
    [Input("rec-btn", "n_clicks")],
    [State("rec-code", "value"),State("rec-grade", "value")]
)
def recommend(btn, code, grade):
    if code == "" or grade == "":
        raise PreventUpdate
    else:

        courses = code.split(",")
        g = np.array([grade.split(",")]).astype(np.int64)
        c_ind = np.array([code2ind[c] for c in courses])

        r_rec = model.genenate_recommendation(c_ind, g)
        record = np.zeros(106).astype(np.int64)
        record[c_ind.astype(np.int64)] = g

        # rec_list = r_rec.keys()
        enrols = c_ind.astype(np.int64)
        c_rec = model.c_rec(enrols)
        s_rec = model.s_rec(record)
        print(s2c)
        # np.set_printoptions(threshold=np.inf)

        # for c in r_rec.keys()



        dic = {1: "Fail", 2:"Credit", 3:"Distinction+"}

        return html.Div(
            [   
                html.Div(
                    [
                        html.H5("Recommend by Course Clustering Result: "),
                        html.H6("*Similar courses to your enrolled courses"),
                        html.Ul(
                            [
                                html.Li(""+str(code2name[ind2code[str(c)][0]])+".        * Your have\
                                     "+str(round(model.predict_grade(enrols, g, int(c), s2c)[0]*100,2))+"% to get\
                                         '"+dic[int(model.predict_grade(enrols,g,int(c),s2c)[1])]+"'.") for c in c_rec
                            ]
                            
                        )
                       
                    ]
                ),
                html.Div(
                    [
                        html.H5("Recommend by Student Clustering Result: "),
                        html.H6("* Courses from your similar students"),
                        html.Ul(
                            [
                                html.Li(""+str(code2name[ind2code[str(c)][0]])+". "     )for c in list(s_rec)
                            ]
                            #   * Your have\
                            #          "+str(round(model.predict_grade(enrols, g, int(c), s2c)[0]*100,2))+"% to get\
                            #              '"+dic[int(model.predict_grade(enrols,g,int(c),s2c)[1])]+"'.") 
                        )
                    ]
                ),
                html.Div(
                    [
                        html.H5("Recommend by Association Rules: ")
                    ]
                ),
                html.Div(
                    [
                        html.P("Recommend to enroll: {\
                        "+str(code2name[ind2code[items[0]][0]])+"} because "+str(round(items[1]["conf"]*100,2))+"% \
                            who enrolled "+str([code2name[ind2code[c][0]] for c in items[1]["if_set"]])+" also enrolled this course.\
                            * Based on your grades, you have "+str(round(model.predict_grade(enrols, g, int(items[0]), s2c)[0]*100,2))+"% to get\
                                '"+dic[int(model.predict_grade(enrols,g,int(items[0]), s2c)[1])] +"'.") for items in r_rec.items()
                    
                    ]
                )
             
                
            ]
        )
        






        # encoded_image_s = base64.b64encode(open("img/s_cluster.png", 'rb').read())
        # encoded_image_c = base64.b64encode(open("img/c_cluster.png", 'rb').read())

        # return html.Div(
        #     [
        #         html.Img(src='data:image/png;base64,{}'.format(encoded_image_s.decode())),
        #         html.Img(src='data:image/png;base64,{}'.format(encoded_image_c.decode())),

        #     ]
        # )


if __name__ == "__main__":
    app.run_server(debug=True)