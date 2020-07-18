require.config(
{
	shim:
	{
		'tabs': ['jquery']
	},
	paths:
	{
		'tabs': 'assets/plugins/tabs/js/tabs'
	}
});

require(['tabs', 'jquery'], function()
{
	$(function()
	{
	    tabs();
	});
});
