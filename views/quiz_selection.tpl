% rebase('skeleton.tpl', title=title)


<section>
<h2 class="w3-teal">Quizzes Available:</h2>
<div class="w3-container w3-ul w3-hoverable">
% for (name, description, filename) in choices:
    <a class="quiz_selection w3-button w3-mobile" href="/quizzes/{{name}}/0">
        <li>{{ description }}</li>
    </a>
% end
</div>
</section>

