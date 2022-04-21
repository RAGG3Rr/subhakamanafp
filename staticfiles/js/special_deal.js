jQuery(function ($) {
    /* $(document).ready(function() { */
	    
	$(function() {	
        {% for deal in special_deals %}
            /* $('#matchCountdown_{{ match.id }}').countdown({until: match_date_{{ match.id }}); */
			alert('{{deal.id}}')
        {% endfor %}
    });
});