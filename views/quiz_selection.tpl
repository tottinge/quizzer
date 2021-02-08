% rebase('skeleton.tpl', title=title)


<section class="w3-container">
<h2 class="w3-teal">Quizzes Available:</h2>
<ul>
% for (name, description, filename) in choices:
<li><a class="quiz_selection" href="/quizzes/{{name}}/0">{{ description }}</a></li>
% end
</ul>
</section>

