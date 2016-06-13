jQuery(document).ready(function($) 
{
	str = "";
    $(".clickable-row").click(function() 
    {
        window.document.location = $(this).data("href");
    });

    $("#add").click(function()
    {
    	n = parseInt($('#max_n').val());
    	s = $("#form-group-"+1).html();
    	var m = new RegExp("medicine"+1,"g");
    	s = s.replace(m,"medicine"+n);
    	var q = new RegExp("quantity"+1,"g");
    	s = s.replace(q,"quantity"+n);
    	s = s.replace(/dropdown-toggle/g,"dropdown-toggle disabled");
    	s = "<div class=\"form-group\" id=\"form-group-" + n + "\">" + s + "</div>";
    	$(s).insertAfter("#form-group-"+1);
    	str = str + $("#quantity1").val() + ',' + $("#medicine1").val() + '|'; 
    	$("#str").attr("value",str);
    });
});