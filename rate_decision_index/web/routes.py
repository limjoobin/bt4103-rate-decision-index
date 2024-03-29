from flask import render_template, request
from web import app
from web.utils import utils, home_plot, macro_plot, market_plot, fedfundfutures_plot
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from werkzeug.utils import secure_filename
import os

from web.utils.paths import Path

# models
from models.fed_futures_model import run_main
from models.macro_model.indicator_index_plots import collect_indicator_data
from models.update_macro_data import update_saved_data
from models.sentiment_model import run_sentiment_model

# Setting data directory: saved to web/data
uploads_dir = os.path.join(os.path.dirname(app.instance_path), 'web/data')
os.makedirs(uploads_dir, exist_ok=True)

path = Path()

# Loading raw data and clean it
#market
final_dir = utils.load_market_data()
market_data_cleaned = utils.import_modify_pickle_ms_main(final_dir)
market_ngram_statement, market_ngram_min, market_ngram_news = utils.load_ngram_market_data()

#macro
gdp_data, employment_data, inflation_data = utils.load_macro_data()
macro_y_train, macro_y_test, macro_x_train, macro_x_test = utils.load_dir_macro_values()
macro_df = utils.clean_maindashboard_macro(macro_y_train, macro_y_test, macro_x_train, macro_x_test)
macro_ts_train, macro_ts_test, macro_pred_train, macro_pred_test = utils.load_dir_macro_ts()
macro_ts_df = utils.import_modify_pickle_overall_ts(macro_ts_train, macro_ts_test, macro_pred_train, macro_pred_test)
macro_main_data = utils.load_macro_model_data()

#fedfundfuture
fff_dir = utils.load_fff_data()
fff_data_cleaned = utils.import_modify_csv_fff(fff_dir)
#fedfundfuture vs fomc dot plot
fff_preds, fff_fomc = utils.load_fff_vs_fomc_data()

# gauge
gauge_final_data, fff_prob_data = utils.load_gauge_data()

# Save Pickle for Main Page in Dashboard
market_data_cleaned.to_pickle(f"./web/utils/pickle/market_data_cleaned.pickle")
macro_df.to_pickle(f"./web/utils/pickle/macro_df.pickle")
fff_data_cleaned.to_pickle(f"./web/utils/pickle/fff_data_cleaned.pickle")
macro_ts_df.to_pickle(f"./web/utils/pickle/macro_ts_df.pickle")
gauge_final_data.to_pickle(f"./web/utils/pickle/gauge_final_data.pickle")
fff_prob_data.to_pickle(f"./web/utils/pickle/fff_prob_data.pickle")

#to change the data for home and start page
@app.route("/",  methods=['GET', 'POST'])
def plot_main_dashboard():
    form = PostForm()
    
    if request.method == 'POST':
        date = request.form['date-mm']
        #ploting
        print('DATE IS HERE', date)
        
        #market
        plot_market_senti_main = home_plot.plot_market(market_data_cleaned, date)
        plot_market_average = home_plot.plot_market_average(market_data_cleaned, date)
        
        #macro
        macro_maindashboard_plot = home_plot.plot_macro_maindashboard(macro_df, date)
        macro_pie_chart = home_plot.plot_contributions_pie(macro_df, date)
        
        #fff
        plot_fff = home_plot.plot_fff(fff_data_cleaned)

        # overall 
        macro_ts_plot = home_plot.plot_fed_rates_ts(macro_ts_df)

        plot_gauge = home_plot.plot_gauge(gauge_final_data, fff_prob_data, date)
        context = {
                "plot_market_senti_main": plot_market_senti_main,
                "plot_market_average": plot_market_average,
                'plot_fff': plot_fff,
                "plot_gauge": plot_gauge,
                'macro_ts_plot':macro_ts_plot,
                'macro_maindashboard_plot':macro_maindashboard_plot,
                'macro_pie_chart':macro_pie_chart}
        return render_template('home.html', context=context, form=form)
    else:
        #ploting
        #market
        plot_market_senti_main = home_plot.plot_market(market_data_cleaned, '2008-09')
        plot_market_average = home_plot.plot_market_average(market_data_cleaned, '2008-09')
        
        #macro
        macro_maindashboard_plot = home_plot.plot_macro_maindashboard(macro_df, '2008-09')
        macro_pie_chart = home_plot.plot_contributions_pie(macro_df, '2008-09')
        
        #fff
        plot_fff = home_plot.plot_fff(fff_data_cleaned)

        # overall 
        macro_ts_plot = home_plot.plot_fed_rates_ts(macro_ts_df)
        plot_gauge = home_plot.plot_gauge(gauge_final_data, fff_prob_data, '2008-09')

        context = {
                "plot_market_senti_main": plot_market_senti_main,
                "plot_market_average": plot_market_average,
                'plot_fff': plot_fff,
                "plot_gauge": plot_gauge,
                'macro_ts_plot':macro_ts_plot,
                'macro_maindashboard_plot':macro_maindashboard_plot,
                'macro_pie_chart':macro_pie_chart}
        return render_template('home.html', context=context, form=form)

