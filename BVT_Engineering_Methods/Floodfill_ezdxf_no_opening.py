# -*- coding: utf-8 -*-

!pip install ezdxf
import ezdxf

import sys
import numpy as np
import matplotlib.pyplot as plt
#turn inline plot off
plt.ioff()
import itertools
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from IPython.display import Image
from ezdxf import math
from ezdxf import bbox
from genericpath import exists
from matplotlib.patches import Polygon

#create dxf doc
def create_dxf_doc(grid_ceiling_coords):

  doc = ezdxf.new("R2000")

  #create modelspace
  msp = doc.modelspace()
  #create layer
  doc.layers.add(name = "room_border", color = 2, linetype="SOLID")
  doc.layers.add(name = 'grid', color = 0, linetype="SOLID")
  #create room outline

  room_border = msp.add_lwpolyline(
      grid_ceiling_coords, close = True, 
      dxfattribs={'layer': 'room_border'})
   
  filename = "polyline1.dxf"
  return room_border, filename


#create drawing figure
def display_drawing(filename):
  # Safe loading procedure (requires ezdxf v0.14):
  try:
      doc, auditor = recover.readfile(filename)
  except IOError:
      print(f'Not a DXF file or a generic I/O error.')
      sys.exit(1)
  except ezdxf.DXFStructureError:
      print(f'Invalid or corrupted DXF file.')
      sys.exit(2)
  # The auditor.errors attribute stores severe errors,
  # which may raise exceptions when rendering.
  if not auditor.has_errors:
      fig = plt.figure()
      ax = fig.add_axes([0, 0, 1, 1])
      ctx = RenderContext(doc)
      out = MatplotlibBackend(ax)
      Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
      drawing_name = filename.replace(".dxf", ".png")
      fig.savefig(drawing_name, dpi=200)


# The ceiling side is assumed start from bottom-left in 
#counter cloclwise orientation
side_x_bot = list()
side_x_top = list()
y_side_x_bot = list()
y_side_x_top = list()

def ceiling_x(grid_ceiling_coords):
  for i in range(len(grid_ceiling_coords) - 1):
    if grid_ceiling_coords[i][1] == grid_ceiling_coords[i + 1][1]:
      x_1 = grid_ceiling_coords[i][0]
      x_2 = grid_ceiling_coords[i + 1][0]
      y = grid_ceiling_coords[i][1]
      if x_2 > x_1:
        start_point = [x_1, y]
        end_point = [x_2, y]
        side_x_bot.append([start_point, end_point])
        side_x_bot.sort(key = lambda side_x_bot:side_x_bot[1])
        y_side_x_bot.append(y)
      else:
        x_1 = grid_ceiling_coords[i + 1][0]
        x_2 = grid_ceiling_coords[i][0]
        start_point = [x_1, y]
        end_point = [x_2, y]
        side_x_top.append([start_point, end_point])
        side_x_top.sort(key = lambda side_x_top:side_x_top[1])
        y_side_x_top.append(y)
 
  return side_x_bot, side_x_top

side_y_left = list()
side_y_right = list()
x_side_y_left = list()
x_side_y_right = list()
def ceiling_y(grid_ceiling_coords):
  for i in range(len(grid_ceiling_coords) - 1):
    if grid_ceiling_coords[i][0] == grid_ceiling_coords[i + 1][0]:
      y_1 = grid_ceiling_coords[i][1]
      y_2 = grid_ceiling_coords[i + 1][1]
      x = grid_ceiling_coords[i][0]
      if y_2 > y_1:
        start_point = [x, y_1]
        end_point = [x, y_2]
        side_angle = 90
        side_y_right.append([start_point, end_point, side_angle])
        side_y_right.sort(key = lambda side_y_right:side_y_right[0])
      else:
        start_point = [x, y_2]
        end_point = [x ,y_1]
        side_angle = 90
        side_y_left.append([start_point, end_point, side_angle])
        side_y_left.sort(key = lambda side_y_left:side_y_left[0])

    #Diogonal sides
    elif (grid_ceiling_coords[i][0] != grid_ceiling_coords[i + 1][0] 
          and grid_ceiling_coords[i][1] != grid_ceiling_coords[i + 1][1]):
      y_1 = grid_ceiling_coords[i][1]
      y_2 = grid_ceiling_coords[i + 1][1]
      x_1 = grid_ceiling_coords[i][0]
      x_2 = grid_ceiling_coords[i + 1][0]
      if y_2 > y_1:
        start_point = [x_1, y_1]
        end_point = [x_2, y_2]
        side_angle = np.degrees(np.arctan((y_2 - y_1)/(x_2 - x_1)))
        side_y_right.append([start_point, end_point, side_angle])
        side_y_right.sort(key = lambda side_y_right:side_y_right[0])
      else:
        start_point = [x_2, y_2]
        end_point = [x_1, y_1]
        side_angle = np.degrees(np.arctan((y_2 - y_1)/(x_2 - x_1)))
        side_y_left.append([start_point, end_point, side_angle])
        side_y_left.sort(key = lambda side_y_left:side_y_left[0])
 
  return side_y_left, side_y_right


