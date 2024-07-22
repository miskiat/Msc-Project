from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.forms import LoginForm, UploadForm, SearchForm
from app.models import User, SensorData
import csv
import os
from datetime import datetime

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/dashboard")
@login_required
def dashboard():
    num_locations, num_users, num_records = SensorData.get_statistics()
    return render_template('dashboard.html', username=current_user.username,
                           num_locations=num_locations, num_users=num_users, num_records=num_records)

@main.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        location = form.location.data
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('data', filename)
            file.save(filepath)
            save_csv_to_datafiles(filepath, location)
            flash('File successfully uploaded and processed', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('upload.html', form=form)

@main.route("/view-data", methods=['GET', 'POST'])
@login_required
def view_data():
    form = SearchForm()
    location = form.location.data if form.location.data != 'all' else None
    search_query = form.search.data
    sensor_data = SensorData.load_sensordata(location)
    
    if search_query:
        sensor_data = [data for data in sensor_data if search_query.lower() in str(data).lower()]
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(sensor_data)
    paginated_data = sensor_data[(page - 1) * per_page: page * per_page]
    
    # Chart Data Preparation
    chart_data = prepare_chart_data(sensor_data)

    return render_template('view_data.html', sensor_data=paginated_data, form=form,
                           total=total, page=page, per_page=per_page, chart_data=chart_data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

def save_csv_to_datafiles(filepath, location):
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            save_sensordata(row, location)

def save_sensordata(row, location):
    with open(DATAFILE_CSV, mode='a', newline='') as datafile:
        fieldnames = ['id', 'location', 'timestamp', 'user_id']
        writer = csv.DictWriter(datafile, fieldnames=fieldnames)
        writer.writerow({
            'id': generate_id(),
            'location': location,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': current_user.id
        })
    with open(SENSORDATA_CSV, mode='a', newline='') as sensordata:
        fieldnames = ['id', 'time', 'temp', 'ir', 'vis', 'lux', 'accel_x', 'accel_y', 'accel_z', 'tilt', 'mag_x', 'mag_y', 'mag_z', 'h_angle', 'direction', 'vbat', 'data_file_id']
        writer = csv.DictWriter(sensordata, fieldnames=fieldnames)
        writer.writerow({
            'id': generate_id(),
            'time': row['Time'],
            'temp': row['Temp'],
            'ir': row['IR'],
            'vis': row['Vis'],
            'lux': row['Lux'],
            'accel_x': row['Accel_X'],
            'accel_y': row['Accel_Y'],
            'accel_z': row['Accel_Z'],
            'tilt': row['Tilt'],
            'mag_x': row['Mag_X'],
            'mag_y': row['Mag_Y'],
            'mag_z': row['Mag_Z'],
            'h_angle': row['H.Angle'],
            'direction': row['Direction'],
            'vbat': row['VBAT'],
            'data_file_id': generate_id()
        })

def generate_id():
    return str(int(datetime.now().timestamp()))

def prepare_chart_data(sensor_data):
    import json
    chart_data = {'labels': [], 'datasets': []}
    if sensor_data:
        labels = set(data['time'] for data in sensor_data)
        chart_data['labels'] = sorted(labels)
        temp_data = [data['temp'] for data in sensor_data]
        chart_data['datasets'].append({
            'label': 'Temperature',
            'data': temp_data,
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)'
        })
    return json.dumps(chart_data)
