from application import app, db
from flask import render_template, request, redirect, flash, url_for
from application.form import AddToDo
from datetime import datetime
from bson import ObjectId

@app.route("/")
def get_todo():
    todos = []
    for todo in db.todo.find().sort("created_at", -1):
        todo["_id"] = str(todo["_id"])
        todo["created_at"] = todo["created_at"].strftime("%b %d %Y %H:%M;&S")
        todos.append(todo)
    return render_template("view.html", title="Home Page", todos=todos)



@app.route("/add", methods=["POST","GET"])
def add_todo():
    if request.method == "POST":
        form_data = AddToDo(request.form)
        name = form_data.name.data
        description = form_data.description.data
        completed = form_data.completed.data
        
        db.todo.insert_one({
            "name": name,
            "description": description,
            "completed": completed,
            "created_at": datetime.utcnow()
        })
        
        flash("ToDo created successfully", "success")
        return redirect("/")
    else:
        form = AddToDo()
    return render_template("add.html", title="Add Page", form=form)

@app.route("/update/<id>", methods=["POST", "GET"])
def update_todo(id):
    if request.method == "POST":
        form = AddToDo(request.form)
        name = form.name.data
        description = form.description.data
        completed = form.completed.data
        
        db.todo.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": name,
            "description": description,
            "completed": completed,
            "created_at": datetime.utcnow()
        }})
        
        flash("Todo Updated Successfully", "success")
        return redirect("/")
    else:
        form = AddToDo()
        todo = db.todo.find_one_or_404({"_id": ObjectId(id)})
        
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("descriptione", None)
        form.completed.data = todo.get("completed", None)
    
    return render_template("add.html", form=form)

@app.route("/delete/<id>")
def delete_todo(id):
    db.todo.find_one_and_delete({ "_id": ObjectId(id) })
    flash("ToDo Deleted Successfully", "success")
    return redirect("/")