import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/zipcodes.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# # Save references to each table
zipcode_data = Base.classes.zipcode_data
# Samples = Base.classes.samples

# Dummy CSV for interim
# dummy=pd.read_csv('dummy.csv')


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


# @app.route("/zips")
# def zips():
#     """Return the full list of zipcodes."""

#     # Use Pandas to perform the sql query
#     # stmt = db.session.query(Samples).statement
#     # df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     # return jsonify(list(df.columns)[2:])

#     # Using dummy data
#     # dummy_json={}
#     # for row in dummy:
#     #     zip = row[0]
#     #     dummy_json{zip}
#     return(jsonify(dummy.to_dict('records')))

@app.route("/income")
def income():
    """Return the list of zipcodes sorted by income (descending)."""
    sel = [
        zipcode_data.zipcode,
        zipcode_data.income, # Average invidiual income
    ]

    results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

    for result in results:
        print(result)

    # Create dataframe for results, to be sorted
    df = pd.DataFrame({
        "zipcode":[],
        "income":[]
    })

    # Counter for populating dataframe
    zipcodes=[]
    incomes=[]

    # Loop through results and create dataframe
    for result in results:
        zipcodes.append(result[0])
        incomes.append(result[1])

    df=pd.DataFrame({
        "zipcode":zipcodes,
        "income":incomes
    })
    
    # Sort dataframe
    sorted_df=df.sort_values(by=["income"],ascending=False)

    # Take top 10 zips from sorted dataframe
    shorted_df=sorted_df["zipcode"][0:10]

    # Return sorted zipcodes
    return(jsonify(list(shorted_df)))


# @app.route("/crime")
# def crime():
#     """Return the list of zipcodes sorted by crime (ascending)."""
#     sel = [
#         zipcode_data.zipcode,
#         zipcode_data.crmcytotc, # Crime - 100 = national average
#     ]

#     results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

#     # Create dataframe for results, to be sorted
#     df = pd.DataFrame({
#         "zipcode":[],
#         "crime":[]
#     })

#     # Counter for populating dataframe
#     count=0

#     # Loop through results and create dataframe
#     for result in results:
#         df["zipcode"][count]=result[0]
#         df["crime"][count]=result[1]
#         count=count+1
    
#     # Sort dataframe
#     sorted_df=df.sort_values(by=["crime"])

#     # Take top 10 zips from sorted dataframe
#     shorted_df=sorted_df["zipcode"][0:10]

#     # Return sorted zipcodes
#     return(jsonify(list(shorted_df)))

# @app.route("/education")
# def age():
#     """Return the list of zipcodes sorted by education (descending)."""
#     sel = [
#         zipcode_data.zipcode,
#         zipcode_data.edubach_00, # Average invidiual income
#         zipcode_data.daypop, # Day Time Population
#     ]

#     results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

#     # Create dataframe for results, to be sorted
#     df = pd.DataFrame({
#         "zipcode":[],
#         "education":[],
#         "population":[]
#     })

#     # Counter for populating dataframe
#     count=0

#     # Loop through results and create dataframe
#     for result in results:
#         df["zipcode"][count]=result[0]
#         df["education"][count]=result[1]
#         df["population"][count]=result[2]
#         count=count+1
    
#     df["pct_bachelors"] = df["education"]/df["population"]
    
#     # Sort dataframe
#     sorted_df=df.sort_values(by=["pct_bachelors"],ascending=False)

#     # Take top 10 zips from sorted dataframe
#     shorted_df=sorted_df["zipcode"][0:10]

#     # Return sorted zipcodes
#     return(jsonify(list(shorted_df)))

# @app.route("/climate")
# def age():
#     """Return the list of zipcodes sorted by average january temperature (descending)."""
#     sel = [
#         zipcode_data.zipcode,
#         zipcode_data.inccypcap, # Average invidiual income
#     ]

#     results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

#     # Create dataframe for results, to be sorted
#     df = pd.DataFrame({
#         "zipcode":[],
#         "income":[]
#     })

#     # Counter for populating dataframe
#     count=0

#     # Loop through results and create dataframe
#     for result in results:
#         df["zipcode"][count]=result[0]
#         df["income"][count]=result[1]
#         count=count+1
    
#     # Sort dataframe
#     sorted_df=df.sort_values(by=["income"],ascending=False)

#     # Take top 10 zips from sorted dataframe
#     shorted_df=sorted_df["zipcode"][0:10]

#     # Return sorted zipcodes
#     return(jsonify(list(sorted_zips)))

# @app.route("/cost")
# def age():
#     """Return the list of zipcodes sorted by cost of living (ascending)."""
#     sel = [
#         zipcode_data.zipcode,
#         zipcode_data.inccypcap, # Average invidiual income
#     ]

#     results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

#     # Create dataframe for results, to be sorted
#     df = pd.DataFrame({
#         "zipcode":[],
#         "income":[]
#     })

#     # Counter for populating dataframe
#     count=0

#     # Loop through results and create dataframe
#     for result in results:
#         df["zipcode"][count]=result[0]
#         df["income"][count]=result[1]
#         count=count+1
    
#     # Sort dataframe
#     sorted_df=df.sort_values(by=["income"],ascending=False)

#     # Take top 10 zips from sorted dataframe
#     shorted_df=sorted_df["zipcode"][0:10]

#     # Return sorted zipcodes
#     return(jsonify(list(sorted_zips)))


@app.route("/zipcodes")
def zipcode():
    """Return the stats for all zipcodes in CA."""
    sel = [
        zipcode_data.zipcode,
        zipcode_data.income, # Average invidiual income
        zipcode_data.crime, # Total crime - 100 = average
        zipcode_data.education, # Total population with a bachelors degree
        zipcode_data.jan_avg_temp, # Daytime population of the zip
        zipcode_data.cost_of_living, # Average temperature in January
        zipcode_data.state, # Costs associated with owned dwellings
        # zipcode_data.latitude,
        # zipcode_data.longitude,
        # zipcode_data.state,
    ]

    results = db.session.query(*sel).filter(zipcode_data.state == "06").all()

    # Create a dictionary for each zip code
    zip_info = {}

    # Loop through each result
    for result in results:
        # Create primaryzip code key
        zip_info[result[0]] = {
            # Populate dictionary entry with a second dictionary
            "income":result[1],
            "crime":result[2],
            "education":result[3],
            "winter_temp":result[4],
            "cost_of_living":result[5],
            # "lat":result[7],
            # "lon":result[8],
        }

    print(zip_info)
    return jsonify(zip_info)

# @app.route("/zipcodes/<zipcode>")
# def sample_metadata(zipcode):
#     """Return the full data set for a given sample."""
#     zip_data=dummy.loc[dummy["zipcode"]==zipcode]
#     print(zip_data)

#     zip_dict=zip_data.to_dict("records")
#     return(jsonify(zip_dict))

# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)

# @app.route("/wfreq/<sample>")
# def wfeq(sample):
#     """Return the WFREQ for a given sample."""
#     sel = [
#         zipcode_data.sample,
#         zipcode_data.WFREQ
#     ]

#     results = db.session.query(*sel).filter(zipcode_data.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["WFREQ"] = result[1]

#     print(sample_metadata)
#     return jsonify(sample_metadata)
    

if __name__ == "__main__":
    app.run()
