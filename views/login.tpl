% rebase('skeleton.tpl', title=title)
<!--suppress HtmlUnknownTarget -->
<form method="POST" action="/auth" class="w3-container" >
    <p>
        <label for='user_name'>User Name</label>
        <input class="w3-input w3-border" type="text" placeholder="Enter Username" id="user_name" name="user_name" required>
    </p>
    <p>
        <label for='password'>Password</label>
        <input class="w3-input w3-border" type="password" placeholder="Enter Password" id="password" name="password" required>
    </p>
    % if flash:
        <section id="flash" class="w3-panel w3-red"> {{ flash }}</section>
    % end
    <input type="hidden" name="destination" value="{{ destination }}">
    <button class="w3-btn w3-teal w3-round" id="login" type="submit">Login</button>
</form>