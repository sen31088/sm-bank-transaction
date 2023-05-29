from flask import request, render_template, Blueprint, session, send_file
from datetime import datetime
from models.model_transactions import Usertranscation, Userdata
from dateutil.relativedelta import relativedelta
import os, glob
import csv
import openpyxl


transactions_ctrl = Blueprint("transactions", __name__, static_folder='static', template_folder='templates')

usertranscation = Usertranscation()

act_page = 'transcation'

def recent_transcations(input_data, source):
        user_session = input_data
        col_transactions_currentuser= user_session + 'transactions'
        user_data_found = usertranscation.find_and_sort_documents(col_transactions_currentuser, user_session)
        user_data_found_list = list(user_data_found)
        if not user_data_found_list:
            msg = 'No Transcation found for ' +  input_data
            if source == 'admin':
                print("Admin active_page is: ", act_page)
                return render_template('admin-recent-transactions.html', active_page = act_page, message = msg, logedin_user = user_session)
            else:
                print("active_page is: ", act_page)
                return render_template('recent-transactions.html', active_page = act_page,  messages1 = msg, logedin_user = user_session)
        else:
            trans_list1 = []
            msg = 'Recent Transcations of ' + user_session
            #print("Transcation found")
            for i in user_data_found_list:
                del i['_id']
                for j in i.values():
                    trans_list1.append(j)
            ##print(trans_list1)
            trans_list = [trans_list1[x:x+9] for x in range(0, len(trans_list1), 9)]
            if source == 'admin':
                return render_template('admin-recent-transactions.html', active_page = act_page, data = trans_list, messages = msg, logedin_user = user_session)
            else:
                return render_template('recent-transactions.html', active_page = act_page, data = trans_list, messages = msg, logedin_user = user_session)

   
           
def detailed_transcation(input_data, source):
        
        user_session = input_data
        user_required_input = request.form.get('months')
        #print("user_required_input: ", user_required_input)
        current_user_found = Userdata.get_data_one({'userid': input_data})
        current_user_name = current_user_found["Name"]
        current_user_accno = current_user_found["Accno"]
        current_user_accbal = current_user_found["Accbal"]
        col_transactions_currentuser= input_data + 'transactions'
        today = datetime.today()
        current_month = str(today.strftime('%m'))
        end_required_month = int(current_month) - int(user_required_input)
        end_month = today - relativedelta(month=end_required_month)
        search_year = int(datetime.strftime(end_month, '%Y'))
        search_month = int(datetime.strftime(end_month, '%m'))
        search_date = int(datetime.strftime(end_month, '%d'))
        from_date = datetime.strftime(end_month, '%d-%b-%Y')
        current_date = datetime.today().strftime('%d-%b-%Y')

        myquery = usertranscation.find_user_transcations(col_transactions_currentuser, datetime, search_year, search_month, search_date )
        
        if not myquery:
            msg = 'No Transcation found for ' +  input_data
            if source == 'admin':
              return render_template('admin-detailed-transactions.html', active_page = act_page, message = msg, logedin_user = user_session)
            else:
              return render_template('detailed-transactions.html',active_page = act_page,  messages = msg, logedin_user = user_session)
        
        if not os.path.exists("statements"):
            os.makedirs("statements")
        
        if source == 'admin':
            file = "statements/" + "admin_" + user_session + '*.csv'
            file_csv_name = "statements/" + "admin_" + input_data + '_' + current_date + '.xlsx'
        else:
            file = "statements/" + user_session + '*.csv'
            file_csv_name = "statements/" + input_data + '_' + current_date + '.xlsx'

        fileList = glob.glob(file, recursive=True)
        for file in fileList:
            os.remove(file)
        
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        
        #file = open(file_csv_name, 'w')
        #output = csv.writer(file) # writng in this file

        Name = ['Name', current_user_name]
        Acc_number = ['Acc No', current_user_accno]
        Acc_bal = ['Acc Balance', current_user_accbal]
        frm_date =['From Date', from_date]
        to_date = ['To Date', current_date]
        heading = ["Transcation ID", "From Acc no",	"To Acc no", "Amount", "Remarks", "Type", "Date", "Time", "Account Balance"]

        worksheet.append(Name)
        worksheet.append(Acc_number)
        worksheet.append(Acc_bal)
        worksheet.append(frm_date)
        worksheet.append(to_date)
        worksheet.append(heading)
        trans_list = []
        for i in myquery:
            del i['_id']
            for j in i.values():
                trans_list.append(j)
        trans_list1 = [trans_list[x:x+9] for x in range(0, len(trans_list), 9)]
        for row in trans_list1:
            #output.writerow(row) 
            worksheet.append([str(cell) for cell in row])
        #file.close()
        workbook.save(file_csv_name)
        return send_file(file_csv_name, mimetype='text/csv', as_attachment=True)



