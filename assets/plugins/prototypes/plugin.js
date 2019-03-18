require.config(
{
	shim:
	{
		'prototypes': ['jquery']
	},
	paths:
	{
		'prototypes': 'assets/plugins/prototypes/js/prototypes'
	}
});

require(['prototypes']);
