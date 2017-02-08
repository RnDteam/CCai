$(document).ready(function(){
	/* =================
	   Instagram Gallery
	====================*/
	var accessToken = '33864256.d8d1d50.db28f9687c694ab2b47258699ed5c469'; // Your Instagram access token, get yours here: http://instagramwordpress.rafsegat.com/docs/get-access-token/
	var userId = '33864256'; // Your instagram User ID, it's on the first row from your access token (before the first dot sign)

	function createPhotoElement(photo) {
	  var innerHtml = $('<img>')
	    .addClass('instagram-image')
	    .attr('src', photo.images.thumbnail.url);

	  innerHtml = $('<a>')
	    .attr('target', '_blank')
	    .attr('href', photo.link)
	    .append(innerHtml);

	  return $('<li>')
	    .addClass('instagram-placeholder')
	    .attr('id', photo.id)
	    .append(innerHtml);
	}

	function didLoadInstagram(event, response) {
	  var that = this;

	  $.each(response.data, function(i, photo) {
	    $(that).append(createPhotoElement(photo));
	  });
	}

	$('.instagram.tag').on('didLoadInstagram', didLoadInstagram);
	$('.instagram.tag').instagram({
		count: 12,
		userId: userId,
		accessToken: accessToken
	});

});



