from flask import request, redirect, render_template, url_for
from flask.ext.login import current_user, login_required
from app import app, db
from uuid import uuid4 as uuid
from .models import User, Group

@app.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('choice'))

	return render_template('index.tmpl.html', signup_link=url_for('auth'))

@app.route('/choice')
@login_required
def choice():
	# TODO: if the user has declared an active group, then redirect to that.
	# if current_user.active_group is not None:
	# ...

	return render_template('choice.tmpl.html',
							create_action=url_for('create_group'),
							join_action=url_for('join_group'))

# @app.route('/choice')
# def choice():
# 	return '''
# 		<form action= "/groups/create">
# 			<input type="text" name="name" placeholder="Create A Group">
# 			<input type="submit" value="submit">
# 		</form>
# 		<form action= "/groups/join">
# 			<input type="text" name="code" placeholder="Join A Group">
# 			<input type="submit" value="submit">
# 		</form>
# 	'''

@app.route('/group/<group_code>/')
@login_required
def group(group_code):
	group = Group.query.filter_by(code=group_code).one()
	groupid = group.id
	return render_template('groups.tmpl.html',
							group=group,
							user=current_user,
							playlist_action=url_for('generate_playlist', groupid=groupid))

@app.route('/group/create')
@login_required
def create_group():
	name = request.args.get('name')
	newCode = uuid().hex[:5]

	newGroup = Group(name=name, code=newCode, host=current_user.id)
	newGroup.members.append(current_user)

	#current_user.active_group = newGroup

	db.session.add(newGroup)
	db.session.commit()

	return redirect(url_for('group', group_code=newCode))

@app.route('/group/join')
@login_required
def join_group():
	code = request.args.get('code')
	group = Group.query.filter_by(code=code).one()

	if current_user not in group.members:
		group.members.append(current_user)
		db.session.commit()

	return redirect(url_for('group', group_code=group.code))