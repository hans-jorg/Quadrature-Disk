"""Quadrature disk generator

This script generates the PS (PostScript) description of a disk
to be used as a position or velocity sensor.

There is an alternative output format. Some printers and/or typesetters
does not generate the correct image with one format.

The parameters are:
       r : radius in mm
       c : center radius
       m : external margin
       s : slot height in mm
       d : distance between slot rings
       a : alternate format
"""
import argparse


texto1="""%!PS
% prints a quadrature encoder disk with {0} slots
/mm {{ 2.835 mul }} def

%%%%%%%% constants
/center     {{ {1} mm 5 mm add {1} mm 1.5 mul }} def
/radiusext  {{ {1} mm }} def
/radius1    {{ radiusext {3} mm sub }} def
/radius2    {{ radius1 {4} mm sub }} def
/radius3    {{ radius2 {5} mm sub }} def
/radius4    {{ radius3 {4} mm sub }} def
/slots      {0}  def

%%%%%%%% external circle
center
radiusext
0 360 arc stroke

%%%%%%%% define color
0 0 0 setrgbcolor

%%%%%%%% define angle increment
 360 slots div
/inc exch def

%%%%%%%% draw arc slices
0 inc 180 {{
    2 mul
    dup
    /a1 exch def
    a1 inc add
    /a2 exch def
    center moveto
    center
    radius1
    a1 a2 arc fill
}} for
stroke

%%%%%%%% clear center
1 1 1 setrgbcolor
center
radius2
0 360 arc fill

%%%%%%%% draw arc slices
0 0 0 setrgbcolor
0.25 inc mul
 inc 180 {{
    2 mul inc add
    dup
    /a3 exch def
    a3 inc add
    /a4 exch def
    center moveto
    center
    radius3
    a3 a4 arc fill
}} for
stroke

%%%%%%%% clear center
1 1 1 setrgbcolor
center
radius4
0 360 arc fill

%%%%%%%% circle at center
0 0 0 setrgbcolor
center
{2} mm
0 360 arc stroke

%%%%%%%% cross at center
0 0 0 setrgbcolor
/ll {2} 1.5 mul def

newpath
center  moveto
0 ll mm rlineto
center  moveto
0 0 ll sub mm rlineto
center  moveto
ll mm 0  rlineto
center  moveto
0 ll sub mm 0  rlineto
stroke
closepath
showpage
"""

texto2="""%!PS
% prints a quadrature encoder disk with {0} slots, alternative format
/mm {{ 2.835 mul }} def

%%%%%%%% constants
/center     {{ {1} mm 5 mm add {1} mm 1.5 mul }} def
/radiusext  {{ {1} mm }} def
/radius1    {{ radiusext {3} mm sub }} def
/radius2    {{ radius1 {4} mm sub }} def
/radius3    {{ radius2 {5} mm sub }} def
/radius4    {{ radius3 {4} mm sub }} def
/slots      {0}  def

%%%%%%%% define color
0 0 0 setrgbcolor

%%%%%%%% define angle increment
360 slots div
/inc exch def

center
    /y exch def
    /x exch def


x y radiusext 0 360 arc stroke

/SlotExt {{
    newpath
    %initial point
        x radius1 a1 cos mul add
        y radius1 a1 sin mul add
        moveto
    % first arc
        center radius1 a1 a2 arc
    % first line inwards
        x radius2 a2 cos mul add
        y radius2 a2 sin mul add
        lineto
    % second arc
        center radius2 a2 a1 arcn
    % second line outwards
        x radius1 a1 cos mul add
        y radius1 a1 sin mul add
        lineto

    closepath
    fill
}} def

/SlotInt {{
    newpath
    %initial point
        x radius3 a1 cos mul add
        y radius3 a1 sin mul add
        moveto
    % first arc
        center radius3 a1 a2 arc
    % first line inwards
        x radius3 a2 cos mul add
        y radius3 a2 sin mul add
        lineto
    % second arc
        center radius4 a2 a1 arcn
    % second line outwards
        x radius4 a1 cos mul add
        y radius4 a1 sin mul add
        lineto
    closepath
    fill
}} def

inc 2 div
/inc2 exch def
inc 4 div
/inc4 exch def

0 inc 360 {{
/a1 exch def
a1 inc2 add
/a2 exch def
SlotExt
}} for

inc4 inc 360 {{
/a1 exch def
a1 inc2 add
/a2 exch def
SlotInt
}} for

%%%%%%%% circle at center
0 0 0 setrgbcolor
center
{2} mm
0 360 arc stroke

%%%%%%%% cross at center
0 0 0 setrgbcolor
/ll {2} 1.5 mul def

newpath
center  moveto
0 ll mm rlineto
center  moveto
0 0 ll sub mm rlineto
center  moveto
ll mm 0  rlineto
center  moveto
0 ll sub mm 0  rlineto
stroke
closepath
showpage
"""

def gendisk(filename,t,r,n,c,m,s,d):
    #generates a file with a postscript description of a disk to generate
    #   quadrature signals
    #   It used the t parameter as a template
    #   r : radius in mm
    #   c : center radius
    #   m : external margin
    #   s : slot height in mm
    #   d : distance between slot rings

    with open(filename,"w") as out:
        out.write(t.format(n,r,c,m,s,d))

def main():
    # Main routine

    parser = argparse.ArgumentParser("quadrature")
    parser.add_argument("-n",help="The number of slots of a channel", type=int, default=90)
    parser.add_argument("-a",help="Alternative Postscript output", default=False,action="store_true")
    parser.add_argument("-r",help="The disk external ratius", type=float, default=100.0)
    parser.add_argument("-m",help="The external margin", type=float, default=5.0)
    parser.add_argument("-s",help="The slots size", type=float, default=10.0)
    parser.add_argument("-c",help="center radius", type=float, default=20.0)
    parser.add_argument("-d",help="distance between sloots",
        type=float, default=1.0)
    parser.add_argument("-o",help="The output PS file",type=str,  default="disk.ps")

    args = parser.parse_args()
    if args.o == "disk.ps":
        args.o = "disk"+str(args.n)+".ps"
    print(f"slots = {args.n}")
    print(f"radius = {args.r}")
    print(f"output = {args.o}")
    if args.a:
        gendisk(args.o,texto2,args.r,args.n,args.c,args.m,args.s,args.d)
    else:
        gendisk(args.o,texto1,args.r,args.n,args.c,args.m,args.s,args.d)

# Entry Point
if __name__ == '__main__':
    main()

