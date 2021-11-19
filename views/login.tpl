% rebase('skeleton.tpl', title=title)
<form action="/auth" class="w3-container" method="POST">

    <section class="w3-card w3-container">
        <label for='user_name'>User Name</label>
        <input type="text" name="user_name" required>
        <label for='password'>Password</label>
        <input type="password" name="password" required>
    </section>
    <br/>
    <button class="w3-btn w3-teal w3-round" id="login" type="submit">Login</button>
</form>