#is a point inside the room?
def is_point_in_poly(point, polygon):
  #point is a (x,y) tuple
  #polygon is a lwpolygon
  #change lwpolyline to list of Vec2 vertices
  vertices_iter = polygon.vertices()
  room_vertices = list(vertices_iter)

  Vec_room = []
  for i in room_vertices:
    Vec_room.append(math.Vec2(i))

  point = math.Vec2(point)

  #-1 is outside poly, 0 is on line, 1 is inside poly.
  #Tolerance set to within 0.1 mm 
  return ezdxf.math.is_point_in_polygon_2d(point, Vec_room, 0.0001)


#get the intersect point
def intersect(line, polygon):
  #point is a (x,y) tuple
  #polygon is a lwpolygon
  #change lwpolyline to list of Vec2 vertices
  vertices_iter = polygon.vertices()
  room_vertices = list(vertices_iter)

  Vec_room = []
  for i in room_vertices:
    Vec_room.append(math.Vec2(i))

  Vec_line = []
  for j in line:
    Vec_line.append(math.Vec2(j)) 
  #-1 is outside poly, 0 is on line, 1 is inside poly. 
  #Tolerance set to within 0.1 mm 

  return ezdxf.math.intersect_polylines_2d(Vec_line, Vec_room, 0.0001)

#Define Center Points
def centre_setpoints(side_y_left):
  if side_y_left[0][2] != 0 or 90:
    centre_left = ((side_y_left[0][1][0] - side_y_left[0][0][0])/
                    2*np.cos(np.deg2rad(side_y_left[0][2])), \
                    side_y_left[0][0][1] + (side_y_left[0][1][1] - 
                    side_y_left[0][0][1])/2*np.sin(np.deg2rad(side_y_left[0][2])))
  else:
    centre_left = (side_y_left[0][0][0], side_y_left[0][0][1]
                 + (side_y_left[0][1][1] - side_y_left[0][0][1])/2)

  return centre_left


#Define Angle of grids
def get_angle(point, last_point):
  
  if point[0] == last_point[0]:
    angle = 90
  elif point[1] == last_point[1]:
    angle = 0
  else:
    angle = np.degrees(np.arctan((point[1] - last_point[1])
                       / (point[0] - last_point[0])))
  return round(angle, 4)

#Convert float to vector
def get_vec(point, side):
    #node = point
    vec_point = math.Vec2(point)
    vec_start_point = math.Vec2(side[0])
    vec_end_point = math.Vec2(side[1])

    return vec_point, vec_start_point, vec_end_point

#Funtion of defining points on lines
def point_on_line(node, side):
  vec_point, vec_start_point, vec_end_point = get_vec(node, side)
  return ezdxf.math.is_point_on_line_2d(vec_point, vec_start_point, 
                                        vec_end_point, 0.0001)

def closest_point(point, intersects):
  vec_point = math.Vec3(point)
  s = math.Vec3(intersects[0])
  e = math.Vec3(intersects[1])
  points_se = [s, e]
  closest_point = ezdxf.math.closest_point(vec_point, points_se)
  return math.Vec2(closest_point)

