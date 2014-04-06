$(document).ready(function() {
	$('.page2').appear();
	$('.page4').appear();
	$('.page6').appear();

	$('.page2').on('appear', function() {
		$('.page2').animate({ opacity: 1 });
	});

	$('.page4').on('appear', function() {
		$('.page4 ul li').each(function(index, element) {
			$(element).animate({ opacity: 1 }, 800 * index);
		});
	});

	$('.page6').on('appear', function() {
		$('.page6 ul li').addClass('active');
	});
});