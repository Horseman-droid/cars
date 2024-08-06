from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Dummy data
users = []
discussions = []
user_id_counter = 1
discussion_id_counter = 1

# Routes for User Management
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    global user_id_counter
    if request.method == 'POST':
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        if any(user['mobile_no'] == mobile_no or user['email'] == email for user in users):
            return "User with this mobile number or email already exists."
        user = {
            'id': user_id_counter,
            'name': name,
            'mobile_no': mobile_no,
            'email': email
        }
        users.append(user)
        user_id_counter += 1
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if user is None:
        return "User not found.", 404
    if request.method == 'POST':
        user['name'] = request.form['name']
        user['mobile_no'] = request.form['mobile_no']
        user['email'] = request.form['email']
        return redirect(url_for('list_users'))
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    global users
    users = [user for user in users if user['id'] != id]
    return redirect(url_for('list_users'))

@app.route('/list_users')
def list_users():
    return render_template('list_users.html', users=users)

@app.route('/search_user', methods=['GET'])
def search_user():
    name = request.args.get('name')
    filtered_users = [user for user in users if name.lower() in user['name'].lower()]
    return render_template('list_users.html', users=filtered_users)

# Routes for Discussion Management
@app.route('/post_discussion', methods=['POST'])
def post_discussion():
    global discussion_id_counter
    text = request.form['text']
    hashtags = request.form['hashtags']
    image = request.files.get('image')

    image_path = None
    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

    discussion = {
        'id': discussion_id_counter,
        'text': text,
        'hashtags': hashtags,
        'image': image_path
    }
    discussions.append(discussion)
    discussion_id_counter += 1
    return redirect(url_for('index'))

@app.route('/update_discussion/<int:id>', methods=['GET', 'POST'])
def update_discussion(id):
    discussion = next((d for d in discussions if d['id'] == id), None)
    if discussion is None:
        return "Discussion not found.", 404
    if request.method == 'POST':
        discussion['text'] = request.form['text']
        discussion['hashtags'] = request.form['hashtags']
        image = request.files.get('image')

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            discussion['image'] = image_path

        return redirect(url_for('index'))
    return render_template('update_discussion.html', discussion=discussion)

@app.route('/delete_discussion/<int:id>')
def delete_discussion(id):
    global discussions
    discussions = [d for d in discussions if d['id'] != id]
    return redirect(url_for('index'))

@app.route('/list_discussions_by_tag', methods=['GET'])
def list_discussions_by_tag():
    tag = request.args.get('tag')
    filtered_discussions = [d for d in discussions if tag.lower() in d['hashtags'].lower()]
    return render_template('list_discussions.html', discussions=filtered_discussions)

@app.route('/list_discussions_by_text', methods=['GET'])
def list_discussions_by_text():
    text = request.args.get('text')
    filtered_discussions = [d for d in discussions if text.lower() in d['text'].lower()]
    return render_template('list_discussions.html', discussions=filtered_discussions)

@app.route('/')
def index():
    return render_template('index.html', discussions=discussions)

if __name__ == '__main__':
    app.run(debug=True)
