 $(document).ready(function() {
	
	$('body header').hover(function() {
		$('nav')
			.slideDown({height: '3em', width: '3em'})
			.show()
	})

	$('body header').mouseleave(function() {
		$('nav')
			.hide()
	})
})
