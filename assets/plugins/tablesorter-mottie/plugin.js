require.config(
{
	shim:
	{
		'tablesorter-mottie':         ['jquery'],
		'tablesorter-mottie-pager':   ['jquery', 'tablesorter-mottie'],
		'tablesorter-mottie-widgets': ['jquery', 'tablesorter-mottie'],
	},
	paths:
	{
		'tablesorter-mottie':         'assets/plugins/tablesorter-mottie/js/jquery.tablesorter.min',
		'tablesorter-mottie-pager':   'assets/plugins/tablesorter-mottie/js/jquery.tablesorter.pager.min',
		'tablesorter-mottie-widgets': 'assets/plugins/tablesorter-mottie/js/jquery.tablesorter.widgets.min',
	}
});
