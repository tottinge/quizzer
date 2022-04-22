% rebase('skeleton.tpl', title=title)

% from dataclasses import asdict
<script src="//unpkg.com/json-form-custom-element"></script>
<script>
    document = "{{ asdict(quiz) }}";
</script>
<script>
    var url="/static/quiz_schema.json"
    fetch (url).then(
        function(response) {console.log(response.json())}
    )
</script>
% if error:
    <p id="post-message" class="w3-panel w3-pale-red w3-leftbar w3-border-amber">{{message}}</p>
% else:
    <p id="post-message" class="w3-panel w3-khaki w3-leftbar w3-border-amber">{{message}}</p>
% end
<form id="quiz_edit" action="/author/edit" method="POST">

    <input type="hidden" id="quiz" name="quiz" value="{'updated':'false'}">

    <json-form name="charlie" schema="{{ schema }}" value="{{ raw_quiz }}"
            onChange="changeDocumentValue(this)"
    ></json-form>

    <script>
        function changeDocumentValue(origin) {
            const documentField = document.getElementById("quiz");
            const value = origin.getAttribute("value");
            documentField.value = value;
        }
    </script>

    <button class="w3-button w3-teal" id="save_changes" type="submit">Save</button>

</form>