@transactions_ctrl.route("/recent-transactions",methods=["POST", "GET"])
def recent_trans(): 
    user_session = session.get('name')
    user_session_otp = session.get('otp_valid')
    if not user_session or not user_session_otp:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('index.html')
    else:
        user_session = session.get('name')
        source = 'user'
        return recent_transcations(user_session, source)

@transactions_ctrl.route("/detailed-transactions",methods=["POST", "GET"])
def details_trans(): 
    user_session = session.get('name')
    user_session_otp = session.get('otp_valid')
    if not user_session or not user_session_otp:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('index.html')
    else:
        return render_template('detailed-transactions.html', active_page = act_page, logedin_user = user_session)


@transactions_ctrl.route("/api/v1/detailed-transactions",methods=["POST", "GET"])
def api_detailed_trans(): 
    user_session = session.get('name')
    user_session_otp = session.get('otp_valid')
    if not user_session or not user_session_otp:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('index.html')
    else:
        source = 'user'
        return detailed_transcation(user_session, source)
     

@transactions_ctrl.route("/admin-recent-transactions",methods=["POST", "GET"])
def admin_recent_trans(): 
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin-index.html')
    else:
        #user_session = session.get('username')
        return render_template('admin-recent-transactions.html', active_page = act_page, logedin_user = user_session)

@transactions_ctrl.route("/api/v1/admin-recent-transactions",methods=["POST", "GET"])
def api_admin_recent_trans(): 
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin-index.html')
    else:
        #user_session = session.get('username')
        if request.method=='POST':

            if 'radioaccno' in request.form:
                accnumber_in = request.form['accno']
                query = {"Accno": accnumber_in}
                userdata_found = Userdata.get_acc_data(query)
                input_data1 = userdata_found[0]
                input_data = input_data1['userid']
                msg = 'Account Number not found'
    
            if 'radiouserid' in request.form:
                userid_in = request.form['userid']
                userdata_found = Userdata.get_acc_data({"userid": userid_in})
                input_data = userid_in
                msg = 'User ID not found'
            if not userdata_found:
                return render_template('admin-recent-transactions.html', active_page = act_page, message = msg, logedin_user = user_session)
            else:
                source = 'admin'
                return recent_transcations(input_data, source)
               

@transactions_ctrl.route("/admin-detailed-transactions",methods=["POST", "GET"])
def admin_detailed_trans(): 
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        #user_session = session.get('username')
        return render_template('admin-detailed-transactions.html', active_page = act_page, logedin_user = user_session)

@transactions_ctrl.route("/api/v1/admin-detailed-transactions",methods=["POST", "GET"])
def api_admin_detailed_trans(): 
    user_session = session.get('username')
    if not user_session:
        #print("In Transfer functuon username is: ", user_found)
        return render_template('admin.index.html')
    else:
        #user_session = session.get('username')
        if request.method=='POST':

            if 'radioaccno' in request.form:
                accnumber_in = request.form['accno']
                query = {"Accno": accnumber_in}
                userdata_found = Userdata.get_acc_data(query)
                input_data1 = userdata_found[0]
                input_data = input_data1['userid']
                msg = 'Account Number not found'
    
            if 'radiouserid' in request.form:
                userid_in = request.form['userid']
                userdata_found = Userdata.get_acc_data({"userid": userid_in})
                input_data = userid_in
                msg = 'User ID not found'
            if not userdata_found:
                return render_template('admin-detailed-transactions.html', active_page = act_page, message = msg, logedin_user = user_session)
            else:
                source = 'admin'
                return detailed_transcation(input_data,source)
               

    
