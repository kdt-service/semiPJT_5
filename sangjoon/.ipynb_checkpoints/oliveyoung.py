import yfinance as yf
import streamlit as st
import pandas as pd

from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go

START = '2018-01-01'
TODAY = date.today().strftime("%Y-%m-%d")
