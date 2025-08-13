include <box.scad>

blinker_x = 43;
blinker_y = 65;
blinker_z = 18;

resin_thickness = 8;

capacitor_r = 16/2;
capacitor_z = 33;
capacitor_n = 2;

box_x = blinker_x+resin_thickness*2;
box_y = blinker_y+resin_thickness*2;
box_z = blinker_z+resin_thickness*2;
echo("Box dimensions: ", box_x, "x", box_y, "x", box_z, " mm");

box(width = box_x,
    depth = box_y,
    height = box_z,
    thickness = 2.8,
    inner=true,
    assemble = false,
    open=true);

resin_floor_volume = (box_x*box_y*resin_thickness)/1000;
capacitors_volume = 2*(capacitor_r^2)*capacitor_z*capacitor_n/1000;

resin_rest_volume = (box_x*box_y*box_z)/1000 - resin_floor_volume - capacitors_volume;

echo("Resin floor volume: ", resin_floor_volume, " mL");
echo(resin_floor_volume*(2/3), " mL part A");
echo(resin_floor_volume*(1/3), " mL part B");

echo("Resin rest volume: ", resin_rest_volume, " mL");
echo(resin_rest_volume*(2/3), " mL part A");
echo(resin_rest_volume*(1/3), " mL part B");