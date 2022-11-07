from flask import Flask, render_template, request
import sqlite3, time

# Connect to sqlite database
def update_database():
    conn = sqlite3.connect("/home/ubuntu/Class-Vote-System/db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM polls_poll")
    return cur.fetchall()
# conn.close()

def resetVotesComments():
    conn = sqlite3.connect("/home/ubuntu/Class-Vote-System/db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM polls_vote")
    conn.commit()
    cur.execute("DELETE FROM polls_comment")
    conn.commit()
    conn.close()


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Update class list
    list_class = update_database()
    # Construct classes dictionary
    classes = []
    for item in list_class:
        classes.append({k: item[k] for k in item.keys()})

    # If reset bottom is clicked
    if request.method == 'POST':
        if request.form.get('reset'):
            resetVotes()
        else:
            pass
    elif request.method == 'GET':
        return render_template("index.html", 
        template_classes = classes)
    
    return render_template("index.html", 
        template_classes = classes)

@app.route('/<class_name>', methods=['GET', 'POST'])
def subpage(class_name):
    # Update class list
    list_class = update_database()
    #--- Count total vote numbers of the class ---#
    # Get Class ID from sqllite
    classID = 0
    for item in list_class:
        if item[1] == class_name:
            classID = item[0]
    # Get Votes from sqllite
    conn = sqlite3.connect("/home/ubuntu/Class-Vote-System/db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM polls_vote")
    votes_all = cur.fetchall()
    cur.execute("SELECT * FROM polls_choice")
    choices_all = cur.fetchall()
    cur.execute("SELECT * FROM polls_comment")
    comment_all = cur.fetchall()
    # Get votes only that of Class ID
    choice_IDs=[]
    for item in votes_all:
        if item[2] == classID:
            choice_IDs.append(item[1])
    totalVotes = len(choice_IDs)
    meanValue = 0
    choices = [0,0,0,0,0,0,0,0,0,0,0]
    for vote in choice_IDs:
        for choice in choices_all:
            if choice[0] == vote:
                meanValue += int(choice[1])/totalVotes
                choices[int(choice[1])] += 1

    comments = []
    for comment in reversed(comment_all):
        comments.append(comment[1])

    color = (10-meanValue)/10*120 # 0 is red and 130 is blue

    choices_list = []
    choices_list.extend([repr(i) + ' : ' + repr(choices[i]) for i in range(len(choices))])

    # If reset bottom is clicked
    if request.method == 'POST':
        if request.form.get('reset'):
            resetVotesComments()
        else:
            pass
    elif request.method == 'GET':
        return render_template("viewer.html",
        class_name=class_name, total_votes = totalVotes, meanValue = meanValue, color_scale = color, choices = choices_list, comments = comments)

    return render_template("viewer.html",
        class_name=class_name, total_votes = totalVotes, meanValue = meanValue, color_scale = color, choices = choices_list, comments = comments)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)
