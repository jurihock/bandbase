require.config(
{
    shim:
    {
        'bootstrap': ['jquery'],
    },
    paths:
    {
        'bootstrap': '/assets/js/bootstrap/js/bootstrap.bundle.min',
    }
});

require(['jquery', 'bootstrap'], function($)
{
    $(function()
    {
        $('[data-toggle="tooltip"]').tooltip();
    });
});
