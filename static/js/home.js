$(document).ready(function(){
	$.ajax({
        type: 'GET',
        url: '/api/v1/get-articles-list?format=json',

        success: function (data) {
        	$.each(data, function(index){
				$('.card-lists ').append('<div class="col-md-6 col-sm-6 col-xs-12" id=""><a href="'+data[index].url+'" target="_blank">'+
				    			'<div class="card" ><div class="img-container"><div class="hn-article-description">'+
				    			'<h4>'+ data[index].title +'</h4><br><br><br><br>'+
				    			'<p class="">Sentiment: '+data[index].sentiment_score+'% '+ data[index].sentiment_type +'</p>'+
				    			// '<h4>Title:'+ data[index].title +'</h4><br>'+
				    			'</div></div><div class="details"><div class="link-title">'+
				    			'Author: '+ data[index].author_username +
				    			'<p class="pull-right">Upvote: '+data[index].score+'</p>'+
				    			'</div></div><div class="clearfix"></div>'+
				    			'</div></a></div>')
				})
        },
    })

	var delay = (function(){
	  var timer = 0;
	  return function(callback, ms){
	    clearTimeout (timer);
	    timer = setTimeout(callback, ms);
	  };
	})();

	$('#searchForm').submit(function(e){
		e.preventDefault();
	})

	$('#searchForm .input-search').bind('keyup', function (e) {
		if(e.keyCode == 13){
        	e.preventDefault();
    	}
		delay(function(){
			var newContent = $(this.target).val()
			searchLink(newContent)
	    }, 1000 );
    })

    function searchLink(value){
		var query = $('#searchForm .input-search').val();
		var formData = {
			'q': query,
		}
		if (query){
			$.ajax({
				type: 'GET',
				url: '/api/v1/search-articles?format=json',
				data: formData,
				success: function(data) {
					$('#search-lists').empty();
					if(data.length==0){
						console.log('nodata');
						$('#search-lists').prepend('<a href="" target="_blank"><div class="title">'+
							'No Result Matches your search</div><div class="hosts mar-t-5"></div></a>');
					} else {
						$.each(data, function(index){
							getSearchData(data[index]);
						})
					}
				}
			})
		} else {
			$('#search-lists').empty();
		}
	}

	function getSearchData(data) {
		var markup = '<a href="'+data.url+'" target="_blank">';
			markup += '<div class="title">' + data.title + '</div>';
			markup += '</a>';

		return $('#search-lists').prepend(markup);
	}
});