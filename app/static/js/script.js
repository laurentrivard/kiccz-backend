$(document).ready( function () {
	$('#add_pic_button').click( function () {
		var count = $('.add_pic').length;
                if(count < 6) {
			count += 1;
			$('#add_pictures').append("<div class='add_pic'>Picture " + count +" : <input type='file' name='picture'> <br></div>");
	
		}
		else {
		alert('too many');
			}
	});
})
