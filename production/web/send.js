$("#mail_form").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    // var formData = JSON.stringify($("#mail_form").serializeArray());
    var form = $(this);
    console.log(form.serialize())
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
          alert(data); // show response from the php script.
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          console.log(XMLHttpRequest, textStatus, errorThrown)
       }
    });
    
});