% rebase('skeleton.tpl', title=title)

<form id="quiz_edit" action="/edit" method="POST">
    <label for="quiz_name">Name</label>
    <input type="text" id="quiz_name" name="name" value="{{quiz.name}}">

    <label for="quiz_title">Title</label>
    <input type="text" id="quiz_title"  name="title" value="{{quiz.title}}">

    <button id="save_changes">Save</button>
</form>