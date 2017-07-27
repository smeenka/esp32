    jQuery(document).ready(function() {
    console.log(' document ready');


	jQuery('.tabs .tab-links a').on('click', function(e)  {
	    var currentAttrValue = jQuery(this).attr('href');

	    console.log(' tabs .tab-links on click ' +  currentAttrValue);

	    // Show/Hide Tabs
	    jQuery('.tabs ' + currentAttrValue).show().siblings().hide();

	    // Change/remove current tab to active
	    jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

	    e.preventDefault();

	});

});
