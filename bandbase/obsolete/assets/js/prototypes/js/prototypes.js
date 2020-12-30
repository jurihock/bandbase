// https://stackoverflow.com/a/18234317
// Example 1: "Hello, {who}!".format({who: "World"});
// Example 2: "Hello, {0}!".format("World");
String.prototype.format = String.prototype.format ||
function()
{
    'use strict';

    var str = this.toString();

    if (arguments.length)
    {
        var type = typeof arguments[0];

        var args = ('string' === type || 'number' === type)
            ? Array.prototype.slice.call(arguments)
            : arguments[0];

        for (var key in args)
        {
            str = str.replace(new RegExp('\\{' + key + '\\}', 'gi'), args[key]);
        }
    }

    return str;
};

String.prototype.encode = String.prototype.encode ||
function()
{
    'use strict';

    var str = this.toString();
    var uri = encodeURI(str);

    return uri;
};

String.prototype.decode = String.prototype.decode ||
function()
{
    'use strict';

    var uri = this.toString();
    var str = decodeURI(uri);

    return str;
};

String.prototype.base64 = String.prototype.base64 ||
function()
{
    'use strict';

    var str = this.toString();
    var b64 = btoa(unescape(encodeURIComponent(str)));

    return b64;
};

String.prototype.lower = String.prototype.lower ||
function()
{
    'use strict';

    return this.toString().toLowerCase();
};

String.prototype.upper = String.prototype.upper ||
function()
{
    'use strict';

    return this.toString().toUpperCase();
};

String.prototype.hash = String.prototype.hash ||
function()
{
    'use strict';

    var value = this.toString();
    var result = 0;

    if (value.length === 0)
        return result;

    for (var i = 0; i < value.length; i++)
    {
        var char = value.charCodeAt(i);

        result = ((result << 5) - result) + char;
        result = result & result;
    }

    return result;
};

String.prototype.zeropad = String.prototype.zeropad ||
function()
{
    'use strict';

    var value = this.toString();
    var length = arguments[0];

    while (value.length < length)
    {
        value = '0' + value;
    }

    return value;
};

// https://stackoverflow.com/a/30810322
String.prototype.toclipboard = String.prototype.toclipboard ||
function()
{
    'use strict';

    var value = this.toString();

    if (!value)
    {
        return;
    }

    var dummy = document.createElement('textarea');

    dummy.style.position = 'fixed';
    dummy.style.top = 0;
    dummy.style.left = 0;
    dummy.style.width = '1em';
    dummy.style.height = '1em';
    dummy.style.padding = 0;
    dummy.style.border = 'none';
    dummy.style.outline = 'none';
    dummy.style.boxShadow = 'none';
    dummy.style.background = 'transparent';

    dummy.value = value;

    document.body.appendChild(dummy);

    dummy.focus();
    dummy.select();

    var ok = false;

    try
    {
        ok = document.execCommand('copy');

        if (!ok)
        {
            throw ok;
        }
    }
    catch (e)
    {
        window.prompt(
            'Der folgende Text konnte leider nicht automatisch in die Zwischenablage kopiert werden! ' +
            'Bitte die Tastenkombination Ctrl+C manuell betätigen, dann klappt\'s bestimmt...', value);
    }

    document.body.removeChild(dummy);

    return ok;
};
