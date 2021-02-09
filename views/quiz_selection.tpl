% rebase('skeleton.tpl', title=title)


<section>
<h2 class="w3-teal">Quizzes Available:</h2>
<div class="w3-container w3-ul w3-hoverable">
% for (name, description, filename) in choices:
    <li>
    <a class="quiz_selection w3-mobile w3-panel" href="/quizzes/{{name}}/0">
        <p>{{ description }}</p>
    </a>
    </li>
% end
</div>
</section>

