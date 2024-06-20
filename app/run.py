from flask import Flask, render_template, request
import pandas as pd
import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# functions to generate the data used by the plots
from functions.answer_questions.answer_question_4_and_7 import forecast_next_24_hours_output_flow_rate
from functions.answer_questions.answer_question_5 import simulate_empyting_reservoir

# functions to generate the plots
from functions.plots.question_2_plots import generate_question_2_plot_1, generate_question_2_plot_2
from functions.plots.question_3_plots import generate_question_3_plot_1, generate_question_3_plot_2
from functions.plots.question_4_and_7_plots import create_questions_4_and_7_plot_1
from functions.plots.question_5_plots import create_question_5_plot
from functions.plots.question_6_plots import generate_question_6_plots

