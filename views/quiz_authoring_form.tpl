% rebase('skeleton.tpl', title=title)

<form id="quiz_edit">
    <label for="quiz_name">Name</label>
    <input type="text" id="quiz_name" value="{{quiz.name}}">

    <label for="quiz_title">Title</label>
    <input type="text" id="quiz_title" value="{{quiz.title}}">
</form>