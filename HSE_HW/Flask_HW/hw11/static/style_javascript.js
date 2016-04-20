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
	
	var start = 0
	var amount = 5
	var add_texts = function(data){
		start += amount
		$.each(data.texts, function(){
			$("<li class='list-group'>")
				.append($("<a href='/view/" + this.textid + "' class='list-group-item'>").text(this.text))
				.insertBefore($("#load_more"))
		})
	}
	
	$("#load_more").click(function(event){
		event.preventDefault()	
		$.getJSON(json_texts, 
				  {start:start, amount:amount},
				  add_texts)
		})
	
	$('#myAffix').affix({
		offset: {
			top: 10,
			left: 10,
			bottom: function(){
				return (this.bottom = $('.footer').outerHeight(true))
			}
		}
	})
})
