% rebase('skeleton.tpl', title=title)


<form>
% for (name, description, filename) in choices:
<a class="quiz_selection" href="/quizzes/{{name}}/0">{{ description }}</a>
<br/>
% end
</form>

