----------------------
SMOK SPACEMAN 10K PRO
----------------------
Battery Status Display
Breakout Info
----------------------

##########

Pin 1 High:
Pin 2 low 		= left digit top segment
Pin 3 low 		= left digit bottom left segment
Pin 4 low 		= left digit top left segment
Pin 5 low 		= left digit bottom segment

Pin 2 High:
Pin 1 low 		= left digit top right segment
Pin 3 low 		= left digit bottom right segment
Pin 4 low 		= left digit middle segment
Pin 5 low 		= right digit top segment

Pin 3 High:
Pin 1 low 		= right digit bottom left segment
Pin 2 low 		= right digit bottom segment
Pin 4 low 		= right digit top left segment
Pin 5 low 		= right digit middle segment

Pin 4 High:
Pin 1 low 		= right digit bottom right segment
Pin 2 low 		= percent symbol
Pin 3 low 		= right digit top right segment
Pin 5 low 		= N/A

Pin 5 High:
Pin 1 low 		= N/A
Pin 2 low		= N/A
Pin 3 low 		= indicator green
Pin 4 low 		= indicator red

##########

Left digit segments:
Top			= 1 High + 2 Low
Top-Left		= 1 High + 4 Low
Top-Right		= 2 High + 1 Low
Middle			= 2 High + 4 Low
Bottom-Left		= 1 High + 3 Low
Bottom-Right		= 2 High + 3 Low
Bottom			= 1 High + 5 Low

Right digit segments:
Top			= 2 High + 5 Low
Top-Left		= 3 High + 4 Low
Top-Right		= 4 High + 3 Low
Middle			= 3 High + 5 Low
Bottom-Left		= 3 High + 1 Low
Bottom-Right		= 4 High + 1 Low
Bottom			= 3 High + 2 Low

Percent symbol:
On			= 4 High + 2 Low

Indicator light:
Green			= 5 High + 3 Low
Red			= 5 High + 4 Low

##########

Left digit:
0			= Left-Top + Left-Top-Right + Left-Bottom-Right + Left-Bottom + Left-Bottom-Left + Left-Top-Left
1			= Left-Top-Right + Left-Bottom-Right
2			= Left-Top + Left-Top-Right + Left-Middle + Left-Bottom-Left + Left-Bottom
3			= Left-Top + Left-Top-Right + Left-Middle + Left-Bottom-Right + Left-Bottom
4			= Left-Top-Left + Left-Middle + Left-Top-Right + Left-Bottom-Right
5			= Left-Top + Left-Top-Left + Left-Middle + Left-Bottom-Right + Left-Bottom
6			= Left-Top + Left-Top-Left + Left-Bottom-Left + Left-Bottom + Left-Bottom-Right + Left-Middle
7			= Left-Top + Left-Top-Right + Left-Bottom-Right
8			= Left-Top + Left-Top-Right + Left-Middle + Left-Bottom-Right + Left-Bottom + Left-Bottom-Left + Left-Top-Left
9			= Left-Top-Left + Left-Top + Left-Top-Right + Left-Middle + Left-Bottom-Right + Left-Bottom

Right digit:
0			= Right-Top + Right-Top-Right + Right-Bottom-Right + Right-Bottom + Right-Bottom-Left + Right-Top-Left
1			= Right-Top-Right + Right-Bottom-Right
2			= Right-Top + Right-Top-Right + Right-Middle + Right-Bottom-Left + Right-Bottom
3			= Right-Top + Right-Top-Right + Right-Middle + Right-Bottom-Right + Right-Bottom
4			= Right-Top-Left + Right-Middle + Right-Top-Right + Right-Bottom-Right
5			= Right-Top + Right-Top-Left + Right-Middle + Right-Bottom-Right + Right-Bottom
6			= Right-Top + Right-Top-Left + Right-Bottom-Left + Right-Bottom + Right-Bottom-Right + Right-Middle
7			= Right-Top + Right-Top-Right + Right-Bottom-Right
8			= Right-Top + Right-Top-Right + Right-Middle + Right-Bottom-Right + Right-Bottom + Right-Bottom-Left + Right-Top-Left
9			= Right-Top-Left + Right-Top + Right-Top-Right + Right-Middle + Right-Bottom-Right + Right-Bottom
