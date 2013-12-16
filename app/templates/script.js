$(document).ready( function () {
	alert('hello');
	$('#add_pic_button').click( function () {
		var count = 3;
		count++;
		$('#add_pictures').append("<div id='add_pic'>Picture " + count +" : <input type='file' name='picture'" + count + "> <br></div>");
	});
})