<!DOCTYPE html>
<html>
<head>
    <h1>Python File Transfer </h1>
    <p><strong>CPSC 470</strong></p>
</head>
<body>
    

  <h2>Project Members:</h2>
<ol>
<ul>Name: Christopher Mireles, Email: Napalashe@csu.fullerton.edu</ul>
<ul>Name: Justin Gerard Perez, Email: justingp45@csu.fullerton.edu </ul>
<ul>Name: Aidan Jahn, Email: nobody34@csu.fullerton.edu </ul>
<ul>Name: [INSERT YOUR NAME], Email: [INSERT EMAIL] </ul>
<ul>Name: [INSERT YOUR NAME], Email: [INSERT EMAIL] </ul>
        
</ol>

  <h2>Programming Language:</h2>
    <p>Python</p>
    
  <h2>Requirements to run</h2>
      <p>
                  Python3
      </p>

  <h2>How to Execute the Program:</h2>
  <h3>Server.py Execution:</h3>
  <ol>
        <li>Navigate to the directory containing <code>server.py</code>.</li>
        <li>Open a terminal in this directory.</li>
        <li>Run the command <code>python3 server.py {insert port number}</code>.</li>
        <li>The server will start and wait for connections on port {port_number}.</li>
    </ol>
    <p>If you do not put a port number it will default to 1200 but it is reccomended to pick your own port.</p>

  <h3>Client Execution:</h3>
  <ol>
        <li>Ensure the server is running as described above.</li>
        <li>Navigate to the directory containing <code>client.py</code>.</li>
        <li>Open a separate terminal in this directory.</li>
        <li>Run the command <code>python3 client.py {insert port number}</code>.</li>
        <li>Use the following commands in the client application:
            <ul>
                <li><code>GET &lt;filename&gt;</code>: To download a file from the server.</li>
                <li><code>PUT &lt;filename&gt;</code>: To upload a file to the server.</li>
                <li><code>LS</code>: To list the files in the server's directory.</li>
                <li><code>QUIT</code>: To disconnect from the server.</li>
            </ul>
        </li>
  </ol>

  <h2>Notes:</h2>
   <p>
        Ensure that both <code>client.py</code> and <code>server.py</code> are in directories that the executing user has read and write permissions for, as file operations are performed in these directories.
        The server and client are set to connect over localhost (<code>127.0.0.1</code>), which means they should run on the same machine for testing purposes. In the file we have submitted there are two files that you can send back and forth.
        The send_me.txt can be used to practice but you can put your own file if you wish.
    

</body>
</html>