#line position on polygon
def is_line_in_poly(line, polygon):
  point_intersect = intersect(line, polygon)
  vertices_iter = polygon.vertices()
  room_vertices = list(vertices_iter)

  Vec_room = []
  for i in room_vertices:
    Vec_room.append(math.Vec2(i))
  
  point_s_nv = (round(line[1][0],3), round(line[1][1],3))
  point_e_nv = (round(line[0][0],3), round(line[0][1],3))
  point_s = math.Vec2(line[1])
  point_e = math.Vec2(line[0])
  
  point_s_check = ezdxf.math.is_point_in_polygon_2d(point_s, Vec_room, 0.001)
  point_e_check = ezdxf.math.is_point_in_polygon_2d(point_e, Vec_room, 0.001) 
 
  if point_s_check == 0 and point_e_nv in room_vertices:
    return "s_point is on border and e_point is on vertex"
  elif point_s_check == 0 and point_e_check == 0 and point_e_nv not in room_vertices:
    return "line on border"
  elif point_s_check == 1 and point_e_check == 0:
    point_x = point_intersect[0][0]
    point_y = point_intersect[0][1]
    point = (point_x, point_y)
    if point ==  point_e_check:
      return "s_point is inside and e_point is on border perpendicularly"
    elif point != point_e_check:
      return "s_point is inside and e_point is align on border"
  elif point_s_check == 0 and point_e_check == -1:
    return "s_point is on border and e_point is outside"
  elif point_s_check == 1 and point_e_check == -1:
    return "s_point is inside and e_point is is outside"
  elif point_s_check == 0 and point_e_check == 1:
    return "s_point is on border and e_point is is inside"
  else:
    return "line is inside"

#use flood-fill algorithm to draw lines from centre points

#start with seed point, draw lines out from there. 
#To achieve margin, use seed point = margin.

#global list of points within room. Starts empty
lines = []
visited_coords = []
points_side_y_left = []
points_side_y_right = []
points_side_x_top = []
points_side_x_bot = []
boundary_points = []
grid_points = []
#function to draw grids at grid size


