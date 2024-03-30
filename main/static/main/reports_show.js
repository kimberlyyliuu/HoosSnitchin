// REFERENCES
// TITLE: How To Toggle Hide/Show using JS
// URL: https://www.w3schools.com/howto/howto_js_toggle_hide_show.asp

function reports_show(report_id){
    var report_content = document.getElementById(report_id);
    if(report_content.style.display === "none"){
        report_content.style.display = "flex";
        $.ajax({
            url: '/update_report/',  
            type: 'post',
            data: {
                'report_id': report_id,
            },
            success: function(response) {
                console.log(response);
            }
        });
    }else{
        report_content.style.display = "none";
    }
}