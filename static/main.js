function set_sidebar(sidebar_item){
    switch (sidebar_item){
    case 'expenses':
        {$("#sidebar-expenses").addClass("active");
        $("#sidebar-balance").removeClass("active");
        $("#sidebar-settings").removeClass("active");
        $("#sidebar-how-to").removeClass("active");}
        
        break;
    case 'balance':
        {$("#sidebar-expenses").removeClass("active");
        $("#sidebar-balance").addClass("active");
        $("#sidebar-settings").removeClass("active");
        $("#sidebar-how-to").removeClass("active");}
        break;
    case 'settings':
        {$("#sidebar-expenses").removeClass("active");
        $("#sidebar-balance").removeClass("active");
        $("#sidebar-settings").addClass("active");
        $("#sidebar-how-to").removeClass("active");}
        break;
    case 'how-to':
        {$("#sidebar-expenses").removeClass("active");
        $("#sidebar-balance").removeClass("active");
        $("#sidebar-settings").removeClass("active");
        $("#sidebar-how-to").addClass("active");}
        break;
    case 'none':
        {$("#sidebar-expenses").removeClass("active");
        $("#sidebar-balance").removeClass("active");
        $("#sidebar-settings").removeClass("active");
        $("#sidebar-how-to").removeClass("active");}
        break;
        
    }
    }

function update_bootstrap_dropdown_button_by_selection(event){

    selection = ($(this).children(":first").html());
    $(this).parent().parent().children(":first").html(selection);


}

function show_static_info(){

msg = "This alert is served from static files\n"
msg = msg + "=============================\n";
msg = msg + "Serving static js, css files:\n"
msg = msg + "Development: Web server django dev server, DEBUG=True. Files are served directly from the repository static directory by django (mysite/site_repo/static) \n";
msg = msg + "Production: Web server Nginx/Apache, DEBUG=False. Files are served from the static_root directory, by Nginx location alias. \n"
msg = msg + "Testing: Web server Nginx/Apache, DEBUG=True. Files are served from static_root with nginx, but with the original file name (instead of the hashed name which collectstatic adds) \n";
msg = msg + "See Readme"
alert(msg);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function style_elements(){

    $("select").addClass("form-control");
     $(":text").addClass("form-control");
     $(":input[type='number']").addClass("form-control");
     $(":input[type='email']").addClass("form-control");
     $(":input[type='password']").addClass("form-control");
    


}

