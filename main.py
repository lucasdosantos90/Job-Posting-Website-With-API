from flask import Flask, request, render_template, redirect, url_for, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_website.sqlite3.db'
CORS(app)
db = SQLAlchemy(app)


#CLASS Post_Job THAT CREATES TABLE post_job IN DATABASE
class Post_Job(db.Model):
    job_id = db.Column(db.Integer(), primary_key=True)
    job_title = db.Column(db.String())
    job_location = db.Column(db.String())
    job_post_date = db.Column(db.DateTime(), default=datetime.now())
    job_contract_time = db.Column(db.DateTime(), default=datetime.now())
    job_requirements = db.Column(db.String())
    job_other_skills = db.Column(db.String())
    job_about = db.Column(db.String())

    def to_dict(self):
        result = {}

        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


#HOMEPAGE
@app.route('/')
def home():
    job_list = Post_Job.query.all()
    return render_template('index.html',job_list=job_list)


#ROUTE ADD JOBS THAT USES FUNCTION ADD NEW JOBS
@app.route('/add')
def add():
    jobs = Post_Job.query.all()
    return render_template('add_jobs.html',jobs=jobs)


#FUNCTION ADD NEW JOBS
@app.route('/job/add', methods=['POST'])
def add_job():
    try:
        form = request.form
        post = Post_Job(
            job_title=form['job_title'], 
            job_location=form['job_location'], 
            
            # job_post_date=datetime(form['job_post_date']),
            #job_contract_time = request.form.get('job_contract_time'),

            job_requirements=form['job_requirements'],
            job_other_skills=form['job_other_skills'],
            job_about=form['job_about'],
            )
        db.session.add(post)
        db.session.commit()
    except Exception as error:
        print('Error',error)
    return redirect(url_for('home'))


#LISTS ALL JOBS
@app.route('/list')
def list_jobs():
    job_list = Post_Job.query.all()
    return render_template('list_jobs.html',job_list=job_list)


#EDIT JOBS USING ID
@app.route('/job/<id>/edit', methods=['POST','GET'])
def edit_jobs(id):
    if request.method == 'POST':
        try:
            edit = Post_Job.query.get(id)
            form = request.form
            edit.job_title = form['job_title']
            edit.job_location = form['job_location']
            edit.job_requirements = form['job_requirements']
            edit.job_other_skills = form['job_other_skills']
            edit.job_about = form['job_about']
            db.session.commit()
        except Exception as error:
            print('Error',error)
        return redirect(url_for('list_jobs'))
    else:
        try:
            edit = Post_Job.query.get(id)
            return render_template('edit_jobs.html',edit=edit)
        except Exception as error:
            print('Error',error)
    return redirect(url_for('list_jobs'))  


#DELETE JOBS USING ID
@app.route('/job/<id>/del')
def delete_job(id):
    try:
        job = Post_Job.query.get(id)
        db.session.delete(job)
        db.session.commit()
    except Exception as error:
        print('Error',error)
    return redirect(url_for('list_jobs'))


#API JOBS LIST
@app.route('/api/jobs')
def api_list_jobs():
    try:
        api_jobs = Post_Job.query.all()
        return jsonify([jobs.to_dict() for jobs in api_jobs])
    except Exception as error:
        print('Error',error)
    return jsonify([])


#API ADD JOBS
@app.route('/api/add_jobs', methods=['PUT'])
def api_add_jobs():
    try:
        form = request.get_json()
        jobs = Post_Job(
            job_title=form['job_title'], 
            job_location=form['job_location'], 
            
            #job_post_date=datetime(form['job_post_date']),
            #job_contract_time = request.form.get('job_contract_time'),

            job_requirements=form['job_requirements'],
            job_other_skills=form['job_other_skills'],
            job_about=form['job_about'],
            )
        db.session.add(jobs)
        db.session.commit()
        return jsonify({'success':True})
    except Exception as error:
        print('Error',error)
    return jsonify({'success':False})


# #API EDIT
# @app.route('/api/post/<id>', methods=['PUT'])
# def api_edit_post(id):
#     try:
#         post = Post.query.get(id)
#         data = request.get_json()
#         post.title = data['title']
#         post.content = data['content']
#         post.author = data['author']
#         db.session.commit()
#         return jsonify({'success':True})
#     except Exception as error:
#         print('Error',error)

#     return jsonify({'success':False})     
        

# #API DELETE
# @app.route('/api/post/<id>/', methods=['DELETE'])
# def api_delete_post(id):
#     try:
#         post = Post.query.get(id)
#         db.session.delete(post)
#         db.session.commit()
#         return jsonify({'success':True})
#     except Exception as error:
#         print('Error',error)
#     return jsonify({'success':False})


app.run(debug=True)

with app.app_context():
    db.create_all()
    db.session.commit()
