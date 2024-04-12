//REFERENCES
//TITLE: How to use FormData for AJAX file upload?
//URL: https://stackoverflow.com/questions/21044798/how-to-use-formdata-for-ajax-file-upload
function upload_multiple_doc(report_id){
    var form_data = new FormData()
    form_data.append('file', $('#file')[0].files[0])
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