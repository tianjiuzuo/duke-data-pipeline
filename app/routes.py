from flask import render_template, flash, redirect, url_for, request, send_file, current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_user import roles_required
from werkzeug.urls import url_parse
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, CollectionForm, ChangePasswordForm
from werkzeug.security import generate_password_hash
from app.models import User, Update, Request, Role
import sqlite3, csv, os
from flask_mail import Message


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [{
        'author': {
            'username': 'John'
        },
        'body': 'Beautiful day in Portland!'
    }, {
        'author': {
            'username': 'Susan'
        },
        'body': 'The Avengers movie was so cool!'
    }]
    if 'admin' in current_user.all_roles():
        return redirect(url_for('admin_dashboard'))
    return render_template('index.html', title='Home', posts=posts, template='base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Password Updated!')
        return redirect(url_for('index'))
    return render_template('changePassword.html', title='Change Password', form=form, template=admin_template_validation())

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if 'shelter' in current_user.all_roles():
        return redirect(url_for('index'))

    form = RegistrationForm()
    available_roles = [role.name for role in Role.query.all()]
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, organization=form.organization.data)
        role = Role.query.filter_by(name=form.role.data).first()
        user.roles.append(role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form, roles = available_roles, template = "base-admin.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/collectionform', methods=['GET', 'POST'])
@login_required
def collectionform():
    form = CollectionForm()
    if form.validate_on_submit():
        submission = Update(user_id=current_user.get_id(),
                            number_of_victims=form.number_of_victims.data,
                            capacity=form.capacity.data)
        db.session.add(submission)
        db.session.commit()
        # send_mail()

        return render_template('confirmation.html')

        flash('Form Completed!')
    return render_template('collectionform.html',
                           title='Collection Form',
                           user=current_user,
                           form=form)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if 'admin' in current_user.all_roles():
        raw_data = db.session.query(Update, User).order_by(Update.timestamp).join(User).all()
        update_fields = ['id', 'user_id', 'number_of_victims', 'capacity', 'timestamp']
        user_fields = ['organization']

        if request.method == 'GET':
            data = []

            for row in raw_data:
                update = row[0]
                user = row[1]
                new_row = []

                for field in update_fields:
                    new_row.append(getattr(update, field))

                for field in user_fields:
                    new_row.append(getattr(user, field))

                data.append(new_row)

            return render_template('admin_dashboard.html',
                                title='Admin Dashboard',
                                fields=update_fields+user_fields,
                                data=data)

        if request.method == 'POST':
            form = request.form.to_dict(flat=False)

            data = []
            csvpath = os.getcwd()
            csvpath = csvpath.split('app')[0]
            csvpath = csvpath + '/app/'
            csvheader = []

            for row in raw_data:
                update = row[0]
                user = row[1]
                new_row = []

                for field in update_fields:
                    if field in form:
                        new_row.append(getattr(update, field))
                        if field not in csvheader:
                            csvheader.append(field)

                for field in user_fields:
                    if field in form:
                        new_row.append(getattr(user, field))
                        if field not in csvheader:
                            csvheader.append(field)

                data.append(new_row)

            with open(csvpath+'data.csv', 'w') as demo_file:
                write = csv.writer(demo_file)
                write.writerow(csvheader)
                write.writerows(data)

            path = 'data.csv'

            return send_file(path, as_attachment=True)

    else:
        return render_template('404.html')

@app.route('/admin_profiles', methods=['GET', 'POST'])
@login_required
def admin_profiles():
    if 'admin' in current_user.all_roles():
        if request.method == 'GET':
            users = User.query.all()
            user_fields = ['id', 'username', 'email', 'organization']
            update_fields = ['id', 'user_id', 'number_of_victims', 'capacity', 'timestamp']
            
            return render_template('profile_page.html', user_fields=user_fields, users=users)

    else:
        return render_template('404.html')

@app.route('/admin_profiles/delete/<int:id>')
@login_required
def delete_profile(id):
    if 'admin' in current_user.all_roles():
        user_to_delete = User.query.get(id)  
        db.session.delete(user_to_delete)
        db.session.commit()
        
        return redirect(url_for('admin_profiles'))
    
    else:
        return render_template('404.html')


@app.route('/research')
@login_required
def research():
    return render_template('research.html', title='Research', template=admin_template_validation())


@app.route('/disclosure')
@login_required
def disclosure():
    return render_template('disclosure.html', title='Disclosure', template=admin_template_validation())


@app.route('/team')
@login_required
def team():
    return render_template('team.html', title='Team', template=admin_template_validation())


@app.route('/contact_us')
@login_required
def contact_us():
    return render_template('contact_us.html', title='Contact Us', template=admin_template_validation())


@app.route('/terms_and_privacy')
@login_required
def terms_and_privacy():
    return render_template('terms_and_privacy.html',
                           title='Please read to continue', template=admin_template_validation())

def admin_template_validation():
    if 'admin' in current_user.all_roles():
        return 'base-admin.html'
    return 'base.html'

def send_mail():
    msg = Message("Submisson Confirmation",
                #   sender = os.environ.get('EMAIL'),
                #   recipients=[os.environ.get('EMAIL')]
                  sender = 'demo@gmail.com',
                  recipients = ['qixuankhoo@gmail.com'])

    msg.body = "Thank you for your submission. The next collection date is _______."
    mail.send(msg)