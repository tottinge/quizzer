% rebase('skeleton.tpl', title=title)

% from dataclasses import asdict
<script src="//unpkg.com/json-form-custom-element"></script>
<!--
<script>
    document = "{{ asdict(quiz) }}";
</script>
-->
<script>
    const url="/static/quiz_schema.json"
    fetch (url)
        .then ( response => response.text() )
        .then ( schema => document.getElementById("quiz-editor").setAttribute("schema", schema) )
</script>

% if message:
<p id="post-message"
   class="w3-panel {{ "w3-pale-red" if error else "w3-khaki"}} w3-leftbar w3-border-amber">
    {{message}}
</p>
% end

<form id="quiz_edit" action="/author/edit" method="POST">

    <input type="hidden" id="quiz" name="quiz" value="{'updated':'false'}">

    <json-form id="quiz-editor" value="{{ raw_quiz }}"
            onChange="changeDocumentValue(this)"
    ></json-form>

    <script>
        function changeDocumentValue(origin) {
            const documentField = document.getElementById("quiz");
            documentField.value = origin.getAttribute("value");
        }
    </script>

    <button class="w3-button w3-teal" id="save_changes" type="submit">Save</button>

</form>