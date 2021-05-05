var f = document.querySelector('form');
function connect() {
    n = document.querySelector("#u-name").value;
    p = document.querySelector("#p-word").value;
    
    if (n == '' || p == '') 
        alert("Fields left Empty!!!");
    else {
        transform();
    }
}

function transform() {
    f.style.height = "80px";
    f.innerHTML = `

    <div class="but-ton">
        <input type="button" id="lis-button" value="Listen" onclick="listen()">
        <input type="button" id="close-button" value="Close" onclick="closeit()">
    </div>

    `;
}

function listen() {
    f.innerHTML = `

    <h1>Listening...<input type='button' id="back-button" value="Stop" onclick="transform()"></h1>

    `; 
}

function closeit() {
    f.style.height = "300px";   
    f.innerHTML = `

    <h1> Database <br /> User Login</h1>
    <div class="user-name" >
        <input id="u-name" type="text" name="username" placeholder="Enter User name here">
        <input id="p-word" type="password" name="password" placeholder="Enter User Password here">
    </div>
    <div class="but-ton">
        <input type="button" value="Connect" onclick="connect()">
    </div>
    
    `;
}