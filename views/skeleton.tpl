<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }}</title>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>

</head>

<body>
<header>
    <h1 class="page-title " id="title">
        <a href="/" id="return_link">
            <img align="left"
                 hspace="5"
                 src="/favicon.ico"
                 style="height:1.1em;"
                 alt="The quizzology logo as a link to the home page"
            />
        </a>
        {{title}}
    </h1>
    <p>Hi, <span id="user_name">default text</span>, you <span id="user_role">default role</span></p>
</header>

    <script>

        const desired = document.cookie.split(';').filter(function(x){
            console.log(`value is [${x}]`);
            const [name,value] = x.split('=');
            console.log(`name is [${name}]`)
            return name === 'quizzology-user'}
        ).pop()

        console.log("Desired is ["+desired+"]");
        const [key,value] = desired.split('=');
        console.log(`value is [${value}]`)
        const trimmed = value.replace(/"/g,'')
        console.log(`value is trimmed to [${trimmed}]`)
        const [name,role] = trimmed.split(' ');
        console.log(`name: [${name}], role: [${role}]`)

        document.getElementById('user_name').innerText = name;
        document.getElementById('user_role').innerText = role;
    </script>

{{!base}}

</body>
</html>
