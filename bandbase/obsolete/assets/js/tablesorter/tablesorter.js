require.config(
{
    shim:
    {
        'tablesorter-without-widgets': ['jquery'],
        'tablesorter': ['tablesorter-without-widgets'],
    },
    paths:
    {
        'tablesorter-without-widgets': '/assets/js/tablesorter/js/jquery.tablesorter.min',
        'tablesorter': '/assets/js/tablesorter/js/jquery.tablesorter.widgets.min',
    }
});
