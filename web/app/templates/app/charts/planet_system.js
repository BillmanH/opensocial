
var s_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#3644E4',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6'
}

$("#sSystem").click(function () {
    console.log( $(this).val() );
  });

$.ajax({
    url: '/ajax/planet/',
    data: {
        'planet': 'planet'
    },
    dataType: 'json',
    success: dwaw_node("pSystem",
                        nodes,
                        links,
                        s_objectColors,
                        .15,
                        height,
                        width) 
});


