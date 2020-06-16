Current Server:
<select id="server">
    {% for server in servers %}
    <option value="{{server.model_id}}">{{server.name}}</option>
    {% end %}
</select><br/>
<script>
    var serverSelect = document.getElementById("server");

    serverSelect.addEventListener('change',function()){
        var value = serverSelect.value;
        if (value){
            window.location.search="?server="+value; //TODO: this just overwrites the query, not the greates idea but should work till i have the time to fix this
        }
    });
</script>