"""Small task tracker used as the system under test (SUT)."""
from flask import Flask, jsonify, request, render_template_string

PAGE = """<!doctype html><html><head><title>Task Tracker</title></head><body>
<h1>Task Tracker</h1>
<form id="form"><input id="title" placeholder="New task" aria-label="Task title">
<button id="add" type="submit">Add</button></form>
<p id="error" role="alert" style="color:red"></p>
<ul id="list"></ul>
<script>
async function load(){const r=await fetch('/api/tasks');const t=await r.json();
 const l=document.getElementById('list');l.innerHTML='';
 t.forEach(x=>{const li=document.createElement('li');li.dataset.id=x.id;
  li.innerHTML=`<span class="title" style="text-decoration:${x.done?'line-through':'none'}">${x.title.replace(/</g,'&lt;')}</span>
  <button class="done">Done</button> <button class="del">Delete</button>`;
  li.querySelector('.done').onclick=async()=>{await fetch('/api/tasks/'+x.id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({done:!x.done})});load()};
  li.querySelector('.del').onclick=async()=>{await fetch('/api/tasks/'+x.id,{method:'DELETE'});load()};
  l.appendChild(li)})}
document.getElementById('form').onsubmit=async e=>{e.preventDefault();
 const title=document.getElementById('title').value;
 const r=await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title})});
 document.getElementById('error').textContent=r.ok?'':(await r.json()).error;
 if(r.ok)document.getElementById('title').value='';load()};
load();
</script></body></html>"""

def create_app():
    app = Flask(__name__)
    store = {"tasks": {}, "next": 1}

    @app.get("/")
    def index():
        return render_template_string(PAGE)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/tasks")
    def list_tasks():
        return jsonify(list(store["tasks"].values()))

    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify(error="title is required"), 400
        if len(title) > 100:
            return jsonify(error="title too long"), 400
        t = {"id": store["next"], "title": title, "done": False}
        store["tasks"][t["id"]] = t
        store["next"] += 1
        return jsonify(t), 201

    @app.get("/api/tasks/<int:tid>")
    def get_task(tid):
        t = store["tasks"].get(tid)
        return (jsonify(t), 200) if t else (jsonify(error="not found"), 404)

    @app.put("/api/tasks/<int:tid>")
    def update_task(tid):
        t = store["tasks"].get(tid)
        if not t:
            return jsonify(error="not found"), 404
        data = request.get_json(silent=True) or {}
        if "title" in data:
            if not str(data["title"]).strip():
                return jsonify(error="title is required"), 400
            t["title"] = data["title"].strip()
        if "done" in data:
            t["done"] = bool(data["done"])
        return jsonify(t)

    @app.delete("/api/tasks/<int:tid>")
    def delete_task(tid):
        if store["tasks"].pop(tid, None) is None:
            return jsonify(error="not found"), 404
        return "", 204

    return app

if __name__ == "__main__":
    create_app().run(port=5000)
