% rebase('skeleton.tpl', title=title)
<form method="POST" action="/auth" class="w3-container" >
    <p>
        <label for='user_name'>User Name</label>
        <input class="w3-input w3-border" type="text" placeholder="Enter Username" name="user_name" required>
    </p>
    <p>
        <label for='password'>Password</label>
        <input class="w3-input w3-border" type="password" placeholder="Enter Password" name="password" required>
    </p>

    <button class="w3-btn w3-teal w3-round" id="login" type="submit">Login</button>
</form>