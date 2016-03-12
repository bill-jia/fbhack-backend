from flask import request, redirect
from flask.ext.login import current_user
from app import app, db
import uuid
from .models import User, Group

@app.route('/choice')
def choice():
	return '''
		<form action= "/groups/create">
			<input type="text" name="name" placeholder="Create A Group">
			<input type="submit" value="submit">
		</form>
		<form action= "/groups/join">
			<input type="text" name="code" placeholder="Join A Group">
			<input type="submit" value="submit">
		</form>
	'''

@app.route('/groups/create')
def create_group():
	print(current_user)
	name = request.args.get('name')
	newCode = uuid.uuid4().hex
	newGroup = Group(name=name, code=newCode, host=current_user.id)
	db.session.add(newGroup)
	db.session.commit()
	return redirect(url_for('choice'))

@app.route('/groups/join')
def join_group():
	code = request.args.get('code')
	group = Group.query.filter_by(code=code).one()
	if current_user not in group.members:
		group.members.append(current_user)
		db.session.commit()
	return redirect(url_for('choice'))		