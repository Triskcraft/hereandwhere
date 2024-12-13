import re
from mcdreforged.api.all import *

def show_coords(src: CommandSource, server: PluginServerInterface, player):
    print(player)
    if not(player):
        name = src.player
    elif player:
        name = player
    coordsstr = re.search(r'\[([^\]]+)\]', server.rcon_query('data get entity {} Pos'.format(name)))
    coords = [int(float(num)) for num in re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', coordsstr.group(1))]
    coords_normal = str(coords[0])+", "+str(coords[1])+", "+str(coords[2])
    coords_over = "§f  ->  §c"+str(int(coords[0]/8))+", "+str(coords[1])+", "+str(int(coords[2]/8))
    coords_nether = "§f  -  >  §a"+str(int(coords[0]*8))+", "+str(coords[1])+", "+str(int(coords[2]*8))
    dim = re.search(r'(?<="minecraft:)(\w+)',server.rcon_query('data get entity {} Dimension'.format(name)))

    server.rcon_query('effect give {} minecraft:glowing 20 2'.format(name))
        
    waypoint_button = RText('[+x]', RColor.aqua).h('Crear minimapa en xaero').c(RAction.run_command, "xaero_waypoint_add:{}'s Location:{}:{}:{}:6:false:0".format(name, int(coords[0]), int(coords[1]), int(coords[2])))
    
    dim_map = {
        'overworld': ('§a', coords_over),
        'the_nether': ('§c', coords_nether),
        'the_end': ('§d', '')
    }
    
    if dim[0] in dim_map:
        color, extra_coords = dim_map[dim[0]]
        msg = f'{name} se encuentra en: {color}{coords_normal}{extra_coords}'
        server.say(msg)

def on_load(server: PluginServerInterface, info: Info):
    server.register_command(Literal('!!here').runs(lambda src: show_coords(src, server, None)))
    server.register_command(Literal('!!where').then(Text('player').runs(lambda src, ctx: show_coords(src,server, ctx['player']))))
    