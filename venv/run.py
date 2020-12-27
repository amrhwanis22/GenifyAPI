from flask_restful import Api,Resource,reqparse,abort
from flask import request
from flask import Flask
import pickle
import xgboost as xgb
import numpy as np


# data_path = "input/"
# train_file =  open(data_path + "train_ver2.csv")
# x_vars_list, y_vars_list, cust_dict = processData(train_file, {})


# print(x_vars_list)
app =Flask(__name__)
api = Api(app)
#
# print(getRent({'renta':'10000'}))
# # exit(0)
# print(final_preds)
class Recommender(Resource):
    def __init__(self):
        self.target_cols = ['ind_ahor_fin_ult1', 'ind_aval_fin_ult1', 'ind_cco_fin_ult1', 'ind_cder_fin_ult1',
                       'ind_cno_fin_ult1', 'ind_ctju_fin_ult1', 'ind_ctma_fin_ult1', 'ind_ctop_fin_ult1',
                       'ind_ctpp_fin_ult1', 'ind_deco_fin_ult1', 'ind_deme_fin_ult1', 'ind_dela_fin_ult1',
                       'ind_ecue_fin_ult1', 'ind_fond_fin_ult1', 'ind_hip_fin_ult1', 'ind_plan_fin_ult1',
                       'ind_pres_fin_ult1', 'ind_reca_fin_ult1', 'ind_tjcr_fin_ult1', 'ind_valo_fin_ult1',
                       'ind_viv_fin_ult1', 'ind_nomina_ult1', 'ind_nom_pens_ult1', 'ind_recibo_ult1']
        # self.target_cols = target_cols[2:]
        # self.train_file = open("input/train_ver2.csv")
        # self.x_vars_list, self.y_vars_list, self.cust_dict = processData(self.train_file, {})

    def getAge(self,age):
        mean_age = 40.
        min_age = 20.
        max_age = 90.
        range_age = max_age - min_age
        age = age
        if age == 'NA' or age == '':
            age = mean_age
        else:
            age = float(age)
            if age < min_age:
                age = min_age
            elif age > max_age:
                age = max_age
        return round((age - min_age) / range_age, 4)

    def getCustSeniority(self,custSen):
        min_value = 0.
        max_value = 256.
        range_value = max_value - min_value
        missing_value = 0.
        cust_seniority = custSen
        if cust_seniority == 'NA' or cust_seniority == '':
            cust_seniority = missing_value
        else:
            cust_seniority = float(cust_seniority)
            if cust_seniority < min_value:
                cust_seniority = min_value
            elif cust_seniority > max_value:
                cust_seniority = max_value
        return round((cust_seniority - min_value) / range_value, 4)

    def getIncome(self,income):
        min_value = 0.
        max_value = 1500000.
        range_value = max_value - min_value
        missing_value = 101850.
        Income = income
        if Income == 'NA' or Income == '':
            Income = missing_value
        else:
            Income = float(Income)
            if Income < min_value:
                Income = min_value
            elif Income > max_value:
                Income = max_value
        return round((Income - min_value) / range_value, 6)

    def post(self):
        #Creating feature list which will contain only values passed as the example fromgenify demo
        #Adding dummy values to the other data ranged between 0 and 2 as described from model
        #Adding finally data range between 0 and 1 as this columns are based on products the user added
        data = request.json
        featureList = []
        income = self.getIncome(data['income'])
        age = self.getAge(data['Age'])
        seniority = self.getCustSeniority(data['seniority'])
        for i in range(9):
            featureList.extend([np.random.randint(0,2)])
        for i in data:
            if i == 'seniority':
                featureList.extend([seniority])
            elif i == 'Age':
                featureList.extend([age])
            elif i == 'income':
                featureList.extend([income])
            else:
                featureList.extend([int(data[i])])
        for i in range(22):
            featureList.extend([np.random.randint(0,1)])
        model = pickle.load(open('model.pickle.dat', 'rb'))
        testXgb = xgb.DMatrix(np.asarray([featureList]))

        preds = model.predict(testXgb)
        self.target_cols = np.array(self.target_cols)
        preds = np.argsort(preds, axis=1)
        preds = np.fliplr(preds)[:, :7]
        final_preds = [list(self.target_cols[pred]) for pred in preds]
        return {'Predictions ' : final_preds}

    def get(self):
        return {'result':'hello world'}

api.add_resource(Recommender,'/recodemo/')
if __name__ == '__main__':
    app.run(debug=True,port=5000,use_reloader=True,host='0.0.0.0')