function showQuestionsModal() {
	var $modalBackground = $('<div class="modal-background"></div>').appendTo('body');
	var $modal = $('<div class="modal"></div>').css('height', '400px').appendTo('body');
	$modalBackground.animate({ opacity: .7 });
	$modal.animate({ marginTop: '-200px', top: '50%' }, function() {
		$('#reply-composer').focus();
	});

	$('html, body').css({
	    'overflow': 'hidden',
	    'height': '100%'
	});

	$modalBackground.on('click', closeQuestionsModal);

	var groupId = $(this).attr('data-group-id');

	$.ajax({
        url: "/dashboard/" + groupId + "/details",
        type: "GET",
        success: function(data) {
        	var template = $('#modal-question').html();

        	data.groupId = groupId;

			$modal.html(Mustache.to_html(template, data));
			$('.modal-close-button').on('click', closeQuestionsModal);

			$('#reply-button').on('click', function(){
				var groupId = $(this).attr('data-group-id');
				$.ajax({
			        url: "/dashboard/" + groupId + "/reply",
			        type: "POST",
			        data: {
			        	message: $('#reply-composer').val()	
			        },
				    dataType: "json",
		   		});
		   		$('.questions-list tbody tr[data-group-id="' + groupId + '"]').remove();
		   		closeQuestionsModal();
			});
    	},
	    dataType: "json",
    });

	return false;
}

function closeQuestionsModal() {
	var $modalBackground = $('.modal-background');
	var $modal = $('.modal');
	$modal.animate({ marginTop: '0', top: '100%' }, function() { $modal.remove() });
	$modalBackground.animate({ opacity: 0 }, function() { $modalBackground.remove() });

	$('html, body').css({
	    'overflow': 'auto',
	    'height': 'auto'
	});

	return false;
}

function polling() {

	var eventId = parseInt($('body').attr('data-event-id'), 10);

    $.ajax({
        url: "/dashboard/event/" + eventId + "/polling",
        type: "GET",
        success: function(data) {

            // Update page
            $('.questions-overview .content .value').text(data.questionsNumber);
			$('.users-overview .content .value').text(data.usersOverview);
			$('.questions-list tbody').html('');

			data.unansweredQuestions.sort(function(a,b){return b.frequency-a.frequency});

			jQuery.each(data.unansweredQuestions, function(index, value) {

				if(value.sentiment === 'positive') {
					data.totalPositive++;
					sentiment = 'green';
				} else {
					if(value.sentiment === 'negative') {
						data.totalNegative++;
						sentiment = 'red';
					} else {
						data.totalNeutral++;
						sentiment = 'grey';
					}
				}

				$('.questions-list tbody').append('<tr data-group-id="' + value.id + '">\
					<td class="sentiment ' + sentiment + '"></td>\
					<td class="question">' + value.question + '</td>\
		            <td class="frequency"><span>' + value.frequency + '</span></td>\
		        </tr>');
			});

			$('.positive').text('+' + data.totalPositive);
			$('.neutral').text(data.totalNeutral);
			$('.negative').text('-' + data.totalNegative);

			$('.questions-list tbody tr').on('click', showQuestionsModal);
        },
        dataType: "json",
        complete: setTimeout(function() { polling() }, 5000),
        timeout: 2000
    })
}


$(document).ready(function() {
	polling();
	$('.questions-list tbody tr').on('click', showQuestionsModal);
});