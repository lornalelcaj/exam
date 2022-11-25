from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.thought import  Thought

@app.route('/createThought', methods=['POST'])
def createThought():

    if not Thought.validate_thought(request.form):
        return redirect(request.referrer)
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Thought.create_thought(data)
    return redirect('/')

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.removeLike(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def destroyThought(id):
    data = {
        'thought_id': id,
    }
    thought = Thought.get_thought_by_id(data)
    if session['user_id']==thought['user_id']:
        Thought.deleteAllLikes(data)
        Thought.destroyThought(data)
        return redirect(request.referrer)
    return redirect(request.referrer)