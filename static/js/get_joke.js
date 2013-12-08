$(document).ready(function(){
	$('.btn').click(function(){
		$('.joke').load($SCRIPT_ROOT + '/_get_joke');
	});
	return false;
});


