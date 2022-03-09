% rebase('skeleton.tpl', title=title)


<section>
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div class="w3-container w3-hoverable">
        % for (name, description, filename) in choices:
        <section class="w3-panel w3-card w3-third w3-hover-shadow" >
        <a class="quiz_selection" href="/study/{{name}}">
            <div>
            <p class="w3-center">{{ description }}</p>
            </div>
        </a>
        </section>

        % end
    </div>
</section>

