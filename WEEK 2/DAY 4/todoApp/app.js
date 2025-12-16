// ---------- Utility: Save Errors to LocalStorage logs ----------
function logError(errorMsg) {
    try {
        const prev = localStorage.getItem("errorLogs") || "";
        const updated = prev + `\n[${new Date().toLocaleString()}] ${errorMsg}`;
        localStorage.setItem("errorLogs", updated);

        console.error("Logged Error:", errorMsg);
    } catch (err) {
        console.error("Critical: Unable to write logs", err);
    }
}

// ---------- Load Existing Todos ----------
function loadTodos() {
    try {
        return JSON.parse(localStorage.getItem("todos")) || [];
    } catch (err) {
        logError("Failed to load todos: " + err);
        return [];
    }
}

// ---------- Save Todos ----------
function saveTodos(todos) {
    try {
        localStorage.setItem("todos", JSON.stringify(todos));
    } catch (err) {
        logError("Failed to save todos: " + err);
    }
}

let todos = loadTodos();   // load on refresh

const input = document.getElementById("todoInput");
const addBtn = document.getElementById("addBtn");
const list = document.getElementById("todoList");

// ---------- Render All Todos ----------
function render() {
    list.innerHTML = "";

    todos.forEach((todo, index) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${todo}</span>
            <div>
                <button onclick="editTodo(${index})">Edit</button>
                <button onclick="deleteTodo(${index})">Delete</button>
            </div>
        `;
        list.appendChild(li);
    });
}

render();

// ---------- Add Todo ----------
addBtn.addEventListener("click", () => {
    try {
        const text = input.value.trim();
        if (!text) return alert("Enter something");

        todos.push(text);
        saveTodos(todos);
        render();

        input.value = "";
    } catch (err) {
        logError("Add Todo Failed: " + err);
    }
});

// ---------- Edit Todo ----------
function editTodo(i) {
    try {
        const newText = prompt("Edit todo:", todos[i]);
        if (!newText) return;
        todos[i] = newText.trim();
        saveTodos(todos);
        render();
    } catch (err) {
        logError("Edit Todo Failed: " + err);
    }
}

// ---------- Delete Todo ----------
function deleteTodo(i) {
    try {
        todos.splice(i, 1);
        saveTodos(todos);
        render();
    } catch (err) {
        logError("Delete Todo Failed: " + err);
    }
}