def flood_fill(x, y, last_point, room, grid_ceiling_coords, coord):
  global visited_coords
  if coord in visited_coords:
    return
  visited_coords.append(coord)

  point = (x,y)
  #if point in boundary_points:
  #  return

  intersect_point = intersect((point, last_point), room)
  line_position = is_line_in_poly((point, last_point), room)
  
  side_x_bot, side_x_top = ceiling_x(grid_ceiling_coords)
  side_y_left, side_y_right = ceiling_y(grid_ceiling_coords)
  
  if len(intersect_point) > 1:
    point = closest_point(last_point, intersect_point)
    if point not in grid_points:
      grid_points.append(point)
      line = (point,last_point)
      lines.append(line)
      msp.add_lwpolyline([point, last_point],dxfattribs={'layer':'grid'}) 
      #define points on specified sides of borders      
      for i in range(len(side_y_left)):
        side = [side_y_left[i][0], side_y_left[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_left:
          points_side_y_left.append(point)
      for i in range(len(side_y_right)):
        side = [side_y_right[i][0], side_y_right[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_right:
          points_side_y_right.append(point)  
      for i in range(len(side_x_top)):
        side = [side_x_top[i][0], side_x_top[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_top:
          points_side_x_top.append(point)
      for i in range(len(side_x_bot)):
        side = [side_x_bot[i][0], side_x_bot[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_bot:
          points_side_x_bot.append(point)      
    return

  if is_point_in_poly(point, room) == 0:
    if line_position == "s_point is inside and e_point is align on border" or\
      line_position == "s_point is on border and e_point is on vertex":
      point_x = intersect_point[0][0]
      point_y = intersect_point[0][1]
      point = (point_x, point_y)
      if point not in grid_points:
        grid_points.append(point)
      line = (point, last_point)
      if line in lines or line[:: -1] in lines:
        return
      lines.append(line)
      msp.add_lwpolyline([point, last_point],dxfattribs={'layer':'grid'}) 
      
      for i in range(len(side_y_left)):
        side = [side_y_left[i][0], side_y_left[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_left:
          points_side_y_left.append(point)

      for i in range(len(side_y_right)):
        side = [side_y_right[i][0], side_y_right[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_right:
          points_side_y_right.append(point)  

      for i in range(len(side_x_top)):
        side = [side_x_top[i][0], side_x_top[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_top:
          points_side_x_top.append(point)

      for i in range(len(side_x_bot)):
        side = [side_x_bot[i][0], side_x_bot[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_bot:
          points_side_x_bot.append(point)
      
      
      return
    if line_position == "s_point is inside and e_point is on border perpendicularly":
      if point not in grid_points:
        grid_points.append(point)
      line = (point, last_point)
      if line in lines or line[:: -1] in lines:
        return
      lines.append(line)
      msp.add_lwpolyline([point, last_point],dxfattribs={'layer':'grid'})
      
      for i in range(len(side_y_left)):
        side = [side_y_left[i][0], side_y_left[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_left:
          points_side_y_left.append(point)

      for i in range(len(side_y_right)):
        side = [side_y_right[i][0], side_y_right[i][1]]
        if point_on_line(point, side) == True and point not in points_side_y_right:
          points_side_y_right.append(point)  

      for i in range(len(side_x_top)):
        side = [side_x_top[i][0], side_x_top[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_top:
          points_side_x_top.append(point)

      for i in range(len(side_x_bot)):
        side = [side_x_bot[i][0], side_x_bot[i][1]]
        if point_on_line(point, side) == True and point not in points_side_x_bot:
          points_side_x_bot.append(point)
      
      return
  #check point within room
  if is_point_in_poly(point, room) == -1:
    point_x = intersect_point[0][0]
    point_y = intersect_point[0][1]
    point = (point_x, point_y)
    if point not in grid_points:
      grid_points.append(point)
    line = (point, last_point)
    if line in lines or line[:: -1] in lines:
      return
    lines.append(line)   
    msp.add_lwpolyline([point, last_point],dxfattribs={'layer':'grid'})
    
    
    for i in range(len(side_y_left)):
      side = [side_y_left[i][0], side_y_left[i][1]]
      if point_on_line(point, side) == True and point not in points_side_y_left:
        points_side_y_left.append(point)

    for i in range(len(side_y_right)):
      side = [side_y_right[i][0], side_y_right[i][1]]
      if point_on_line(point, side) == True and point not in points_side_y_right:
        points_side_y_right.append(point)  

    for i in range(len(side_x_top)):
      side = [side_x_top[i][0], side_x_top[i][1]]
      if point_on_line(point, side) == True and point not in points_side_x_top:
        points_side_x_top.append(point)

    for i in range(len(side_x_bot)):
      side = [side_x_bot[i][0], side_x_bot[i][1]]
      if point_on_line(point, side) == True and point not in points_side_x_bot:
        points_side_x_bot.append(point)
    
    
    return
  
  line = (point, last_point)
  #define points in sides
 
  #draw line from last point to new point
  msp.add_lwpolyline([point, last_point],dxfattribs={'layer':'grid'})
  
  lines.append(line)
 
  #change point to last_point
  last_point = point

  grid_points.append(point)
  #check points around point
  #for centre left fill and margin

  flood_fill(x - grid_x_x, y - grid_x_y, last_point, room, grid_ceiling_coords,
             (coord[0] - 1, coord[1], 1)) 
  flood_fill(x + grid_y_x, y - grid_y_y, last_point, room, grid_ceiling_coords,
             (coord[0], coord[1] - 1, 2))
  flood_fill(x + grid_x_x, y + grid_x_y, last_point, room, grid_ceiling_coords,
             (coord[0] + 1,coord[1], 0))              
  flood_fill(x - grid_y_x, y + grid_y_y, last_point, room, grid_ceiling_coords,
             (coord[0], coord[1] + 1, 3))  
  

  return grid_points, boundary_points, lines, points_side_y_left, \
         points_side_y_right, points_side_x_top, points_side_x_bot


#Define points on edges of ceilings
side_y_left_ch_coord = []
side_y_right_ch_coord = []
side_x_top_ch_coord = []
side_x_bot_ch_coord = []

def get_channels_points_in_ceiling_edges(p_side_y_left, p_side_y_right,
                                         p_side_x_top, p_side_x_bot):
  for i in range(len(p_side_y_left)):
    x_coord = p_side_y_left[i][0]
    y_coord = p_side_y_left[i][1]
    x_y_coord = [x_coord, y_coord]
    side_y_left_ch_coord.append(x_y_coord)

  for i in range(len(p_side_y_right)):
    x_coord = p_side_y_right[i][0]
    y_coord = p_side_y_right[i][1]
    x_y_coord = [x_coord, y_coord]
    side_y_right_ch_coord.append(x_y_coord)

  for i in range(len(p_side_x_top)):
    x_coord = p_side_x_top[i][0]
    y_coord = p_side_x_top[i][1]
    x_y_coord = [x_coord, y_coord]
    side_x_top_ch_coord.append(x_y_coord)

  for i in range(len(p_side_x_bot)):
    x_coord = p_side_x_bot[i][0]
    y_coord = p_side_x_bot[i][1]
    x_y_coord = [x_coord,  y_coord]
    side_x_bot_ch_coord.append(x_y_coord)

  return side_y_left_ch_coord, side_y_right_ch_coord, \
         side_x_top_ch_coord, side_x_bot_ch_coord

#Define the channels coordinates

channels_x = []
channels_y = []
start_end_point = []

grid_x_angle = grid_angle
if grid_x_angle == 0:
  grid_y_angle = grid_x_angle + 90
elif grid_x_angle > 0 and grid_x_angle < 90:
  grid_y_angle = grid_x_angle - 90
else:
  print("Please put angle between 0 to 90 degree")

def get_channels_coord(points_side_y_left, points_side_y_right, 
                       points_side_x_top, points_side_x_bot):
  
  side_y_left_ch_coord, \
  side_y_right_ch_coord, \
  side_x_top_ch_coord, \
  side_x_bot_ch_coord = get_channels_points_in_ceiling_edges(
                              points_side_y_left,
                              points_side_y_right,
                              points_side_x_top, 
                              points_side_x_bot
                              )
  
  for i in side_y_left_ch_coord:
    for j in itertools.chain(side_y_right_ch_coord, side_x_top_ch_coord, 
                            side_x_bot_ch_coord):
      start_point = i
      end_point = j
      start_end_point = [start_point, end_point]
      if (get_angle(start_point, end_point) == grid_x_angle and 
          start_end_point not in channels_x and 
          start_end_point[::-1] not in channels_x):
        channels_x.append([start_point, end_point])
      elif (get_angle(start_point, end_point) == grid_y_angle and 
            start_end_point not in channels_y and 
            start_end_point[::-1] not in channels_y):
        channels_y.append([start_point, end_point])
      else:
        pass

  for i in side_y_right_ch_coord:
    start_point = i
    for j in itertools.chain(side_y_left_ch_coord, side_x_top_ch_coord, 
                            side_x_bot_ch_coord):
      end_point = j
      start_end_point = [start_point, end_point]
      if (get_angle(start_point, end_point) == grid_x_angle and
          start_end_point not in channels_x and
          start_end_point[::-1] not in channels_x):
        channels_x.append([start_point, end_point])
      elif (get_angle(start_point, end_point) == grid_y_angle and
            start_end_point not in channels_y and
            start_end_point[::-1] not in channels_y):
        channels_y.append([start_point, end_point])
      else:
        pass    

  for i in side_x_bot_ch_coord:
    start_point = i
    for j in itertools.chain(side_y_left_ch_coord, side_x_top_ch_coord, 
                            side_y_right_ch_coord):
      end_point = j
      start_end_point = [start_point, end_point]
      if (get_angle(start_point, end_point) == grid_x_angle and
      start_end_point not in channels_x and
      start_end_point[::-1] not in channels_x):
        channels_x.append([start_point, end_point])
      elif (get_angle(start_point, end_point) == grid_y_angle and
            start_end_point not in channels_y and
            start_end_point[::-1] not in channels_y):
        channels_y.append([start_point, end_point])
      else:
        pass  


  for i in side_x_top_ch_coord:
    start_point = i
    for j in itertools.chain(side_y_left_ch_coord, side_x_bot_ch_coord, 
                            side_y_right_ch_coord):
      end_point = j
      start_end_point = [start_point, end_point]
      if (get_angle(start_point, end_point) == grid_x_angle and
          start_end_point not in channels_x and
          start_end_point[::-1] not in channels_x):
        channels_x.append([start_point, end_point])
      elif (get_angle(start_point, end_point) == grid_y_angle and
            start_end_point not in channels_y and
            start_end_point[::-1] not in channels_y):
        channels_y.append([start_point, end_point])
      else:
        pass 

  return channels_x, channels_y


channels_x, channels_y = get_channels_coord(points_side_y_left, 
                                            points_side_y_right, 
                                            points_side_x_top, 
                                            points_side_x_bot)
