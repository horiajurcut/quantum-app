function showCreateSessionModal() {
	var $modalBackground = $('<div class="modal-background"></div>').appendTo('body');
	var $modal = $('<div class="modal"></div>').css('height', '330px').appendTo('body');
	$modalBackground.animate({ opacity: .7 });
	$modal.animate({ marginTop: '-115px', top: '50%' }, function() {
		$('#session-title').focus();
	});

	$modalBackground.on('click', closeCreateSessionModal);

	var template = $('#modal-new-session').html();

	$modal.html(Mustache.to_html(template, null));
	$('.modal-close-button').on('click', closeCreateSessionModal);
	$('.cancel-create-session').on('click', closeCreateSessionModal);
	$('.submit-create-session').on('click', submitNewEvent);
	$('.date-wrapper input').datetimepicker();

	return false;
}

function submitNewEvent() {
	$('#session-start-date').val($('#start-date').val());
	$('#session-start-date').val($('#start-date').val());

	$('.new-event').submit();
}

function closeCreateSessionModal() {
	var $modalBackground = $('.modal-background');
	var $modal = $('.modal');
	$modal.animate({ marginTop: '0', top: '100%' }, function() { $modal.remove() });
	$modalBackground.animate({ opacity: 0 }, function() { $modalBackground.remove() });

	return false;
}

$(document).ready(function() {
	$('.session').on('click', function() {
		window.location.href = '/dashboard/event/' + $(this).parent().attr('data-event-id');
	});

	$('.add-session-button').on('click', showCreateSessionModal);
});