@app.route("/upload")
def upload_file():
    return render_template('model-run.html')

@app.route("/runfff", methods = ['GET', 'POST'])
def run_fff_model():
    data_path = path.fed_funds_data
    run_main(path = data_path)
    return render_template('model-run.html')

@app.route('/run', methods = ['GET', 'POST'])
def run_all_models():
    # run FFF model
    print("===== Running Federal Funds Model =====")
    fed_funds_data_path = path.fed_funds_data
    run_main(path = fed_funds_data_path)

    # # collect Macroeconomic Indicators data for index breakdown
    print("===== Running Macroindicators Breakdown =====")
    macro_data_path = path.macroeconomic_indicators_data
    collect_indicator_data(path = macro_data_path)

    # run sentiment model
    print("===== Running Market Consensus/Sentiment Model =====")
    sentiment_data_path = path.sentiment_data
    extract_path = path.sentiment_extract_data
    run_sentiment_model(path=sentiment_data_path, extract_path=extract_path)

    # update macro data 
    print("===== Running Macroeconomic Model =====")
    sentiment_hist_path = path.sentiment_hist_data
    update_saved_data(path_to_folder=macro_data_path, path_to_HD_folder=sentiment_hist_path)

    print("********** All Models Completed! *************")
    return render_template('model-run.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      path = os.path.join(uploads_dir, secure_filename(f.filename))
      f.save(path)
      return 'file uploaded successfully'

class PostForm(FlaskForm):
    date = StringField('date', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/home",  methods=['GET', 'POST'])
def plot_home():
    form = PostForm()
    
    if request.method == 'POST':
        date = request.form['date-mm']
        #ploting
        print('DATE IS HERE', date)
        
        #market
        plot_market_senti_main = home_plot.plot_market(market_data_cleaned, date)
        plot_market_average = home_plot.plot_market_average(market_data_cleaned, date)
        
        #macro
        macro_maindashboard_plot = home_plot.plot_macro_maindashboard(macro_df, date)
        macro_pie_chart = home_plot.plot_contributions_pie(macro_df, date)
        
        #fff
        plot_fff = home_plot.plot_fff(fff_data_cleaned)

        # overall 
        macro_ts_plot = home_plot.plot_fed_rates_ts(macro_ts_df)

        plot_gauge = home_plot.plot_gauge(gauge_final_data, fff_prob_data, date)
        context = {
                "plot_market_senti_main": plot_market_senti_main,
                "plot_market_average": plot_market_average,
                'plot_fff': plot_fff,
                "plot_gauge": plot_gauge,
                'macro_ts_plot':macro_ts_plot,
                'macro_maindashboard_plot':macro_maindashboard_plot,
                'macro_pie_chart':macro_pie_chart}
        return render_template('home.html', context=context, form=form)
    else:
        #ploting
        #market
        plot_market_senti_main = home_plot.plot_market(market_data_cleaned, '2008-09')
        plot_market_average = home_plot.plot_market_average(market_data_cleaned, '2008-09')
        
        #macro
        macro_maindashboard_plot = home_plot.plot_macro_maindashboard(macro_df, '2008-09')
        macro_pie_chart = home_plot.plot_contributions_pie(macro_df, '2008-09')
        #fff
        plot_fff = home_plot.plot_fff(fff_data_cleaned)

        # overall 
        macro_ts_plot = home_plot.plot_fed_rates_ts(macro_ts_df)
        plot_gauge = home_plot.plot_gauge(gauge_final_data, fff_prob_data, '2008-09')

        context = {
                "plot_market_senti_main": plot_market_senti_main,
                "plot_market_average": plot_market_average,
                'plot_fff': plot_fff,
                "plot_gauge": plot_gauge,
                'macro_ts_plot':macro_ts_plot,
                'macro_maindashboard_plot':macro_maindashboard_plot,
                'macro_pie_chart':macro_pie_chart}
        return render_template('home.html', context=context, form=form)

class PostForm2(FlaskForm):
    date = StringField('date', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/market-consensus",  methods=['GET', 'POST'])
def plot_market_consensus():
    form2 = PostForm2()
    
    if request.method == 'POST':
        date = request.form['date']
        print("DATE IS HERE", date)
        print(type(date))
        #ploting
        market_ts_plot = market_plot.plot_hd_ts(market_data_cleaned)
        ngram_min = market_plot.get_top_n_gram_mins(market_ngram_min, date=date)
        ngram_statement = market_plot.get_top_n_gram_st(market_ngram_statement, date=date)
        ngram_news = market_plot.get_top_n_gram_news(market_ngram_news, date=date)

        context = {
                'market_ts_plot':market_ts_plot,
                'ngram_min': ngram_min, 
                'ngram_statement':ngram_statement,
                'ngram_news':ngram_news}
        return render_template('market-consensus.html', context=context, form=form2)
    else:
        #ploting
        market_ts_plot = market_plot.plot_hd_ts(market_data_cleaned)
        ngram_min = market_plot.get_top_n_gram_mins(market_ngram_min, date=2004)
        ngram_statement = market_plot.get_top_n_gram_st(market_ngram_statement, date=2004)
        ngram_news = market_plot.get_top_n_gram_news(market_ngram_news, date=2004)

        context = {
                'market_ts_plot':market_ts_plot,
                'ngram_min': ngram_min, 
                'ngram_statement':ngram_statement,
                'ngram_news':ngram_news}
        return render_template('market-consensus.html', context=context, form=form2)

@app.route("/macroeconomic-indicators")
def plot_macroeconomic_indicators():
    #ploting
    plot_gdp_index = macro_plot.plot_gdp_index(gdp_data)
    plot_employment_index = macro_plot.plot_employment_index(employment_data)
    plot_inflation_index = macro_plot.plot_inflation_index(inflation_data)
    plot_main_model = macro_plot.plot_main_plot(macro_main_data)
    context = {'plot_gdp_index': plot_gdp_index, 
               'plot_employment_index': plot_employment_index, 
               'plot_inflation_index': plot_inflation_index, 
               'plot_main_model': plot_main_model, 
               }
    return render_template('macroeconomic-indicators.html', context=context)
    
@app.route("/fedfundfutures")
def plot_fedfundfutures():
    #ploting - add plots here and in context
    plot_fff_results = fedfundfutures_plot.plot_fff_results(fff_data_cleaned)
    plot_futures_pred_vs_fomc = fedfundfutures_plot.plot_futures_pred_vs_fomc(fff_preds, fff_fomc)
    context = {'plot_fff_results': plot_fff_results,
               'plot_futures_pred_vs_fomc': plot_futures_pred_vs_fomc} 
    return render_template('fedfundfutures.html', context=context)