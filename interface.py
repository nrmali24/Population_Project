from flask import Flask,jsonify,render_template,request
import numpy as np
import os
import config
from flask_mysqldb import MySQL
import pickle
import json

app=Flask(__name__)

#for connection with sql database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Mysql1234"
app.config["MYSQL_DB"] = "nileshdb"
mysql = MySQL(app)

#for loading the path
with open(config.model_path,"rb")as file:
    model=pickle.load(file)
with open(config.project_data,"r")as file:
    columns = json.load(file)

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/population",methods=["GET","POST"])
def get_pop():
    data=request.form
    test_array=np.zeros(len(columns["columns"]))
    test_array[0]=eval(data["Yearly change"])
    a=test_array[0]
    test_array[1]=eval(data["Net change"])
    b=test_array[1]
    test_array[2]=eval(data["Density (P/Km²)"])
    c=test_array[2]
    test_array[3]=eval(data["Migrants (net)"])
    d=test_array[3]
    test_array[4]=eval(data["Fert. Rate"])
    e=test_array[4]
    test_array[5]=eval(data["Med.Age"])
    f=test_array[5]
    test_array[6]=eval(data["Urban Pop %"])
    g=test_array[6]
    test_array[7]=eval(data["World Share"])
    h=test_array[7]

    country_index=np.where(columns["columns"]==data["country"])
    test_array[country_index]=1
    print(test_array)

    result=model.predict([test_array])

    cursor=mysql.connection.cursor()
    query = "create table if not exists population(Yearly_change varchar(10),Net_change varchar(10),Density varchar(10),Migrants varchar(10),Fert_Rate varchar(10),Med_Age varchar(10),UrbanPop varchar(10),World_Share varchar(10),country varchar(10),population varchar(50))"
    cursor.execute(query)
    cursor.execute("insert into population(Yearly_change,Net_change,Density,Migrants,Fert_Rate,Med_Age,UrbanPop,World_Share,country,population)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(a,b,c,d,e,f,g,h,data["country"],result))

    mysql.connection.commit()
    cursor.close()

    return render_template("End.html",result=result)



if __name__=="__main__":
    app.run(host="0.0.0.0",port=config.port_number)