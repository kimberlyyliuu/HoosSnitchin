//REFERENCES
//RESOURCE 1
//TITLE: How to use FormData for AJAX file upload?
//URL: https://stackoverflow.com/questions/21044798/how-to-use-formdata-for-ajax-file-upload
//RESOURCE 2
//TITLE: HTML DOM Element appendChild()
//URL: https://www.w3schools.com/jsref/met_node_appendchild.asp

function upload_multiple_doc(report_id, files){
    var form_data = new FormData()
    var file = document.getElementById("file")
    for(var i = 0; i < files.length; i++) //add files that were already added
        form_data.append('files', files[i])
    form_data.append('files', file.files[0]) //add the new file
    form_data.append('report_id', report_id)
    $.ajax({
      url: "/document_upload/",
      type: "post",
      data: form_data,
      processData: false,
      contentType: false,
      success: function (response) {
        console.log(response);
      },
    });
}
function show_files(report_id){
    document.getElementById("curr_files").hidden = false
    var file = document.getElementById("file")
    var list = document.createElement("li")
    var currFile = file.files[0]
    var filename = document.createTextNode(currFile.name)
    list.appendChild(filename)
    document.getElementById("uploaded").appendChild(list)
    upload_multiple_doc(report_id, selector)
}