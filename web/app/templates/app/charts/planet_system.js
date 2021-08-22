
var p_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#3644E4',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6'
}

function draw_planet(pdata){
    console.log(pdata)
    dwaw_node("pSystem",
            pdata["nodes"],
            pdata["links"],
            p_objectColors,
            .15,
            height,
            width,
            strokesFunc = s_objectStrokes) 
}




