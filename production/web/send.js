$("#mail_form").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    // var formData = JSON.stringify($("#mail_form").serializeArray());
    var form = $(this);
    console.log(form.serialize())

    document.getElementById('out_title').innerHTML = ""
    document.getElementById('out_content').innerHTML = "Generating..."
    // var actionUrl = form.attr('action');
    $.ajax({
        type: "POST",
        dataType: 'json',
        crossDomain: true,
        url: "http://127.0.0.1:8000/api/mails/",
        data: form.serialize(), // serializes the form's elements.
        xhrFields: { withCredentials: true },
        success: function(data)
        {
          console.log(data)
          document.getElementById('out_title').innerHTML = data["subject"].replace(/(?:\r\n|\r|\n)/g, '<br>')
          document.getElementById('out_content').innerHTML = data["content"].replace(/(?:\r\n|\r|\n)/g, '<br>') // show response from the php script.
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          document.getElementById('out_title').innerHTML = "Mail Title"
          document.getElementById('out_content').innerHTML = "Content"
          console.log(XMLHttpRequest, textStatus, errorThrown)
       }
    });
    
});

function reset_act(){
  document.getElementById('out_title').innerHTML = "Mail Title"
  document.getElementById('out_content').innerHTML = "Content"  
}
