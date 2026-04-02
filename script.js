let BACKEND_URL = "https://ai-study-assistant-3.onrender.com";

let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

// ===== TASKS =====
function showTasks() {
    let list = document.getElementById("taskList");
    list.innerHTML = "";

    let completedCount = 0;

    tasks.forEach((task, index) => {
        let li = document.createElement("li");

        li.className = task.priority.toLowerCase();
        if (task.completed) {
            li.classList.add("completed");
            completedCount++;
        }

        li.innerHTML = `
            <div>
                <input type="checkbox" ${task.completed ? "checked" : ""}
                onchange="toggleComplete(${index})">
                ${task.text} (${task.priority})
                <br>
                <small>📅 ${task.deadline || "No deadline"}</small>
            </div>
            <button onclick="deleteTask(${index})">❌</button>
        `;

        list.appendChild(li);
    });

    updateProgress(completedCount);
}

function addTask() {
    let input = document.getElementById("taskInput");
    let priority = document.getElementById("priority").value;
    let deadline = document.getElementById("deadline").value;

    if (!input.value.trim()) return;

    tasks.push({ text: input.value, priority, deadline, completed: false });

    localStorage.setItem("tasks", JSON.stringify(tasks));
    input.value = "";
    showTasks();
}

function deleteTask(i) {
    tasks.splice(i, 1);
    localStorage.setItem("tasks", JSON.stringify(tasks));
    showTasks();
}

function toggleComplete(i) {
    tasks[i].completed = !tasks[i].completed;
    localStorage.setItem("tasks", JSON.stringify(tasks));
    showTasks();
}

function updateProgress(done) {
    let percent = tasks.length === 0 ? 0 : Math.round((done / tasks.length) * 100);
    document.getElementById("progress").innerText = `Progress: ${percent}%`;
}

// ===== TIMER =====
let time = 1500;
let interval;

function startTimer() {
    if (interval) return;

    interval = setInterval(() => {
        if (time <= 0) {
            clearInterval(interval);
            interval = null;
            addMessage("bot", "⏰ Time's up!");
        }

        time--;

        let m = Math.floor(time / 60);
        let s = time % 60;

        document.getElementById("timer").innerText =
            `${m}:${s < 10 ? "0" : ""}${s}`;
    }, 1000);
}

function pauseTimer() {
    clearInterval(interval);
    interval = null;
}

function resetTimer() {
    clearInterval(interval);
    interval = null;
    time = 1500;
    document.getElementById("timer").innerText = "25:00";
}

// ===== DARK MODE =====
function toggleDarkMode() {
    document.body.classList.toggle("dark");
}

// ===== CHAT =====
function addMessage(type, text) {
    let chatBox = document.getElementById("chatBox");

    let msg = document.createElement("div");
    msg.className = `message ${type}`;
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ===== AI CHAT (FIXED FETCH) =====
async function askAI() {
    let input = document.getElementById("userInput");
    let text = input.value;

    if (!text.trim()) return;

    addMessage("user", text);
    input.value = "";

    let botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerText = "Typing...";
    document.getElementById("chatBox").appendChild(botMsg);

    try {
        let response = await fetch(`${BACKEND_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        let data = await response.json();
        typeEffect(data.reply, botMsg);

    } catch (error) {
        typeEffect("❌ Backend not connected. Check deployment/CORS", botMsg);
    }
}

// ===== QUICK ASK =====
function quickAsk(text) {
    document.getElementById("userInput").value = text;
    askAI();
}

// ===== TYPE EFFECT =====
function typeEffect(text, element) {
    element.innerHTML = "";
    let i = 0;

    let interval = setInterval(() => {
        if (i >= text.length) {
            clearInterval(interval);
            return;
        }

        let char = text[i];

        if (char === "\n") element.innerHTML += "<br>";
        else if (char === " ") element.innerHTML += "&nbsp;";
        else element.innerHTML += char;

        i++;
    }, 10);
}

// INIT
showTasks();

