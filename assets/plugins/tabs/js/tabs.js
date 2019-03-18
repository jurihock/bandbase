function tab(id)
{
    $('div[data-tab]').each(function()
    {
        if ($(this).attr('data-tab') == id)
        {
            $(this).show();
        }
        else
        {
            $(this).hide();
        }
    });

    $('a[data-tab]').each(function()
    {
        if ($(this).attr('data-tab') == id)
        {
            $(this).addClass('active');
        }
        else
        {
            $(this).removeClass('active');
        }
    });
}

function tabs()
{
    $('a[data-tab]').each(function()
    {
        $(this).click(function()
        {
            var id = $(this).attr('data-tab');

            tab(id);

            return false;
        });
    });

    var id = $('a[data-tab]').attr('data-tab');

    tab(id);
}
