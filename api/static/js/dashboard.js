function showQuestionsModal() {
	var $modalBackground = $('<div class="modal-background"></div>').appendTo('body');
	var $modal = $('<div class="modal"></div>').css('height', '400px').appendTo('body');
	$modalBackground.animate({ opacity: .7 });
	$modal.animate({ marginTop: '-200px', top: '50%' }, function() {
		$('#reply-composer').focus();
	});

	$modalBackground.on('click', closeQuestionsModal);

	var template = $('#modal-question').html();
	var data = {
		question: "I love when actors actually have--and run--their own FB pages. You were already one of my favorite actors and seeing stuff like this only makes me love you more!",
		askedby : [
			{
				full_name: 'Stefan Filip',
				user_id: 'stefy.filip',
				avatar: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/t1.0-1/p160x160/1975001_10152232954170395_510883959_n.jpg'
			},
			{
				full_name: 'Horia Jurcut',
				user_id: 'horiajurcut',
				avatar: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1.0-1/c0.45.160.160/p160x160/1391726_10151966902849082_288564753_n.jpg'
			},
			{
				full_name: 'Giorgiana Petre',
				user_id: 'giorgiana.petre',
				avatar: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/t1.0-1/c0.29.160.160/p160x160/1010306_10202683853310726_2016244149_n.jpg'
			}
		]	
	};

	$modal.html(Mustache.to_html(template, data));
	$('.modal-close-button').on('click', closeQuestionsModal);

	return false;
}

function closeQuestionsModal() {
	var $modalBackground = $('.modal-background');
	var $modal = $('.modal');
	$modal.animate({ marginTop: '0', top: '100%' }, function() { $modal.remove() });
	$modalBackground.animate({ opacity: 0 }, function() { $modalBackground.remove() });

	return false;
}

$(document).ready(function() {
	$('.questions-list tbody tr').on('click', showQuestionsModal);
});