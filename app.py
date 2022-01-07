from flask import Flask,render_template,request,jsonify 
import os
import yaml
import joblib
import numpy as np

from prediction_service import prediction

params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root,"static")
templates_dir = os.path.join(webapp_root,"templates")


app = Flask(__name__,static_folder=static_dir,template_folder=templates_dir)


def read_params(config_path):
    with open(config_path) as yaml_file:   #params will be loaded as yaml's
        config = yaml.safe_load(yaml_file)  #parmas and their datatype

    return config   


def predict(data):  #used for prediction
    config = read_params (params_path)  
    model_dir_path =config['webapp_model_dir']
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)

    return prediction[0]   

def api_response(request):
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response":response}
        return response
    except Exception as e:
        print(e)    

    
@app.route("/",methods = ['GET','POST'])
def index():

    if request.method =="POST":
        try:
            if request.form:

                data = dict(request.form).values()
                data = [list(map(float,data))]
                response = predict(data)
                return render_template("index.html",response= response)

            elif request.json:    
                response =  api_response(request)

                return jsonify(response)  

        except Exception as e:
            return e


    else : 
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
