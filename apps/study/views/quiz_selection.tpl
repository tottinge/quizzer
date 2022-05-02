% rebase('skeleton.tpl', title=title)


<section class="">
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div lass="w3-container">
        % for (name, description, filename, img_url) in choices:
        <a class="quiz_selection w3-container w3-card w3-third w3-hover-shadow quiz-card" href="/study/{{name}}">
                <p class="w3-container w3-center">
                    <img alt="go to quiz" class="quiz-icon" style="height: 100%;" src="{{ img_url }}">
                </p>
                <footer class="w3-center w3-container w3-large">{{ description }}</footer>
        </a>

        % end
    </div>
</section>

