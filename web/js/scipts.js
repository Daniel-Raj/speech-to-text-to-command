var f = document.querySelector('form');
function connect() {
    n = document.querySelector("#u-name").value;
    p = document.querySelector("#p-word").value;
    
    if (n == '' || p == '') 
        alert("Fields left Empty!!!");
    else {
        eel.start();
    }
}

eel.expose(transform);
function transform() {
    f.style.height = "250px";
    f.innerHTML = `

    <div class="but-ton">
        <div> 
        Use the following PHRASES for the values while speaking.<br />
        <table>
            <thead>
                <th>Phrases</th>
                <th>values</th>
            </head>
            <tbody>
                <tr>
                    <td>Asterisk</td>
                    <td>*</td>
                </tr>
                <tr>
                    <td>Open Bracket</td>
                    <td>(</td>
                </tr>
                <tr>
                    <td>Close Bracket</td>
                    <td>)</td>
                </tr>
                <tr>
                    <td>Character</td>
                    <td>Varchar2</td>
                </tr>
            </tbody>
        </table>
        </div>
        <input type="button" id="lis-button" value="Listen" onclick="listen()">
        <input type="button" id="close-button" value="Close" onclick="closeit()">
    </div>

    `;
}

function listen() {
    f.style.height = "80px";
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