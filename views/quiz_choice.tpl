% rebase('skeleton.tpl', title=title)


<section class="">
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div class="w3-container">
        % for (name, description, filename, img_url) in choices:
        <section class=" quiz-card w3-card w3-third w3-hover-shadow"  style="margin: 20px 10px;">
            <a class="quiz_selection quiz-nav" href="/study/{{ name }}">
                <p class="w3-container w3-center">
                    <img alt="go to quiz" class="quiz-icon" style="height: 100%;" src="{{ img_url }}">
                </p>
                <p class="w3-center w3-container"
                   style="height: 3rem; width:100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                >{{ description }}</p>
            </a>
            % if role=='author':
            <a href="/author/edit/{{ name }}" class="quiz-nav">
                <p class="w3-container w3-blue">EDIT</p>
            </a>
            % end
        </section>
        % end
    </div>
</section>






