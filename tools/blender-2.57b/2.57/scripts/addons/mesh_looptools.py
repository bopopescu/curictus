# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name': "LoopTools",
    'author': "Bart Crouch",
    'version': (3, 2, 0),
    'blender': (2, 5, 7),
    'api': 35979,
    'location': "View3D > Toolbar and View3D > Specials (W-key)",
    'warning': "",
    'description': "Mesh modelling toolkit. Several tools to aid modelling",
    'wiki_url': "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/Modeling/LoopTools",
    'tracker_url': "http://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=26189",
    'category': 'Mesh'}


import bpy
import mathutils
import math


##########################################
####### General functions ################
##########################################


# used by all tools to improve speed on reruns
looptools_cache = {}


# force a full recalculation next time
def cache_delete(tool):
    if tool in looptools_cache:
        del looptools_cache[tool]


# check cache for stored information
def cache_read(tool, object, mesh, input_method, boundaries):
    # current tool not cached yet
    if tool not in looptools_cache:
        return(False, False, False, False, False)
    # check if selected object didn't change
    if object.name != looptools_cache[tool]["object"]:
        return(False, False, False, False, False)
    # check if input didn't change
    if input_method != looptools_cache[tool]["input_method"]:
        return(False, False, False, False, False)
    if boundaries != looptools_cache[tool]["boundaries"]:
        return(False, False, False, False, False)
    modifiers = [mod.name for mod in object.modifiers if mod.show_viewport \
        and mod.type == 'MIRROR']
    if modifiers != looptools_cache[tool]["modifiers"]:
        return(False, False, False, False, False)
    input = [v.index for v in mesh.vertices if v.select and not v.hide]
    if input != looptools_cache[tool]["input"]:
        return(False, False, False, False, False)
    # reading values
    single_loops = looptools_cache[tool]["single_loops"]
    loops = looptools_cache[tool]["loops"]
    derived = looptools_cache[tool]["derived"]
    mapping = looptools_cache[tool]["mapping"]
    
    return(True, single_loops, loops, derived, mapping)


# store information in the cache
def cache_write(tool, object, mesh, input_method, boundaries, single_loops,
loops, derived, mapping):
    # clear cache of current tool
    if tool in looptools_cache:
        del looptools_cache[tool]
    # prepare values to be saved to cache
    input = [v.index for v in mesh.vertices if v.select and not v.hide]
    modifiers = [mod.name for mod in object.modifiers if mod.show_viewport \
        and mod.type == 'MIRROR']
    # update cache
    looptools_cache[tool] = {"input": input, "object": object.name,
        "input_method": input_method, "boundaries": boundaries,
        "single_loops": single_loops, "loops": loops,
        "derived": derived, "mapping": mapping, "modifiers": modifiers}


# calculates natural cubic splines through all given knots
def calculate_cubic_splines(mesh_mod, tknots, knots):
    # hack for circular loops
    if knots[0] == knots[-1] and len(knots) > 1:
        circular = True
        k_new1 = []
        for k in range(-1, -5, -1):
            if k - 1 < -len(knots):
                k += len(knots)
            k_new1.append(knots[k-1])
        k_new2 = []
        for k in range(4):
            if k + 1 > len(knots) - 1:
                k -= len(knots)
            k_new2.append(knots[k+1])
        for k in k_new1:
            knots.insert(0, k)
        for k in k_new2:
            knots.append(k)
        t_new1 = []
        total1 = 0
        for t in range(-1, -5, -1):
            if t - 1 < -len(tknots):
                t += len(tknots)
            total1 += tknots[t] - tknots[t-1]
            t_new1.append(tknots[0] - total1)
        t_new2 = []
        total2 = 0
        for t in range(4):
            if t + 1 > len(tknots) - 1:
                t -= len(tknots)
            total2 += tknots[t+1] - tknots[t]
            t_new2.append(tknots[-1] + total2)
        for t in t_new1:
            tknots.insert(0, t)
        for t in t_new2:
            tknots.append(t)
    else:
        circular = False
    # end of hack
    
    n = len(knots)
    if n < 2:
        return False
    x = tknots[:]
    locs = [mesh_mod.vertices[k].co[:] for k in knots]
    result = []
    for j in range(3):
        a = []
        for i in locs:
            a.append(i[j])
        h = []
        for i in range(n-1):
            if x[i+1] - x[i] == 0:
                h.append(1e-8)
            else:
                h.append(x[i+1] - x[i])
        q = [False]
        for i in range(1, n-1):
            q.append(3/h[i]*(a[i+1]-a[i]) - 3/h[i-1]*(a[i]-a[i-1]))
        l = [1.0]
        u = [0.0]
        z = [0.0]
        for i in range(1, n-1):
            l.append(2*(x[i+1]-x[i-1]) - h[i-1]*u[i-1])
            if l[i] == 0:
                l[i] = 1e-8
            u.append(h[i] / l[i])
            z.append((q[i] - h[i-1] * z[i-1]) / l[i])
        l.append(1.0)
        z.append(0.0)
        b = [False for i in range(n-1)]
        c = [False for i in range(n)]
        d = [False for i in range(n-1)]
        c[n-1] = 0.0
        for i in range(n-2, -1, -1):
            c[i] = z[i] - u[i]*c[i+1]
            b[i] = (a[i+1]-a[i])/h[i] - h[i]*(c[i+1]+2*c[i])/3
            d[i] = (c[i+1]-c[i]) / (3*h[i])
        for i in range(n-1):
            result.append([a[i], b[i], c[i], d[i], x[i]])
    splines = []
    for i in range(len(knots)-1):
        splines.append([result[i], result[i+n-1], result[i+(n-1)*2]])
    if circular: # cleaning up after hack
        knots = knots[4:-4]
        tknots = tknots[4:-4]
    
    return(splines)


# calculates linear splines through all given knots
def calculate_linear_splines(mesh_mod, tknots, knots):
    splines = []
    for i in range(len(knots)-1):
        a = mesh_mod.vertices[knots[i]].co
        b = mesh_mod.vertices[knots[i+1]].co
        d = b-a
        t = tknots[i]
        u = tknots[i+1]-t
        splines.append([a, d, t, u]) # [locStart, locDif, tStart, tDif]
    
    return(splines)


# calculate a best-fit plane to the given vertices
def calculate_plane(mesh_mod, loop, method="best_fit", object=False):
    # getting the vertex locations
    locs = [mathutils.Vector(mesh_mod.vertices[v].co[:]) for v in loop[0]]
    
    # calculating the center of masss
    com = mathutils.Vector()
    for loc in locs:
        com += loc
    com /= len(locs)
    x, y, z = com
    
    if method == 'best_fit':
        # creating the covariance matrix
        mat = mathutils.Matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]])
        for loc in locs:
            mat[0][0] += (loc[0]-x)**2
            mat[0][1] += (loc[0]-x)*(loc[1]-y)
            mat[0][2] += (loc[0]-x)*(loc[2]-z)
            mat[1][0] += (loc[1]-y)*(loc[0]-x)
            mat[1][1] += (loc[1]-y)**2
            mat[1][2] += (loc[1]-y)*(loc[2]-z)
            mat[2][0] += (loc[2]-z)*(loc[0]-x)
            mat[2][1] += (loc[2]-z)*(loc[1]-y)
            mat[2][2] += (loc[2]-z)**2
        
        # calculating the normal to the plane
        normal = False
        try:
            mat.invert()
        except:
            if sum(mat[0]) == 0.0:
                normal = mathutils.Vector([1.0, 0.0, 0.0])
            elif sum(mat[1]) == 0.0:
                normal = mathutils.Vector([0.0, 1.0, 0.0])
            elif sum(mat[2]) == 0.0:
                normal = mathutils.Vector([0.0, 0.0, 1.0])
        if not normal:
            itermax = 500
            iter = 0
            vec = mathutils.Vector([1.0, 1.0, 1.0])
            vec2 = (vec*mat)/(vec*mat).length
            while vec != vec2 and iter<itermax:
                iter += 1
                vec = vec2
                vec2 = (vec*mat)/(vec*mat).length
            normal = vec2
    
    elif method == 'normal':
        # averaging the vertex normals
        v_normals = [mesh_mod.vertices[v].normal for v in loop[0]]
        normal = mathutils.Vector()
        for v_normal in v_normals:
            normal += v_normal
        normal /= len(v_normals)
        normal.normalize()
        
    elif method == 'view':
        # calculate view normal
        rotation = bpy.context.space_data.region_3d.view_matrix.to_3x3().\
            inverted()
        normal = mathutils.Vector([0.0, 0.0, 1.0]) * rotation
        if object:
            normal *= object.matrix_world.inverted().to_euler().to_matrix()
    
    return(com, normal)


# calculate splines based on given interpolation method (controller function)
def calculate_splines(interpolation, mesh_mod, tknots, knots):
    if interpolation == 'cubic':
        splines = calculate_cubic_splines(mesh_mod, tknots, knots[:])
    else: # interpolations == 'linear'
        splines = calculate_linear_splines(mesh_mod, tknots, knots[:])
    
    return(splines)


# check loops and only return valid ones
def check_loops(loops, mapping, mesh_mod):
    valid_loops = []
    for loop, circular in loops:
        # loop needs to have at least 3 vertices
        if len(loop) < 3:
            continue
        # loop needs at least 1 vertex in the original, non-mirrored mesh
        if mapping:
            all_virtual = True
            for vert in loop:
                if mapping[vert] > -1:
                    all_virtual = False
                    break
            if all_virtual:
                continue
        # vertices can not all be at the same location
        stacked = True
        for i in range(len(loop) - 1):
            if (mesh_mod.vertices[loop[i]].co - \
            mesh_mod.vertices[loop[i+1]].co).length > 1e-6:
                stacked = False
                break
        if stacked:
            continue    
        # passed all tests, loop is valid
        valid_loops.append([loop, circular])
    
    return(valid_loops)


# input: mesh, output: dict with the edge-key as key and face-index as value
def dict_edge_faces(mesh):
    edge_faces = dict([[edge.key, []] for edge in mesh.edges if not edge.hide])
    for face in mesh.faces:
        if face.hide:
            continue
        for key in face.edge_keys:
            edge_faces[key].append(face.index)
    
    return(edge_faces)

# input: mesh (edge-faces optional), output: dict with face-face connections
def dict_face_faces(mesh, edge_faces=False):
    if not edge_faces:
        edge_faces = dict_edge_faces(mesh)
    
    connected_faces = dict([[face.index, []] for face in mesh.faces if \
        not face.hide])
    for face in mesh.faces:
        if face.hide:
            continue
        for edge_key in face.edge_keys:
            for connected_face in edge_faces[edge_key]:
                if connected_face == face.index:
                    continue
                connected_faces[face.index].append(connected_face)
    
    return(connected_faces)


# input: mesh, output: dict with the vert index as key and edge-keys as value
def dict_vert_edges(mesh):
    vert_edges = dict([[v.index, []] for v in mesh.vertices if not v.hide])
    for edge in mesh.edges:
        if edge.hide:
            continue
        for vert in edge.key:
            vert_edges[vert].append(edge.key)
    
    return(vert_edges)


# input: mesh, output: dict with the vert index as key and face index as value
def dict_vert_faces(mesh):
    vert_faces = dict([[v.index, []] for v in mesh.vertices if not v.hide])
    for face in mesh.faces:
        if not face.hide:
            for vert in face.vertices:
                vert_faces[vert].append(face.index)
                
    return(vert_faces)


# input: list of edge-keys, output: dictionary with vertex-vertex connections
def dict_vert_verts(edge_keys):
    # create connection data
    vert_verts = {}
    for ek in edge_keys:
        for i in range(2):
            if ek[i] in vert_verts:
                vert_verts[ek[i]].append(ek[1-i])
            else:
                vert_verts[ek[i]] = [ek[1-i]]
    
    return(vert_verts)


# calculate input loops
def get_connected_input(object, mesh, scene, input):
    # get mesh with modifiers applied
    derived, mesh_mod = get_derived_mesh(object, mesh, scene)
    
    # calculate selected loops
    edge_keys = [edge.key for edge in mesh_mod.edges if \
        edge.select and not edge.hide]
    loops = get_connected_selections(edge_keys)
    
    # if only selected loops are needed, we're done
    if input == 'selected':
        return(derived, mesh_mod, loops)
    # elif input == 'all':    
    loops = get_parallel_loops(mesh_mod, loops)
    
    return(derived, mesh_mod, loops)


# sorts all edge-keys into a list of loops
def get_connected_selections(edge_keys):
    # create connection data
    vert_verts = dict_vert_verts(edge_keys)
    
    # find loops consisting of connected selected edges
    loops = []
    while len(vert_verts) > 0:
        loop = [iter(vert_verts.keys()).__next__()]
        growing = True
        flipped = False
        
        # extend loop
        while growing:
            # no more connection data for current vertex
            if loop[-1] not in vert_verts:
                if not flipped:
                    loop.reverse()
                    flipped = True
                else:
                    growing = False
            else:
                extended = False
                for i, next_vert in enumerate(vert_verts[loop[-1]]):
                    if next_vert not in loop:
                        vert_verts[loop[-1]].pop(i)
                        if len(vert_verts[loop[-1]]) == 0:
                            del vert_verts[loop[-1]]
                        # remove connection both ways
                        if next_vert in vert_verts:
                            if len(vert_verts[next_vert]) == 1:
                                del vert_verts[next_vert]
                            else:
                                vert_verts[next_vert].remove(loop[-1])
                        loop.append(next_vert)
                        extended = True
                        break
                if not extended:
                    # found one end of the loop, continue with next
                    if not flipped:
                        loop.reverse()
                        flipped = True
                    # found both ends of the loop, stop growing
                    else:
                        growing = False
        
        # check if loop is circular
        if loop[0] in vert_verts:
            if loop[-1] in vert_verts[loop[0]]:
                # is circular
                if len(vert_verts[loop[0]]) == 1:
                    del vert_verts[loop[0]]
                else:
                    vert_verts[loop[0]].remove(loop[-1])
                if len(vert_verts[loop[-1]]) == 1:
                    del vert_verts[loop[-1]]
                else:
                    vert_verts[loop[-1]].remove(loop[0])
                loop = [loop, True]
            else:
                # not circular
                loop = [loop, False]
        else:
            # not circular
            loop = [loop, False]
        
        loops.append(loop)
    
    return(loops)


# get the derived mesh data, if there is a mirror modifier
def get_derived_mesh(object, mesh, scene):
    # check for mirror modifiers
    if 'MIRROR' in [mod.type for mod in object.modifiers if mod.show_viewport]:
        derived = True
        # disable other modifiers
        show_viewport = [mod.name for mod in object.modifiers if \
            mod.show_viewport]
        for mod in object.modifiers:
            if mod.type != 'MIRROR':
                mod.show_viewport = False
        # get derived mesh
        mesh_mod = object.to_mesh(scene, True, 'PREVIEW')
        # re-enable other modifiers
        for mod_name in show_viewport:
            object.modifiers[mod_name].show_viewport = True
    # no mirror modifiers, so no derived mesh necessary
    else:
        derived = False
        mesh_mod = mesh
    
    return(derived, mesh_mod)


# return a mapping of derived indices to indices
def get_mapping(derived, mesh, mesh_mod, single_vertices, full_search, loops):
    if not derived:
        return(False)
    
    if full_search:
        verts = [v for v in mesh.vertices if not v.hide]
    else:
        verts = [v for v in mesh.vertices if v.select and not v.hide]
    
    # non-selected vertices around single vertices also need to be mapped
    if single_vertices:
        mapping = dict([[vert, -1] for vert in single_vertices])
        verts_mod = [mesh_mod.vertices[vert] for vert in single_vertices]
        for v in verts:
            for v_mod in verts_mod:
                if (v.co - v_mod.co).length < 1e-6:
                    mapping[v_mod.index] = v.index
                    break
        real_singles = [v_real for v_real in mapping.values() if v_real>-1]
        
        verts_indices = [vert.index for vert in verts]
        for face in [face for face in mesh.faces if not face.select \
        and not face.hide]:
            for vert in face.vertices:
                if vert in real_singles:
                    for v in face.vertices:
                        if not v in verts_indices:
                            if mesh.vertices[v] not in verts:
                                verts.append(mesh.vertices[v])
                    break
    
    # create mapping of derived indices to indices
    mapping = dict([[vert, -1] for loop in loops for vert in loop[0]])
    if single_vertices:
        for single in single_vertices:
            mapping[single] = -1
    verts_mod = [mesh_mod.vertices[i] for i in mapping.keys()]
    for v in verts:
        for v_mod in verts_mod:
            if (v.co - v_mod.co).length < 1e-6:
                mapping[v_mod.index] = v.index
                verts_mod.remove(v_mod)
                break
    
    return(mapping)


# returns a list of all loops parallel to the input, input included
def get_parallel_loops(mesh_mod, loops):
    # get required dictionaries
    edge_faces = dict_edge_faces(mesh_mod)
    connected_faces = dict_face_faces(mesh_mod, edge_faces)
    # turn vertex loops into edge loops
    edgeloops = []
    for loop in loops:
        edgeloop = [[sorted([loop[0][i], loop[0][i+1]]) for i in \
            range(len(loop[0])-1)], loop[1]]
        if loop[1]: # circular
            edgeloop[0].append(sorted([loop[0][-1], loop[0][0]]))
        edgeloops.append(edgeloop[:])
    # variables to keep track while iterating
    all_edgeloops = []
    has_branches = False
    
    for loop in edgeloops:
        # initialise with original loop
        all_edgeloops.append(loop[0])
        newloops = [loop[0]]
        verts_used = []
        for edge in loop[0]:
            if edge[0] not in verts_used:
                verts_used.append(edge[0])
            if edge[1] not in verts_used:
                verts_used.append(edge[1])
        
        # find parallel loops
        while len(newloops) > 0:
            side_a = []
            side_b = []
            for i in newloops[-1]:
                i = tuple(i)
                forbidden_side = False
                if not i in edge_faces:
                    # weird input with branches
                    has_branches = True
                    break
                for face in edge_faces[i]:
                    if len(side_a) == 0 and forbidden_side != "a":
                        side_a.append(face)
                        if forbidden_side:
                            break
                        forbidden_side = "a"
                        continue
                    elif side_a[-1] in connected_faces[face] and \
                    forbidden_side != "a":
                        side_a.append(face)
                        if forbidden_side:
                            break
                        forbidden_side = "a"
                        continue
                    if len(side_b) == 0 and forbidden_side != "b":
                        side_b.append(face)
                        if forbidden_side:
                            break
                        forbidden_side = "b"
                        continue
                    elif side_b[-1] in connected_faces[face] and \
                    forbidden_side != "b":
                        side_b.append(face)
                        if forbidden_side:
                            break
                        forbidden_side = "b"
                        continue
            
            if has_branches:
                # weird input with branches
                break
            
            newloops.pop(-1)
            sides = []
            if side_a:
                sides.append(side_a)
            if side_b:
                sides.append(side_b)
            
            for side in sides:
                extraloop = []
                for fi in side:
                    for key in mesh_mod.faces[fi].edge_keys:
                        if key[0] not in verts_used and key[1] not in \
                        verts_used:
                            extraloop.append(key)
                            break
                if extraloop:
                    for key in extraloop:
                        for new_vert in key:
                            if new_vert not in verts_used:
                                verts_used.append(new_vert)
                    newloops.append(extraloop)
                    all_edgeloops.append(extraloop)
    
    # input contains branches, only return selected loop
    if has_branches:
        return(loops)
    
    # change edgeloops into normal loops
    loops = []
    for edgeloop in all_edgeloops:
        loop = []
        # grow loop by comparing vertices between consecutive edge-keys
        for i in range(len(edgeloop)-1):
            for vert in range(2):
                if edgeloop[i][vert] in edgeloop[i+1]:
                    loop.append(edgeloop[i][vert])
                    break
        if loop:
            # add starting vertex
            for vert in range(2):
                if edgeloop[0][vert] != loop[0]:
                    loop = [edgeloop[0][vert]] + loop
                    break
            # add ending vertex
            for vert in range(2):
                if edgeloop[-1][vert] != loop[-1]:
                    loop.append(edgeloop[-1][vert])
                    break
            # check if loop is circular
            if loop[0] == loop[-1]:
                circular = True
                loop = loop[:-1]
            else:
                circular = False
        loops.append([loop, circular])
    
    return(loops)


# gather initial data
def initialise():
    global_undo = bpy.context.user_preferences.edit.use_global_undo
    bpy.context.user_preferences.edit.use_global_undo = False
    bpy.ops.object.mode_set(mode='OBJECT')
    object = bpy.context.active_object
    mesh = bpy.context.active_object.data
    
    return(global_undo, object, mesh)


# move the vertices to their new locations
def move_verts(mesh, mapping, move, influence):
    for loop in move:
        for index, loc in loop:
            if mapping:
                if mapping[index] == -1:
                    continue
                else:
                    index = mapping[index]
            if influence >= 0:
                mesh.vertices[index].co = loc*(influence/100) + \
                    mesh.vertices[index].co*((100-influence)/100)
            else:
                mesh.vertices[index].co = loc


# load custom tool settings 
def settings_load(self):
    lt = bpy.context.window_manager.looptools
    tool = self.name.split()[0].lower()
    keys = self.as_keywords().keys()
    for key in keys:
        setattr(self, key, getattr(lt, tool + "_" + key))


# store custom tool settings
def settings_write(self):
    lt = bpy.context.window_manager.looptools
    tool = self.name.split()[0].lower()
    keys = self.as_keywords().keys()
    for key in keys:
        setattr(lt, tool + "_" + key, getattr(self, key))


# clean up and set settings back to original state
def terminate(global_undo):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.user_preferences.edit.use_global_undo = global_undo


##########################################
####### Bridge functions #################
##########################################

# calculate a cubic spline through the middle section of 4 given coordinates
def bridge_calculate_cubic_spline(mesh, coordinates):
    result = []
    x = [0, 1, 2, 3]
    
    for j in range(3):
        a = []
        for i in coordinates:
            a.append(float(i[j]))
        h = []
        for i in range(3):
            h.append(x[i+1]-x[i])
        q = [False]
        for i in range(1,3):
            q.append(3.0/h[i]*(a[i+1]-a[i])-3.0/h[i-1]*(a[i]-a[i-1]))
        l = [1.0]
        u = [0.0]
        z = [0.0]
        for i in range(1,3):
            l.append(2.0*(x[i+1]-x[i-1])-h[i-1]*u[i-1])
            u.append(h[i]/l[i])
            z.append((q[i]-h[i-1]*z[i-1])/l[i])
        l.append(1.0)
        z.append(0.0)
        b = [False for i in range(3)]
        c = [False for i in range(4)]
        d = [False for i in range(3)]
        c[3] = 0.0
        for i in range(2,-1,-1):
            c[i] = z[i]-u[i]*c[i+1]
            b[i] = (a[i+1]-a[i])/h[i]-h[i]*(c[i+1]+2.0*c[i])/3.0
            d[i] = (c[i+1]-c[i])/(3.0*h[i])
        for i in range(3):
            result.append([a[i], b[i], c[i], d[i], x[i]])
    spline = [result[1], result[4], result[7]]

    return(spline)


# return a list with new vertex location vectors, a list with face vertex 
# integers, and the highest vertex integer in the virtual mesh
def bridge_calculate_geometry(mesh, lines, vertex_normals, segments,
interpolation, cubic_strength, min_width, max_vert_index):
    new_verts = []
    faces = []
    
    # calculate location based on interpolation method
    def get_location(line, segment, splines):
        v1 = mesh.vertices[lines[line][0]].co
        v2 = mesh.vertices[lines[line][1]].co
        if interpolation == 'linear':
            return v1 + (segment/segments) * (v2-v1)
        else: # interpolation == 'cubic'
            m = (segment/segments)
            ax,bx,cx,dx,tx = splines[line][0]
            x = ax+bx*m+cx*m**2+dx*m**3
            ay,by,cy,dy,ty = splines[line][1]
            y = ay+by*m+cy*m**2+dy*m**3
            az,bz,cz,dz,tz = splines[line][2]
            z = az+bz*m+cz*m**2+dz*m**3
            return mathutils.Vector([x,y,z])
        
    # no interpolation needed
    if segments == 1:
        for i, line in enumerate(lines):
            if i < len(lines)-1:
                faces.append([line[0], lines[i+1][0], lines[i+1][1], line[1]])
    # more than 1 segment, interpolate
    else:
        # calculate splines (if necessary) once, so no recalculations needed
        if interpolation == 'cubic':
            splines = []
            for line in lines:
                v1 = mesh.vertices[line[0]].co
                v2 = mesh.vertices[line[1]].co
                size = (v2-v1).length * cubic_strength
                splines.append(bridge_calculate_cubic_spline(mesh,
                    [v1+size*vertex_normals[line[0]], v1, v2,
                    v2+size*vertex_normals[line[1]]]))
        else:
            splines = False
        
        # create starting situation
        virtual_width = [(mathutils.Vector(mesh.vertices[lines[i][0]].co) - \
            mathutils.Vector(mesh.vertices[lines[i+1][0]].co)).length for i \
            in range(len(lines)-1)]
        new_verts = [get_location(0, seg, splines) for seg in range(1,
            segments)]
        first_line_indices = [i for i in range(max_vert_index+1,
            max_vert_index+segments)]
        
        prev_verts = new_verts[:] # vertex locations of verts on previous line
        prev_vert_indices = first_line_indices[:]
        max_vert_index += segments - 1 # highest vertex index in virtual mesh
        next_verts = [] # vertex locations of verts on current line
        next_vert_indices = []
        
        for i, line in enumerate(lines):
            if i < len(lines)-1:
                v1 = line[0]
                v2 = lines[i+1][0]
                end_face = True
                for seg in range(1, segments):
                    loc1 = prev_verts[seg-1]
                    loc2 = get_location(i+1, seg, splines)
                    if (loc1-loc2).length < (min_width/100)*virtual_width[i] \
                    and line[1]==lines[i+1][1]:
                        # triangle, no new vertex
                        faces.append([v1, v2, prev_vert_indices[seg-1],
                            prev_vert_indices[seg-1]])
                        next_verts += prev_verts[seg-1:]
                        next_vert_indices += prev_vert_indices[seg-1:]
                        end_face = False
                        break
                    else:
                        if i == len(lines)-2 and lines[0] == lines[-1]:
                            # quad with first line, no new vertex
                            faces.append([v1, v2, first_line_indices[seg-1],
                                prev_vert_indices[seg-1]])
                            v2 = first_line_indices[seg-1]
                            v1 = prev_vert_indices[seg-1]
                        else:
                            # quad, add new vertex
                            max_vert_index += 1
                            faces.append([v1, v2, max_vert_index,
                                prev_vert_indices[seg-1]])
                            v2 = max_vert_index
                            v1 = prev_vert_indices[seg-1]
                            new_verts.append(loc2)
                            next_verts.append(loc2)
                            next_vert_indices.append(max_vert_index)
                if end_face:
                    faces.append([v1, v2, lines[i+1][1], line[1]])
                
                prev_verts = next_verts[:]
                prev_vert_indices = next_vert_indices[:]
                next_verts = []
                next_vert_indices = []
    
    return(new_verts, faces, max_vert_index)


# calculate lines (list of lists, vertex indices) that are used for bridging
def bridge_calculate_lines(mesh, loops, mode, twist, reverse):
    lines = []
    loop1, loop2 = [i[0] for i in loops]
    loop1_circular, loop2_circular = [i[1] for i in loops]
    circular = loop1_circular or loop2_circular
    circle_full = False
    
    # calculate loop centers
    centers = []
    for loop in [loop1, loop2]:
        center = mathutils.Vector([0,0,0])
        for vertex in loop:
            center += mesh.vertices[vertex].co
        center /= len(loop)
        centers.append(center)
    for i, loop in enumerate([loop1, loop2]):
        for vertex in loop:
            if mesh.vertices[vertex].co == centers[i]:
                # prevent zero-length vectors in angle comparisons
                centers[i] += mathutils.Vector([0.01, 0, 0])
                break
    center1, center2 = centers
    
    # calculate the normals of the virtual planes that the loops are on
    normals = []
    normal_plurity = False
    for i, loop in enumerate([loop1, loop2]):
        # covariance matrix
        mat = mathutils.Matrix(((0.0, 0.0, 0.0), (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0)))
        x, y, z = centers[i]
        for loc in [mesh.vertices[vertex].co for vertex in loop]:
            mat[0][0] += (loc[0]-x)**2
            mat[0][1] += (loc[0]-x)*(loc[1]-y)
            mat[0][2] += (loc[0]-x)*(loc[2]-z)
            mat[1][0] += (loc[1]-y)*(loc[0]-x)
            mat[1][1] += (loc[1]-y)**2
            mat[1][2] += (loc[1]-y)*(loc[2]-z)
            mat[2][0] += (loc[2]-z)*(loc[0]-x)
            mat[2][1] += (loc[2]-z)*(loc[1]-y)
            mat[2][2] += (loc[2]-z)**2
        # plane normal
        normal = False
        if sum(mat[0]) < 1e-6 or sum(mat[1]) < 1e-6 or sum(mat[2]) < 1e-6:
            normal_plurity = True
        try:
            mat.invert()
        except:
            if sum(mat[0]) == 0:
                normal = mathutils.Vector([1.0, 0.0, 0.0])
            elif sum(mat[1]) == 0:
                normal = mathutils.Vector([0.0, 1.0, 0.0])
            elif sum(mat[2]) == 0:
                normal = mathutils.Vector([0.0, 0.0, 1.0])
        if not normal:
            itermax = 500
            iter = 0
            vec = mathutils.Vector([1.0, 1.0, 1.0])
            vec2 = (vec*mat)/(vec*mat).length
            while vec != vec2 and iter<itermax:
                iter+=1
                vec = vec2
                vec2 = (vec*mat)/(vec*mat).length
            normal = vec2
        normals.append(normal)
    # have plane normals face in the same direction (maximum angle: 90 degrees)
    if ((center1 + normals[0]) - center2).length < \
    ((center1 - normals[0]) - center2).length:
        normals[0].negate()
    if ((center2 + normals[1]) - center1).length > \
    ((center2 - normals[1]) - center1).length:
        normals[1].negate()
    
    # rotation matrix, representing the difference between the plane normals
    axis = normals[0].cross(normals[1])
    axis = mathutils.Vector([loc if abs(loc) > 1e-8 else 0 for loc in axis])
    if axis.angle(mathutils.Vector([0, 0, 1]), 0) > 1.5707964:
        axis.negate()
    angle = normals[0].dot(normals[1])
    rotation_matrix = mathutils.Matrix.Rotation(angle, 4, axis)
    
    # if circular, rotate loops so they are aligned
    if circular:
        # make sure loop1 is the circular one (or both are circular)
        if loop2_circular and not loop1_circular:
            loop1_circular, loop2_circular = True, False
            loop1, loop2 = loop2, loop1
        
        # match start vertex of loop1 with loop2
        target_vector = mesh.vertices[loop2[0]].co - center2
        dif_angles = [[((mesh.vertices[vertex].co - center1) * \
            rotation_matrix).angle(target_vector, 0), False, i] for \
            i, vertex in enumerate(loop1)]
        dif_angles.sort()
        if len(loop1) != len(loop2):
            angle_limit = dif_angles[0][0] * 1.2 # 20% margin
            dif_angles = [[(mesh.vertices[loop2[0]].co - \
                mesh.vertices[loop1[index]].co).length, angle, index] for \
                angle, distance, index in dif_angles if angle <= angle_limit]
            dif_angles.sort()
        loop1 = loop1[dif_angles[0][2]:] + loop1[:dif_angles[0][2]]
    
    # have both loops face the same way
    if normal_plurity and not circular:
        second_to_first, second_to_second, second_to_last = \
            [(mesh.vertices[loop1[1]].co - center1).\
            angle(mesh.vertices[loop2[i]].co - center2) for i in [0, 1, -1]]
        last_to_first, last_to_second = [(mesh.vertices[loop1[-1]].co - \
            center1).angle(mesh.vertices[loop2[i]].co - center2) for \
            i in [0, 1]]
        if (min(last_to_first, last_to_second)*1.1 < min(second_to_first, \
        second_to_second)) or (loop2_circular and second_to_last*1.1 < \
        min(second_to_first, second_to_second)):
            loop1.reverse()
            if circular:
                loop1 = [loop1[-1]] + loop1[:-1]
    else:
        angle = (mesh.vertices[loop1[0]].co - center1).\
            cross(mesh.vertices[loop1[1]].co - center1).angle(normals[0], 0)
        target_angle = (mesh.vertices[loop2[0]].co - center2).\
            cross(mesh.vertices[loop2[1]].co - center2).angle(normals[1], 0)
        limit = 1.5707964 # 0.5*pi, 90 degrees
        if not ((angle > limit and target_angle > limit) or \
        (angle < limit and target_angle < limit)):
            loop1.reverse()
            if circular:
                loop1 = [loop1[-1]] + loop1[:-1]
        elif normals[0].angle(normals[1]) > limit:
            loop1.reverse()
            if circular:
                loop1 = [loop1[-1]] + loop1[:-1]
    
    # both loops have the same length
    if len(loop1) == len(loop2):
        # manual override
        if twist:
            if abs(twist) < len(loop1):
                loop1 = loop1[twist:]+loop1[:twist]
        if reverse:
            loop1.reverse()
        
        lines.append([loop1[0], loop2[0]])
        for i in range(1, len(loop1)):
            lines.append([loop1[i], loop2[i]])
    
    # loops of different lengths
    else:
        # make loop1 longest loop
        if len(loop2) > len(loop1):
            loop1, loop2 = loop2, loop1
            loop1_circular, loop2_circular = loop2_circular, loop1_circular
        
        # manual override
        if twist:
            if abs(twist) < len(loop1):
                loop1 = loop1[twist:]+loop1[:twist]
        if reverse:
            loop1.reverse()
            
        # shortest angle difference doesn't always give correct start vertex
        if loop1_circular and not loop2_circular:
            shifting = 1
            while shifting:
                if len(loop1) - shifting < len(loop2):
                    shifting = False
                    break
                to_last, to_first = [((mesh.vertices[loop1[-1]].co - \
                    center1) * rotation_matrix).angle((mesh.\
                    vertices[loop2[i]].co - center2), 0) for i in [-1, 0]]
                if to_first < to_last:
                    loop1 = [loop1[-1]] + loop1[:-1]
                    shifting += 1
                else:
                    shifting = False
                    break
        
        # basic shortest side first
        if mode == 'basic':
            lines.append([loop1[0], loop2[0]])
            for i in range(1, len(loop1)):
                if i >= len(loop2) - 1:
                    # triangles
                    lines.append([loop1[i], loop2[-1]])
                else:
                    # quads
                    lines.append([loop1[i], loop2[i]])
        
        # shortest edge algorithm
        else: # mode == 'shortest'
            lines.append([loop1[0], loop2[0]])
            prev_vert2 = 0
            for i in range(len(loop1) -1):
                if prev_vert2 == len(loop2) - 1 and not loop2_circular:
                    # force triangles, reached end of loop2
                    tri, quad = 0, 1
                elif prev_vert2 == len(loop2) - 1 and loop2_circular:
                    # at end of loop2, but circular, so check with first vert
                    tri, quad = [(mathutils.Vector(mesh.vertices[loop1[i+1]].\
                        co) - mathutils.Vector(mesh.vertices[loop2[j]].co)).\
                        length for j in [prev_vert2, 0]]
                    circle_full = 2
                elif len(loop1) - 1 - i == len(loop2) - 1 - prev_vert2 and \
                not circle_full:
                    # force quads, otherwise won't make it to end of loop2
                    tri, quad = 1, 0
                else:
                    # calculate if tri or quad gives shortest edge
                    tri, quad = [(mathutils.Vector(mesh.vertices[loop1[i+1]].\
                        co) - mathutils.Vector(mesh.vertices[loop2[j]].co)).\
                        length for j in range(prev_vert2, prev_vert2+2)]
                
                # triangle
                if tri < quad:
                    lines.append([loop1[i+1], loop2[prev_vert2]])
                    if circle_full == 2:
                        circle_full = False
                # quad
                elif not circle_full:
                    lines.append([loop1[i+1], loop2[prev_vert2+1]])
                    prev_vert2 += 1
                # quad to first vertex of loop2
                else:
                    lines.append([loop1[i+1], loop2[0]])
                    prev_vert2 = 0
                    circle_full = True
    
    # final face for circular loops
    if loop1_circular and loop2_circular:
        lines.append([loop1[0], loop2[0]])
    
    return(lines)


# calculate number of segments needed
def bridge_calculate_segments(mesh, lines, loops, segments):
    # return if amount of segments is set by user
    if segments != 0:
        return segments
    
    # edge lengths
    average_edge_length = [(mesh.vertices[vertex].co - \
        mesh.vertices[loop[0][i+1]].co).length for loop in loops for \
        i, vertex in enumerate(loop[0][:-1])]
    # closing edges of circular loops
    average_edge_length += [(mesh.vertices[loop[0][-1]].co - \
        mesh.vertices[loop[0][0]].co).length for loop in loops if loop[1]] 
    
    # average lengths
    average_edge_length = sum(average_edge_length) / len(average_edge_length)
    average_bridge_length = sum([(mesh.vertices[v1].co - \
        mesh.vertices[v2].co).length for v1, v2 in lines]) / len(lines)
    
    segments = max(1, round(average_bridge_length / average_edge_length))
        
    return(segments)


# return dictionary with vertex index as key, and the normal vector as value
def bridge_calculate_virtual_vertex_normals(mesh, lines, loops, edge_faces,
edgekey_to_edge):
    if not edge_faces: # interpolation isn't set to cubic
        return False
    
    # pity reduce() isn't one of the basic functions in python anymore
    def average_vector_dictionary(dic):
        for key, vectors in dic.items():
            #if type(vectors) == type([]) and len(vectors) > 1:
            if len(vectors) > 1:
                average = mathutils.Vector([0, 0, 0])
                for vector in vectors:
                    average += vector
                average /= len(vectors)
                dic[key] = [average]
        return dic
    
    # get all edges of the loop
    edges = [[edgekey_to_edge[tuple(sorted([loops[j][0][i],
        loops[j][0][i+1]]))] for i in range(len(loops[j][0])-1)] for \
        j in [0,1]]
    edges = edges[0] + edges[1]
    for j in [0, 1]:
        if loops[j][1]: # circular
            edges.append(edgekey_to_edge[tuple(sorted([loops[j][0][0],
                loops[j][0][-1]]))])
    
    """
    calculation based on face topology (assign edge-normals to vertices)
    
    edge_normal = face_normal x edge_vector
    vertex_normal = average(edge_normals)
    """
    vertex_normals = dict([(vertex, []) for vertex in loops[0][0]+loops[1][0]])
    for edge in edges:
        faces = edge_faces[edge.key] # valid faces connected to edge
        
        if faces:
            # get edge coordinates
            v1, v2 = [mesh.vertices[edge.key[i]].co for i in [0,1]]
            edge_vector = v1 - v2
            if edge_vector.length < 1e-4:
                # zero-length edge, vertices at same location
                continue
            edge_center = (v1 + v2) / 2
            
            # average face coordinates, if connected to more than 1 valid face
            if len(faces) > 1:
                face_normal = mathutils.Vector([0, 0, 0])
                face_center = mathutils.Vector([0, 0, 0])
                for face in faces:
                    face_normal += face.normal
                    face_center += face.center
                face_normal /= len(faces)
                face_center /= len(faces)
            else:
                face_normal = faces[0].normal
                face_center = faces[0].center
            if face_normal.length < 1e-4:
                # faces with a surface of 0 have no face normal
                continue
            
            # calculate virtual edge normal
            edge_normal = edge_vector.cross(face_normal)
            edge_normal.length = 0.01
            if (face_center - (edge_center + edge_normal)).length > \
            (face_center - (edge_center - edge_normal)).length:
                # make normal face the correct way
                edge_normal.negate()
            edge_normal.normalize()
            # add virtual edge normal as entry for both vertices it connects
            for vertex in edge.key:
                vertex_normals[vertex].append(edge_normal)
    
    """ 
    calculation based on connection with other loop (vertex focused method) 
    - used for vertices that aren't connected to any valid faces
    
    plane_normal = edge_vector x connection_vector
    vertex_normal = plane_normal x edge_vector
    """
    vertices = [vertex for vertex, normal in vertex_normals.items() if not \
        normal]
    
    if vertices:
        # edge vectors connected to vertices
        edge_vectors = dict([[vertex, []] for vertex in vertices])
        for edge in edges:
            for v in edge.key:
                if v in edge_vectors:
                    edge_vector = mesh.vertices[edge.key[0]].co - \
                        mesh.vertices[edge.key[1]].co
                    if edge_vector.length < 1e-4:
                        # zero-length edge, vertices at same location
                        continue
                    edge_vectors[v].append(edge_vector)
    
        # connection vectors between vertices of both loops
        connection_vectors = dict([[vertex, []] for vertex in vertices])
        connections = dict([[vertex, []] for vertex in vertices])
        for v1, v2 in lines:
            if v1 in connection_vectors or v2 in connection_vectors:
                new_vector = mesh.vertices[v1].co - mesh.vertices[v2].co
                if new_vector.length < 1e-4:
                    # zero-length connection vector,
                    # vertices in different loops at same location
                    continue
                if v1 in connection_vectors:
                    connection_vectors[v1].append(new_vector)
                    connections[v1].append(v2)
                if v2 in connection_vectors:
                    connection_vectors[v2].append(new_vector)
                    connections[v2].append(v1)
        connection_vectors = average_vector_dictionary(connection_vectors)
        connection_vectors = dict([[vertex, vector[0]] if vector else \
            [vertex, []] for vertex, vector in connection_vectors.items()])
        
        for vertex, values in edge_vectors.items():
            # vertex normal doesn't matter, just assign a random vector to it
            if not connection_vectors[vertex]:
                vertex_normals[vertex] = [mathutils.Vector([1, 0, 0])]
                continue
            
            # calculate to what location the vertex is connected, 
            # used to determine what way to flip the normal
            connected_center = mathutils.Vector([0, 0, 0])
            for v in connections[vertex]:
                connected_center += mesh.vertices[v].co
            if len(connections[vertex]) > 1:
                connected_center /= len(connections[vertex])
            if len(connections[vertex]) == 0:
                # shouldn't be possible, but better safe than sorry
                vertex_normals[vertex] = [mathutils.Vector([1, 0, 0])]
                continue
            
            # can't do proper calculations, because of zero-length vector
            if not values:
                if (connected_center - (mesh.vertices[vertex].co + \
                connection_vectors[vertex])).length < (connected_center - \
                (mesh.vertices[vertex].co - connection_vectors[vertex])).\
                length:
                    connection_vectors[vertex].negate()
                vertex_normals[vertex] = [connection_vectors[vertex].\
                    normalized()]
                continue
            
            # calculate vertex normals using edge-vectors,
            # connection-vectors and the derived plane normal
            for edge_vector in values:
                plane_normal = edge_vector.cross(connection_vectors[vertex])
                vertex_normal = edge_vector.cross(plane_normal)
                vertex_normal.length = 0.1
                if (connected_center - (mesh.vertices[vertex].co + \
                vertex_normal)).length < (connected_center - \
                (mesh.vertices[vertex].co - vertex_normal)).length:
                # make normal face the correct way
                    vertex_normal.negate()
                vertex_normal.normalize()
                vertex_normals[vertex].append(vertex_normal)
    
    # average virtual vertex normals, based on all edges it's connected to
    vertex_normals = average_vector_dictionary(vertex_normals)
    vertex_normals = dict([[vertex, vector[0]] for vertex, vector in \
        vertex_normals.items()])
    
    return(vertex_normals)


# add vertices to mesh
def bridge_create_vertices(mesh, vertices):
    start_index = len(mesh.vertices)
    mesh.vertices.add(len(vertices))
    for i in range(len(vertices)):
        mesh.vertices[start_index + i].co = vertices[i]


# add faces to mesh
def bridge_create_faces(mesh, faces, twist):
    # have the normal point the correct way
    if twist < 0:
        [face.reverse() for face in faces]
        faces = [face[2:]+face[:2] if face[0]==face[1] else face for \
            face in faces]
    
    # eekadoodle prevention
    for i in range(len(faces)):
        if not faces[i][-1]:
            if faces[i][0] == faces[i][-1]:
                faces[i] = [faces[i][1], faces[i][2], faces[i][3], faces[i][1]]
            else:
                faces[i] = [faces[i][-1]] + faces[i][:-1]
    
    start_faces = len(mesh.faces)
    mesh.faces.add(len(faces))
    for i in range(len(faces)):
        mesh.faces[start_faces + i].vertices_raw = faces[i]
    mesh.update(calc_edges = True) # calc_edges prevents memory-corruption


# calculate input loops
def bridge_get_input(mesh):
    # create list of internal edges, which should be skipped
    eks_of_selected_faces = [item for sublist in [face.edge_keys for face \
        in mesh.faces if face.select and not face.hide] for item in sublist]
    edge_count = {}
    for ek in eks_of_selected_faces:
        if ek in edge_count:
            edge_count[ek] += 1
        else:
            edge_count[ek] = 1
    internal_edges = [ek for ek in edge_count if edge_count[ek] > 1]
    
    # sort correct edges into loops
    selected_edges = [edge.key for edge in mesh.edges if edge.select \
        and not edge.hide and edge.key not in internal_edges]
    loops = get_connected_selections(selected_edges)
    
    return(loops)


# return values needed by the bridge operator
def bridge_initialise(mesh, interpolation):
    if interpolation == 'cubic':
        # dict with edge-key as key and list of connected valid faces as value
        face_blacklist = [face.index for face in mesh.faces if face.select or \
            face.hide]
        edge_faces = dict([[edge.key, []] for edge in mesh.edges if not \
            edge.hide])
        for face in mesh.faces:
            if face.index in face_blacklist:
                continue
            for key in face.edge_keys:
                edge_faces[key].append(face)
        # dictionary with the edge-key as key and edge as value
        edgekey_to_edge = dict([[edge.key, edge] for edge in mesh.edges if \
            edge.select and not edge.hide])
    else:
        edge_faces = False
        edgekey_to_edge = False
    
    # selected faces input
    old_selected_faces = [face.index for face in mesh.faces if face.select \
        and not face.hide]
    
    # find out if faces created by bridging should be smoothed
    smooth = False
    if mesh.faces:
        if sum([face.use_smooth for face in mesh.faces])/len(mesh.faces) \
        >= 0.5:
            smooth = True
    
    return(edge_faces, edgekey_to_edge, old_selected_faces, smooth)


# return a string with the input method
def bridge_input_method(loft, loft_loop):
    method = ""
    if loft:
        if loft_loop:
            method = "Loft loop"
        else:
            method = "Loft no-loop"
    else:
        method = "Bridge"
    
    return(method)


# match up loops in pairs, used for multi-input bridging
def bridge_match_loops(mesh, loops):
    # calculate average loop normals and centers
    normals = []
    centers = []
    for vertices, circular in loops:
        normal = mathutils.Vector([0, 0, 0])
        center = mathutils.Vector([0, 0, 0])
        for vertex in vertices:
            normal += mesh.vertices[vertex].normal
            center += mesh.vertices[vertex].co
        normals.append(normal / len(vertices) / 10)
        centers.append(center / len(vertices))
    
    # possible matches if loop normals are faced towards the center
    # of the other loop
    matches = dict([[i, []] for i in range(len(loops))])
    matches_amount = 0
    for i in range(len(loops) + 1):
        for j in range(i+1, len(loops)):
            if (centers[i] - centers[j]).length > (centers[i] - (centers[j] \
            + normals[j])).length and (centers[j] - centers[i]).length > \
            (centers[j] - (centers[i] + normals[i])).length:
                matches_amount += 1
                matches[i].append([(centers[i] - centers[j]).length, i, j])
                matches[j].append([(centers[i] - centers[j]).length, j, i])
    # if no loops face each other, just make matches between all the loops
    if matches_amount == 0:
        for i in range(len(loops) + 1):
            for j in range(i+1, len(loops)):
                matches[i].append([(centers[i] - centers[j]).length, i, j])
                matches[j].append([(centers[i] - centers[j]).length, j, i])
    for key, value in matches.items():
        value.sort()
    
    # matches based on distance between centers and number of vertices in loops
    new_order = []
    for loop_index in range(len(loops)):
        if loop_index in new_order:
            continue
        loop_matches = matches[loop_index]
        if not loop_matches:
            continue
        shortest_distance = loop_matches[0][0]
        shortest_distance *= 1.1
        loop_matches = [[abs(len(loops[loop_index][0]) - \
            len(loops[loop[2]][0])), loop[0], loop[1], loop[2]] for loop in \
            loop_matches if loop[0] < shortest_distance]
        loop_matches.sort()
        for match in loop_matches:
            if match[3] not in new_order:
                new_order += [loop_index, match[3]]
                break
    
    # reorder loops based on matches
    if len(new_order) >= 2:
        loops = [loops[i] for i in new_order]
    
    return(loops)


# have normals of selection face outside
def bridge_recalculate_normals():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.normals_make_consistent()


# remove old_selected_faces
def bridge_remove_internal_faces(mesh, old_selected_faces):
    select_mode = [i for i in bpy.context.tool_settings.mesh_select_mode]
    bpy.context.tool_settings.mesh_select_mode = [False, False, True]
    
    # hack to keep track of the current selection
    for edge in mesh.edges:
        if edge.select and not edge.hide:
            edge.bevel_weight = (edge.bevel_weight/3) + 0.2
        else:
            edge.bevel_weight = (edge.bevel_weight/3) + 0.6
    
    # remove faces
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for face in old_selected_faces:
        mesh.faces[face].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type = 'FACE')
    
    # restore old selection, using hack
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    for edge in mesh.edges:
        if edge.bevel_weight < 0.6:
            edge.bevel_weight = (edge.bevel_weight-0.2) * 3
            edge.select = True
        else:
            edge.bevel_weight = (edge.bevel_weight-0.6) * 3
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.tool_settings.mesh_select_mode = select_mode


# update list of internal faces that are flagged for removal
def bridge_save_unused_faces(mesh, old_selected_faces, loops):
    # key: vertex index, value: lists of selected faces using it
    vertex_to_face = dict([[i, []] for i in range(len(mesh.vertices))])
    [[vertex_to_face[vertex_index].append(face) for vertex_index in \
        mesh.faces[face].vertices] for face in old_selected_faces]
    
    # group selected faces that are connected
    groups = []
    grouped_faces = []
    for face in old_selected_faces:
        if face in grouped_faces:
            continue
        grouped_faces.append(face)
        group = [face]
        new_faces = [face]
        while new_faces:
            grow_face = new_faces[0]
            for vertex in mesh.faces[grow_face].vertices:
                vertex_face_group = [face for face in vertex_to_face[vertex] \
                    if face not in grouped_faces]
                new_faces += vertex_face_group
                grouped_faces += vertex_face_group
                group += vertex_face_group
            new_faces.pop(0)
        groups.append(group)
    
    # key: vertex index, value: True/False (is it in a loop that is used)
    used_vertices = dict([[i, 0] for i in range(len(mesh.vertices))])
    for loop in loops:
        for vertex in loop[0]:
            used_vertices[vertex] = True
    
    # check if group is bridged, if not remove faces from internal faces list
    for group in groups:
        used = False
        for face in group:
            if used:
                break
            for vertex in mesh.faces[face].vertices:
                if used_vertices[vertex]:
                    used = True
                    break
        if not used:
            for face in group:
                old_selected_faces.remove(face)


# add the newly created faces to the selection
def bridge_select_new_faces(mesh, amount, smooth):
    select_mode = [i for i in bpy.context.tool_settings.mesh_select_mode]
    bpy.context.tool_settings.mesh_select_mode = [False, False, True]
    for i in range(amount):
        mesh.faces[-(i+1)].select = True
        mesh.faces[-(i+1)].use_smooth = smooth
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.tool_settings.mesh_select_mode = select_mode


# sort loops, so they are connected in the correct order when lofting
def bridge_sort_loops(mesh, loops, loft_loop):
    # simplify loops to single points, and prepare for pathfinding
    x, y, z = [[sum([mesh.vertices[i].co[j] for i in loop[0]]) / \
        len(loop[0]) for loop in loops] for j in range(3)]
    nodes = [mathutils.Vector([x[i], y[i], z[i]]) for i in range(len(loops))]
    
    active_node = 0
    open = [i for i in range(1, len(loops))]
    path = [[0,0]]
    # connect node to path, that is shortest to active_node
    while len(open) > 0:
        distances = [(nodes[active_node] - nodes[i]).length for i in open]
        active_node = open[distances.index(min(distances))]
        open.remove(active_node)
        path.append([active_node, min(distances)])
    # check if we didn't start in the middle of the path
    for i in range(2, len(path)):
        if (nodes[path[i][0]]-nodes[0]).length < path[i][1]:
            temp = path[:i]
            path.reverse()
            path = path[:-i] + temp
            break
    
    # reorder loops
    loops = [loops[i[0]] for i in path]
    # if requested, duplicate first loop at last position, so loft can loop
    if loft_loop:
        loops = loops + [loops[0]]
    
    return(loops)


##########################################
####### Circle functions #################
##########################################

# convert 3d coordinates to 2d coordinates on plane
def circle_3d_to_2d(mesh_mod, loop, com, normal):
    # project vertices onto the plane
    verts = [mesh_mod.vertices[v] for v in loop[0]]
    verts_projected = [[mathutils.Vector(v.co[:]) - \
        (mathutils.Vector(v.co[:])-com).dot(normal)*normal, v.index] \
        for v in verts]
    
    # calculate two vectors (p and q) along the plane
    m = mathutils.Vector([normal[0]+1.0, normal[1], normal[2]])
    p = m - (m.dot(normal) * normal)
    if p.dot(p) == 0.0:
        m = mathutils.Vector([normal[0], normal[1]+1.0, normal[2]])
        p = m - (m.dot(normal) * normal)
    q = p.cross(normal)
    
    # change to 2d coordinates using perpendicular projection
    locs_2d = []
    for loc, vert in verts_projected:
        vloc = loc - com
        x = p.dot(vloc) / p.dot(p)
        y = q.dot(vloc) / q.dot(q)
        locs_2d.append([x, y, vert])
    
    return(locs_2d, p, q)


# calculate a best-fit circle to the 2d locations on the plane
def circle_calculate_best_fit(locs_2d):
    # initial guess
    x0 = 0.0
    y0 = 0.0
    r = 1.0
    
    # calculate center and radius (non-linear least squares solution)
    for iter in range(500):
        jmat = []
        k = []
        for v in locs_2d:
            d = (v[0]**2-2.0*x0*v[0]+v[1]**2-2.0*y0*v[1]+x0**2+y0**2)**0.5
            jmat.append([(x0-v[0])/d, (y0-v[1])/d, -1.0])
            k.append(-(((v[0]-x0)**2+(v[1]-y0)**2)**0.5-r))
        jmat2 = mathutils.Matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], \
            [0.0, 0.0, 0.0]])
        k2 = mathutils.Vector([0.0, 0.0, 0.0])
        for i in range(len(jmat)):
            k2 += mathutils.Vector(jmat[i])*k[i]
            jmat2[0][0] += jmat[i][0]**2
            jmat2[0][1] += jmat[i][0]*jmat[i][1]
            jmat2[0][2] += jmat[i][0]*jmat[i][2]
            jmat2[1][1] += jmat[i][1]**2
            jmat2[1][2] += jmat[i][1]*jmat[i][2]
            jmat2[2][2] += jmat[i][2]**2
        jmat2[1][0] = jmat2[0][1]
        jmat2[2][0] = jmat2[0][2]
        jmat2[2][1] = jmat2[1][2]
        try:
            jmat2.invert()
        except:
            pass
        dx0, dy0, dr = k2 * jmat2
        x0 += dx0
        y0 += dy0
        r += dr
        # stop iterating if we're close enough to optimal solution
        if abs(dx0)<1e-6 and abs(dy0)<1e-6 and abs(dr)<1e-6:
            break
    
    # return center of circle and radius
    return(x0, y0, r)


# calculate circle so no vertices have to be moved away from the center
def circle_calculate_min_fit(locs_2d):
    # center of circle
    x0 = (min([i[0] for i in locs_2d])+max([i[0] for i in locs_2d]))/2.0
    y0 = (min([i[1] for i in locs_2d])+max([i[1] for i in locs_2d]))/2.0
    center = mathutils.Vector([x0, y0])
    # radius of circle
    r = min([(mathutils.Vector([i[0], i[1]])-center).length for i in locs_2d])
    
    # return center of circle and radius
    return(x0, y0, r)


# calculate the new locations of the vertices that need to be moved
def circle_calculate_verts(flatten, mesh_mod, locs_2d, com, p, q, normal):
    # changing 2d coordinates back to 3d coordinates
    locs_3d = []
    for loc in locs_2d:
        locs_3d.append([loc[2], loc[0]*p + loc[1]*q + com])
    
    if flatten: # flat circle
        return(locs_3d)
    
    else: # project the locations on the existing mesh
        vert_edges = dict_vert_edges(mesh_mod)
        vert_faces = dict_vert_faces(mesh_mod)
        faces = [f for f in mesh_mod.faces if not f.hide]
        rays = [normal, -normal]
        new_locs = []
        for loc in locs_3d:
            projection = False
            if mesh_mod.vertices[loc[0]].co == loc[1]: # vertex hasn't moved
                projection = loc[1]
            else:
                dif = normal.angle(loc[1]-mesh_mod.vertices[loc[0]].co)
                if -1e-6 < dif < 1e-6 or math.pi-1e-6 < dif < math.pi+1e-6:
                    # original location is already along projection normal
                    projection = mesh_mod.vertices[loc[0]].co
                else:
                    # quick search through adjacent faces
                    for face in vert_faces[loc[0]]:
                        verts = [mesh_mod.vertices[v].co for v in \
                            mesh_mod.faces[face].vertices]
                        if len(verts) == 3: # triangle
                            v1, v2, v3 = verts
                            v4 = False
                        else: # quad
                            v1, v2, v3, v4 = verts
                        for ray in rays:
                            intersect = mathutils.geometry.\
                            intersect_ray_tri(v1, v2, v3, ray, loc[1])
                            if intersect:
                                projection = intersect
                                break
                            elif v4:
                                intersect = mathutils.geometry.\
                                intersect_ray_tri(v1, v3, v4, ray, loc[1])
                                if intersect:
                                    projection = intersect
                                    break
                        if projection:
                            break
            if not projection:
                # check if projection is on adjacent edges
                for edgekey in vert_edges[loc[0]]:
                    line1 = mesh_mod.vertices[edgekey[0]].co
                    line2 = mesh_mod.vertices[edgekey[1]].co
                    intersect, dist = mathutils.geometry.intersect_point_line(\
                        loc[1], line1, line2)
                    if 1e-6 < dist < 1 - 1e-6:
                        projection = intersect
                        break
            if not projection:
                # full search through the entire mesh
                hits = []
                for face in faces:
                    verts = [mesh_mod.vertices[v].co for v in face.vertices]
                    if len(verts) == 3: # triangle
                        v1, v2, v3 = verts
                        v4 = False
                    else: # quad
                        v1, v2, v3, v4 = verts
                    for ray in rays:
                        intersect = mathutils.geometry.intersect_ray_tri(\
                            v1, v2, v3, ray, loc[1])
                        if intersect:
                            hits.append([(loc[1] - intersect).length,
                                intersect])
                            break
                        elif v4:
                            intersect = mathutils.geometry.intersect_ray_tri(\
                                v1, v3, v4, ray, loc[1])
                            if intersect:
                                hits.append([(loc[1] - intersect).length,
                                    intersect])
                                break
                if len(hits) >= 1:
                    # if more than 1 hit with mesh, closest hit is new loc
                    hits.sort()
                    projection = hits[0][1]
            if not projection:
                # nothing to project on, remain at flat location
                projection = loc[1]
            new_locs.append([loc[0], projection])
        
        # return new positions of projected circle
        return(new_locs)


# check loops and only return valid ones
def circle_check_loops(single_loops, loops, mapping, mesh_mod):
    valid_single_loops = {}
    valid_loops = []
    for i, [loop, circular] in enumerate(loops):
        # loop needs to have at least 3 vertices
        if len(loop) < 3:
            continue
        # loop needs at least 1 vertex in the original, non-mirrored mesh
        if mapping:
            all_virtual = True
            for vert in loop:
                if mapping[vert] > -1:
                    all_virtual = False
                    break
            if all_virtual:
                continue
        # loop has to be non-collinear
        collinear = True
        loc0 = mathutils.Vector(mesh_mod.vertices[loop[0]].co[:])
        loc1 = mathutils.Vector(mesh_mod.vertices[loop[1]].co[:])
        for v in loop[2:]:
            locn = mathutils.Vector(mesh_mod.vertices[v].co[:])
            if loc0 == loc1 or loc1 == locn:
                loc0 = loc1
                loc1 = locn
                continue
            d1 = loc1-loc0
            d2 = locn-loc1
            if -1e-6 < d1.angle(d2, 0) < 1e-6:
                loc0 = loc1
                loc1 = locn
                continue
            collinear = False
            break
        if collinear:
            continue
        # passed all tests, loop is valid
        valid_loops.append([loop, circular])
        valid_single_loops[len(valid_loops)-1] = single_loops[i]
    
    return(valid_single_loops, valid_loops)


# calculate the location of single input vertices that need to be flattened
def circle_flatten_singles(mesh_mod, com, p, q, normal, single_loop):
    new_locs = []
    for vert in single_loop:
        loc = mathutils.Vector(mesh_mod.vertices[vert].co[:])
        new_locs.append([vert,  loc - (loc-com).dot(normal)*normal])
    
    return(new_locs)


# calculate input loops
def circle_get_input(object, mesh, scene):
    # get mesh with modifiers applied
    derived, mesh_mod = get_derived_mesh(object, mesh, scene)
    
    # create list of edge-keys based on selection state
    faces = False
    for face in mesh.faces:
        if face.select and not face.hide:
            faces = True
            break
    if faces:
        # get selected, non-hidden , non-internal edge-keys
        eks_selected = [key for keys in [face.edge_keys for face in \
            mesh_mod.faces if face.select and not face.hide] for key in keys]
        edge_count = {}
        for ek in eks_selected:
            if ek in edge_count:
                edge_count[ek] += 1
            else:
                edge_count[ek] = 1
        edge_keys = [edge.key for edge in mesh_mod.edges if edge.select \
            and not edge.hide and edge_count.get(edge.key, 1)==1]
    else:
        # no faces, so no internal edges either
        edge_keys = [edge.key for edge in mesh_mod.edges if edge.select \
            and not edge.hide]
    
    # add edge-keys around single vertices
    verts_connected = dict([[vert, 1] for edge in [edge for edge in \
        mesh_mod.edges if edge.select and not edge.hide] for vert in edge.key])
    single_vertices = [vert.index for vert in mesh_mod.vertices if \
        vert.select and not vert.hide and not \
        verts_connected.get(vert.index, False)]
    
    if single_vertices and len(mesh.faces)>0:
        vert_to_single = dict([[v.index, []] for v in mesh_mod.vertices \
            if not v.hide])
        for face in [face for face in mesh_mod.faces if not face.select \
        and not face.hide]:
            for vert in face.vertices:
                if vert in single_vertices:
                    for ek in face.edge_keys:
                        if not vert in ek:
                            edge_keys.append(ek)
                            if vert not in vert_to_single[ek[0]]:
                                vert_to_single[ek[0]].append(vert)
                            if vert not in vert_to_single[ek[1]]:
                                vert_to_single[ek[1]].append(vert)
                    break
    
    # sort edge-keys into loops
    loops = get_connected_selections(edge_keys)
    
    # find out to which loops the single vertices belong
    single_loops = dict([[i, []] for i in range(len(loops))])
    if single_vertices and len(mesh.faces)>0:
        for i, [loop, circular] in enumerate(loops):
            for vert in loop:
                if vert_to_single[vert]:
                    for single in vert_to_single[vert]:
                        if single not in single_loops[i]:
                            single_loops[i].append(single)
    
    return(derived, mesh_mod, single_vertices, single_loops, loops)


# recalculate positions based on the influence of the circle shape
def circle_influence_locs(locs_2d, new_locs_2d, influence):
    for i in range(len(locs_2d)):
        oldx, oldy, j = locs_2d[i]
        newx, newy, k = new_locs_2d[i]
        altx = newx*(influence/100)+ oldx*((100-influence)/100)
        alty = newy*(influence/100)+ oldy*((100-influence)/100)
        locs_2d[i] = [altx, alty, j]
    
    return(locs_2d)


# project 2d locations on circle, respecting distance relations between verts
def circle_project_non_regular(locs_2d, x0, y0, r):
    for i in range(len(locs_2d)):
        x, y, j = locs_2d[i]
        loc = mathutils.Vector([x-x0, y-y0])
        loc.length = r
        locs_2d[i] = [loc[0], loc[1], j]
    
    return(locs_2d)


# project 2d locations on circle, with equal distance between all vertices
def circle_project_regular(locs_2d, x0, y0, r):
    # find offset angle and circling direction
    x, y, i = locs_2d[0]
    loc = mathutils.Vector([x-x0, y-y0])
    loc.length = r
    offset_angle = loc.angle(mathutils.Vector([1.0, 0.0]), 0.0)
    loca = mathutils.Vector([x-x0, y-y0, 0.0])
    if loc[1] < -1e-6:
        offset_angle *= -1
    x, y, j = locs_2d[1]
    locb = mathutils.Vector([x-x0, y-y0, 0.0])
    if loca.cross(locb)[2] >= 0:
        ccw = 1
    else:
        ccw = -1
    # distribute vertices along the circle
    for i in range(len(locs_2d)):
        t = offset_angle + ccw * (i / len(locs_2d) * 2 * math.pi)
        x = math.cos(t) * r
        y = math.sin(t) * r
        locs_2d[i] = [x, y, locs_2d[i][2]]
    
    return(locs_2d)


# shift loop, so the first vertex is closest to the center
def circle_shift_loop(mesh_mod, loop, com):
    verts, circular = loop
    distances = [[(mesh_mod.vertices[vert].co - com).length, i] \
        for i, vert in enumerate(verts)]
    distances.sort()
    shift = distances[0][1]
    loop = [verts[shift:] + verts[:shift], circular]
    
    return(loop)


##########################################
####### Curve functions ##################
##########################################

# create lists with knots and points, all correctly sorted
def curve_calculate_knots(loop, verts_selected):
    knots = [v for v in loop[0] if v in verts_selected]
    points = loop[0][:]
    # circular loop, potential for weird splines
    if loop[1]:
        offset = int(len(loop[0]) / 4)
        kpos = []
        for k in knots:
            kpos.append(loop[0].index(k))
        kdif = []
        for i in range(len(kpos) - 1):
            kdif.append(kpos[i+1] - kpos[i])
        kdif.append(len(loop[0]) - kpos[-1] + kpos[0])
        kadd = []
        for k in kdif:
            if k > 2 * offset:
                kadd.append([kdif.index(k), True])
            # next 2 lines are optional, they insert
            # an extra control point in small gaps
            #elif k > offset:
            #   kadd.append([kdif.index(k), False])
        kins = []
        krot = False
        for k in kadd: # extra knots to be added
            if k[1]: # big gap (break circular spline)
                kpos = loop[0].index(knots[k[0]]) + offset
                if kpos > len(loop[0]) - 1:
                    kpos -= len(loop[0])
                kins.append([knots[k[0]], loop[0][kpos]])
                kpos2 = k[0] + 1
                if kpos2 > len(knots)-1:
                    kpos2 -= len(knots)
                kpos2 = loop[0].index(knots[kpos2]) - offset
                if kpos2 < 0:
                    kpos2 += len(loop[0])
                kins.append([loop[0][kpos], loop[0][kpos2]])
                krot = loop[0][kpos2]
            else: # small gap (keep circular spline)
                k1 = loop[0].index(knots[k[0]])
                k2 = k[0] + 1
                if k2 > len(knots)-1:
                    k2 -= len(knots)
                k2 = loop[0].index(knots[k2])
                if k2 < k1:
                    dif = len(loop[0]) - 1 - k1 + k2
                else:
                    dif = k2 - k1
                kn = k1 + int(dif/2)
                if kn > len(loop[0]) - 1:
                    kn -= len(loop[0])
                kins.append([loop[0][k1], loop[0][kn]])
        for j in kins: # insert new knots
            knots.insert(knots.index(j[0]) + 1, j[1])
        if not krot: # circular loop
            knots.append(knots[0])
            points = loop[0][loop[0].index(knots[0]):]
            points += loop[0][0:loop[0].index(knots[0]) + 1]
        else: # non-circular loop (broken by script)
            krot = knots.index(krot)
            knots = knots[krot:] + knots[0:krot]
            if loop[0].index(knots[0]) > loop[0].index(knots[-1]):
                points = loop[0][loop[0].index(knots[0]):]
                points += loop[0][0:loop[0].index(knots[-1])+1]
            else:
                points = loop[0][loop[0].index(knots[0]):\
                    loop[0].index(knots[-1]) + 1]
    # non-circular loop, add first and last point as knots
    else:
        if loop[0][0] not in knots:
            knots.insert(0, loop[0][0])
        if loop[0][-1] not in knots:
            knots.append(loop[0][-1])
    
    return(knots, points)


# calculate relative positions compared to first knot
def curve_calculate_t(mesh_mod, knots, points, pknots, regular, circular):
    tpoints = []
    loc_prev = False
    len_total = 0
    
    for p in points:
        if p in knots:
            loc = pknots[knots.index(p)] # use projected knot location
        else:
            loc = mathutils.Vector(mesh_mod.vertices[p].co[:])
        if not loc_prev:
            loc_prev = loc
        len_total += (loc-loc_prev).length
        tpoints.append(len_total)
        loc_prev = loc
    tknots = []
    for p in points:
        if p in knots:
            tknots.append(tpoints[points.index(p)])
    if circular:
        tknots[-1] = tpoints[-1]
    
    # regular option
    if regular:
        tpoints_average = tpoints[-1] / (len(tpoints) - 1)
        for i in range(1, len(tpoints) - 1):
            tpoints[i] = i * tpoints_average
        for i in range(len(knots)):
            tknots[i] = tpoints[points.index(knots[i])]
        if circular:
            tknots[-1] = tpoints[-1]
    
    
    return(tknots, tpoints)


# change the location of non-selected points to their place on the spline
def curve_calculate_vertices(mesh_mod, knots, tknots, points, tpoints, splines,
interpolation, restriction):
    newlocs = {}
    move = []
    
    for p in points:
        if p in knots:
            continue
        m = tpoints[points.index(p)]
        if m in tknots:
            n = tknots.index(m)
        else:
            t = tknots[:]
            t.append(m)
            t.sort()
            n = t.index(m) - 1
        if n > len(splines) - 1:
            n = len(splines) - 1
        elif n < 0:
            n = 0
        
        if interpolation == 'cubic':
            ax, bx, cx, dx, tx = splines[n][0]
            x = ax + bx*(m-tx) + cx*(m-tx)**2 + dx*(m-tx)**3
            ay, by, cy, dy, ty = splines[n][1]
            y = ay + by*(m-ty) + cy*(m-ty)**2 + dy*(m-ty)**3
            az, bz, cz, dz, tz = splines[n][2]
            z = az + bz*(m-tz) + cz*(m-tz)**2 + dz*(m-tz)**3
            newloc = mathutils.Vector([x,y,z])
        else: # interpolation == 'linear'
            a, d, t, u = splines[n]
            newloc = ((m-t)/u)*d + a

        if restriction != 'none': # vertex movement is restricted
            newlocs[p] = newloc
        else: # set the vertex to its new location
            move.append([p, newloc])
        
    if restriction != 'none': # vertex movement is restricted
        for p in points:
            if p in newlocs:
                newloc = newlocs[p]
            else:
                move.append([p, mesh_mod.vertices[p].co])
                continue
            oldloc = mesh_mod.vertices[p].co
            normal = mesh_mod.vertices[p].normal
            dloc = newloc - oldloc
            if dloc.length < 1e-6:
                move.append([p, newloc])
            elif restriction == 'extrude': # only extrusions
                if dloc.angle(normal, 0) < 0.5 * math.pi + 1e-6:
                    move.append([p, newloc])
            else: # restriction == 'indent' only indentations
                if dloc.angle(normal) > 0.5 * math.pi - 1e-6:
                    move.append([p, newloc])

    return(move)


# trim loops to part between first and last selected vertices (including)
def curve_cut_boundaries(mesh_mod, loops):
    cut_loops = []
    for loop, circular in loops:
        if circular:
            # don't cut
            cut_loops.append([loop, circular])
            continue
        selected = [mesh_mod.vertices[v].select for v in loop]
        first = selected.index(True)
        selected.reverse()
        last = -selected.index(True)
        if last == 0:
            cut_loops.append([loop[first:], circular])
        else:
            cut_loops.append([loop[first:last], circular])
    
    return(cut_loops)


# calculate input loops
def curve_get_input(object, mesh, boundaries, scene):
    # get mesh with modifiers applied
    derived, mesh_mod = get_derived_mesh(object, mesh, scene)
    
    # vertices that still need a loop to run through it
    verts_unsorted = [v.index for v in mesh_mod.vertices if \
        v.select and not v.hide]
    # necessary dictionaries
    vert_edges = dict_vert_edges(mesh_mod)
    edge_faces = dict_edge_faces(mesh_mod)
    correct_loops = []
    
    # find loops through each selected vertex
    while len(verts_unsorted) > 0:
        loops = curve_vertex_loops(mesh_mod, verts_unsorted[0], vert_edges,
            edge_faces)
        verts_unsorted.pop(0)
        
        # check if loop is fully selected
        search_perpendicular = False
        i = -1
        for loop, circular in loops:
            i += 1
            selected = [v for v in loop if mesh_mod.vertices[v].select]
            if len(selected) < 2:
                # only one selected vertex on loop, don't use
                loops.pop(i)
                continue
            elif len(selected) == len(loop):
                search_perpendicular = loop
                break
        # entire loop is selected, find perpendicular loops
        if search_perpendicular:
            for vert in loop:
                if vert in verts_unsorted:
                    verts_unsorted.remove(vert)
            perp_loops = curve_perpendicular_loops(mesh_mod, loop,
                vert_edges, edge_faces)
            for perp_loop in perp_loops:
                correct_loops.append(perp_loop)
        # normal input
        else:
            for loop, circular in loops:
                correct_loops.append([loop, circular])
    
    # boundaries option
    if boundaries:
        correct_loops = curve_cut_boundaries(mesh_mod, correct_loops)
    
    return(derived, mesh_mod, correct_loops)


# return all loops that are perpendicular to the given one
def curve_perpendicular_loops(mesh_mod, start_loop, vert_edges, edge_faces):
    # find perpendicular loops
    perp_loops = []
    for start_vert in start_loop:
        loops = curve_vertex_loops(mesh_mod, start_vert, vert_edges,
            edge_faces)
        for loop, circular in loops:
            selected = [v for v in loop if mesh_mod.vertices[v].select]
            if len(selected) == len(loop):
                continue
            else:
                perp_loops.append([loop, circular, loop.index(start_vert)])
    
    # trim loops to same lengths
    shortest = [[len(loop[0]), i] for i, loop in enumerate(perp_loops)\
        if not loop[1]]
    if not shortest:
        # all loops are circular, not trimming
        return([[loop[0], loop[1]] for loop in perp_loops])
    else:
        shortest = min(shortest)
    shortest_start = perp_loops[shortest[1]][2]
    before_start = shortest_start
    after_start = shortest[0] - shortest_start - 1
    bigger_before = before_start > after_start
    trimmed_loops = []
    for loop in perp_loops:
        # have the loop face the same direction as the shortest one
        if bigger_before:
            if loop[2] < len(loop[0]) / 2:
                loop[0].reverse()
                loop[2] = len(loop[0]) - loop[2] - 1
        else:
            if loop[2] > len(loop[0]) / 2:
                loop[0].reverse()
                loop[2] = len(loop[0]) - loop[2] - 1
        # circular loops can shift, to prevent wrong trimming
        if loop[1]:
            shift = shortest_start - loop[2]
            if loop[2] + shift > 0 and loop[2] + shift < len(loop[0]):
                loop[0] = loop[0][-shift:] + loop[0][:-shift]
            loop[2] += shift
            if loop[2] < 0:
                loop[2] += len(loop[0])
            elif loop[2] > len(loop[0]) -1:
                loop[2] -= len(loop[0])
        # trim
        start = max(0, loop[2] - before_start)
        end = min(len(loop[0]), loop[2] + after_start + 1)
        trimmed_loops.append([loop[0][start:end], False])
    
    return(trimmed_loops)


# project knots on non-selected geometry
def curve_project_knots(mesh_mod, verts_selected, knots, points, circular):
    # function to project vertex on edge
    def project(v1, v2, v3):
        # v1 and v2 are part of a line
        # v3 is projected onto it
        v2 -= v1
        v3 -= v1
        p = v3.project(v2)
        return(p + v1)
    
    if circular: # project all knots
        start = 0
        end = len(knots)
        pknots = []
    else: # first and last knot shouldn't be projected
        start = 1
        end = -1
        pknots = [mathutils.Vector(mesh_mod.vertices[knots[0]].co[:])]
    for knot in knots[start:end]:
        if knot in verts_selected:
            knot_left = knot_right = False
            for i in range(points.index(knot)-1, -1*len(points), -1):
                if points[i] not in knots:
                    knot_left = points[i]
                    break
            for i in range(points.index(knot)+1, 2*len(points)):
                if i > len(points) - 1:
                    i -= len(points)
                if points[i] not in knots:
                    knot_right = points[i]
                    break
            if knot_left and knot_right and knot_left != knot_right:
                knot_left = mathutils.Vector(\
                    mesh_mod.vertices[knot_left].co[:])
                knot_right = mathutils.Vector(\
                    mesh_mod.vertices[knot_right].co[:])
                knot = mathutils.Vector(mesh_mod.vertices[knot].co[:])
                pknots.append(project(knot_left, knot_right, knot))
            else:
                pknots.append(mathutils.Vector(mesh_mod.vertices[knot].co[:]))
        else: # knot isn't selected, so shouldn't be changed
            pknots.append(mathutils.Vector(mesh_mod.vertices[knot].co[:]))
    if not circular:
        pknots.append(mathutils.Vector(mesh_mod.vertices[knots[-1]].co[:]))
    
    return(pknots)


# find all loops through a given vertex
def curve_vertex_loops(mesh_mod, start_vert, vert_edges, edge_faces):
    edges_used = []
    loops = []
        
    for edge in vert_edges[start_vert]:
        if edge in edges_used:
            continue
        loop = []
        circular = False
        for vert in edge:
            active_faces = edge_faces[edge]
            new_vert = vert
            growing = True
            while growing:
                growing = False
                new_edges = vert_edges[new_vert]
                loop.append(new_vert)
                if len(loop) > 1:
                    edges_used.append(tuple(sorted([loop[-1], loop[-2]])))
                if len(new_edges) < 3 or len(new_edges) > 4:
                    # pole
                    break
                else:
                    # find next edge
                    for new_edge in new_edges:
                        if new_edge in edges_used:
                            continue
                        eliminate = False
                        for new_face in edge_faces[new_edge]:
                            if new_face in active_faces:
                                eliminate = True
                                break
                        if eliminate:
                            continue
                        # found correct new edge
                        active_faces = edge_faces[new_edge]
                        v1, v2 = new_edge
                        if v1 != new_vert:
                            new_vert = v1
                        else:
                            new_vert = v2
                        if new_vert == loop[0]:
                            circular = True
                        else:
                            growing = True
                        break
            if circular:
                break
            loop.reverse()
        loops.append([loop, circular])
    
    return(loops)


##########################################
####### Flatten functions ################
##########################################

# sort input into loops
def flatten_get_input(mesh):
    vert_verts = dict_vert_verts([edge.key for edge in mesh.edges \
        if edge.select and not edge.hide])
    verts = [v.index for v in mesh.vertices if v.select and not v.hide]
    
    # no connected verts, consider all selected verts as a single input
    if not vert_verts:
        return([[verts, False]])
    
    loops = []
    while len(verts) > 0:
        # start of loop
        loop = [verts[0]]
        verts.pop(0)
        if loop[-1] in vert_verts:
            to_grow = vert_verts[loop[-1]]
        else:
            to_grow = []
        # grow loop
        while len(to_grow) > 0:
            new_vert = to_grow[0]
            to_grow.pop(0)
            if new_vert in loop:
                continue
            loop.append(new_vert)
            verts.remove(new_vert)
            to_grow += vert_verts[new_vert]
        # add loop to loops
        loops.append([loop, False])
    
    return(loops)


# calculate position of vertex projections on plane
def flatten_project(mesh, loop, com, normal):
    verts = [mesh.vertices[v] for v in loop[0]]
    verts_projected = [[v.index, mathutils.Vector(v.co[:]) - \
        (mathutils.Vector(v.co[:])-com).dot(normal)*normal] for v in verts]
    
    return(verts_projected)


##########################################
####### Relax functions ##################
##########################################

# create lists with knots and points, all correctly sorted
def relax_calculate_knots(loops):
    all_knots = []
    all_points = []
    for loop, circular in loops:
        knots = [[], []]
        points = [[], []]
        if circular:
            if len(loop)%2 == 1: # odd
                extend = [False, True, 0, 1, 0, 1]
            else: # even
                extend = [True, False, 0, 1, 1, 2]
        else:
            if len(loop)%2 == 1: # odd
                extend = [False, False, 0, 1, 1, 2]
            else: # even
                extend = [False, False, 0, 1, 1, 2]
        for j in range(2):
            if extend[j]:
                loop = [loop[-1]] + loop + [loop[0]]
            for i in range(extend[2+2*j], len(loop), 2):
                knots[j].append(loop[i])
            for i in range(extend[3+2*j], len(loop), 2):
                if loop[i] == loop[-1] and not circular:
                    continue
                if len(points[j]) == 0:
                    points[j].append(loop[i])
                elif loop[i] != points[j][0]:
                    points[j].append(loop[i])
            if circular:
                if knots[j][0] != knots[j][-1]:
                    knots[j].append(knots[j][0])
        if len(points[1]) == 0:
            knots.pop(1)
            points.pop(1)
        for k in knots:
            all_knots.append(k)
        for p in points:
            all_points.append(p)
    
    return(all_knots, all_points)


# calculate relative positions compared to first knot
def relax_calculate_t(mesh_mod, knots, points, regular):
    all_tknots = []
    all_tpoints = []
    for i in range(len(knots)):
        amount = len(knots[i]) + len(points[i])
        mix  = []
        for j in range(amount):
            if j%2 == 0:
                mix.append([True, knots[i][round(j/2)]])
            elif j == amount-1:
                mix.append([True, knots[i][-1]])
            else:
                mix.append([False, points[i][int(j/2)]])
        len_total = 0
        loc_prev = False
        tknots = []
        tpoints = []
        for m in mix:
            loc = mathutils.Vector(mesh_mod.vertices[m[1]].co[:])
            if not loc_prev:
                loc_prev = loc
            len_total += (loc - loc_prev).length
            if m[0]:
                tknots.append(len_total)
            else:
                tpoints.append(len_total)
            loc_prev = loc
        if regular:
            tpoints = []
            for p in range(len(points[i])):
                tpoints.append((tknots[p] + tknots[p+1]) / 2)
        all_tknots.append(tknots)
        all_tpoints.append(tpoints)
    
    return(all_tknots, all_tpoints)


# change the location of the points to their place on the spline
def relax_calculate_verts(mesh_mod, interpolation, tknots, knots, tpoints,
points, splines):
    change = []
    move = []
    for i in range(len(knots)):
        for p in points[i]:
            m = tpoints[i][points[i].index(p)]
            if m in tknots[i]:
                n = tknots[i].index(m)
            else:
                t = tknots[i][:]
                t.append(m)
                t.sort()
                n = t.index(m)-1
            if n > len(splines[i]) - 1:
                n = len(splines[i]) - 1
            elif n < 0:
                n = 0
            
            if interpolation == 'cubic':
                ax, bx, cx, dx, tx = splines[i][n][0]
                x = ax + bx*(m-tx) + cx*(m-tx)**2 + dx*(m-tx)**3
                ay, by, cy, dy, ty = splines[i][n][1]
                y = ay + by*(m-ty) + cy*(m-ty)**2 + dy*(m-ty)**3
                az, bz, cz, dz, tz = splines[i][n][2]
                z = az + bz*(m-tz) + cz*(m-tz)**2 + dz*(m-tz)**3
                change.append([p, mathutils.Vector([x,y,z])])
            else: # interpolation == 'linear'
                a, d, t, u = splines[i][n]
                if u == 0:
                    u = 1e-8
                change.append([p, ((m-t)/u)*d + a])
    for c in change:
        move.append([c[0], (mesh_mod.vertices[c[0]].co + c[1]) / 2])
    
    return(move)


##########################################
####### Space functions ##################
##########################################

# calculate relative positions compared to first knot
def space_calculate_t(mesh_mod, knots):
    tknots = []
    loc_prev = False
    len_total = 0
    for k in knots:
        loc = mathutils.Vector(mesh_mod.vertices[k].co[:])
        if not loc_prev:
            loc_prev = loc
        len_total += (loc - loc_prev).length
        tknots.append(len_total)
        loc_prev = loc
    amount = len(knots)
    t_per_segment = len_total / (amount - 1)
    tpoints = [i * t_per_segment for i in range(amount)]
    
    return(tknots, tpoints)


# change the location of the points to their place on the spline
def space_calculate_verts(mesh_mod, interpolation, tknots, tpoints, points,
splines):
    move = []
    for p in points:
        m = tpoints[points.index(p)]
        if m in tknots:
            n = tknots.index(m)
        else:
            t = tknots[:]
            t.append(m)
            t.sort()
            n = t.index(m) - 1
        if n > len(splines) - 1:
            n = len(splines) - 1
        elif n < 0:
            n = 0
        
        if interpolation == 'cubic':
            ax, bx, cx, dx, tx = splines[n][0]
            x = ax + bx*(m-tx) + cx*(m-tx)**2 + dx*(m-tx)**3
            ay, by, cy, dy, ty = splines[n][1]
            y = ay + by*(m-ty) + cy*(m-ty)**2 + dy*(m-ty)**3
            az, bz, cz, dz, tz = splines[n][2]
            z = az + bz*(m-tz) + cz*(m-tz)**2 + dz*(m-tz)**3
            move.append([p, mathutils.Vector([x,y,z])])
        else: # interpolation == 'linear'
            a, d, t, u = splines[n]
            move.append([p, ((m-t)/u)*d + a])
    
    return(move)


##########################################
####### Operators ########################
##########################################

# bridge operator
class Bridge(bpy.types.Operator):
    bl_idname = 'mesh.looptools_bridge'
    bl_label = "Bridge / Loft"
    bl_description = "Bridge two, or loft several, loops of vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    cubic_strength = bpy.props.FloatProperty(name = "Strength",
        description = "Higher strength results in more fluid curves",
        default = 1.0,
        soft_min = -3.0,
        soft_max = 3.0)
    interpolation = bpy.props.EnumProperty(name = "Interpolation mode",
        items = (('cubic', "Cubic", "Gives curved results"),
            ('linear', "Linear", "Basic, fast, straight interpolation")),
        description = "Interpolation mode: algorithm used when creating "\
            "segments",
        default = 'cubic')
    loft = bpy.props.BoolProperty(name = "Loft",
        description = "Loft multiple loops, instead of considering them as "\
            "a multi-input for bridging",
        default = False)
    loft_loop = bpy.props.BoolProperty(name = "Loop",
        description = "Connect the first and the last loop with each other",
        default = False)
    min_width = bpy.props.IntProperty(name = "Minimum width",
        description = "Segments with an edge smaller than this are merged "\
            "(compared to base edge)",
        default = 0,
        min = 0,
        max = 100,
        subtype = 'PERCENTAGE')
    mode = bpy.props.EnumProperty(name = "Mode",
        items = (('basic', "Basic", "Fast algorithm"), ('shortest',
            "Shortest edge", "Slower algorithm with better vertex matching")),
        description = "Algorithm used for bridging",
        default = 'shortest')
    remove_faces = bpy.props.BoolProperty(name = "Remove faces",
        description = "Remove faces that are internal after bridging",
        default = True)
    reverse = bpy.props.BoolProperty(name = "Reverse",
        description = "Manually override the direction in which the loops "\
            "are bridged. Only use if the tool gives the wrong result.",
        default = False)
    segments = bpy.props.IntProperty(name = "Segments",
        description = "Number of segments used to bridge the gap "\
            "(0 = automatic)",
        default = 1,
        min = 0,
        soft_max = 20)
    twist = bpy.props.IntProperty(name = "Twist",
        description = "Twist what vertices are connected to each other",
        default = 0)
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        #layout.prop(self, "mode") # no cases yet where 'basic' mode is needed
        
        # top row
        col_top = layout.column(align=True)
        row = col_top.row(align=True)
        col_left = row.column(align=True)
        col_right = row.column(align=True)
        col_right.active = self.segments != 1
        col_left.prop(self, "segments")
        col_right.prop(self, "min_width", text="")
        # bottom row
        bottom_left = col_left.row()
        bottom_left.active = self.segments != 1
        bottom_left.prop(self, "interpolation", text="")
        bottom_right = col_right.row()
        bottom_right.active = self.interpolation == 'cubic'
        bottom_right.prop(self, "cubic_strength")
        # boolean properties
        col_top.prop(self, "remove_faces")
        if self.loft:
            col_top.prop(self, "loft_loop")
        
        # override properties
        col_top.separator()
        row = layout.row(align = True)
        row.prop(self, "twist")
        row.prop(self, "reverse")
    
    def invoke(self, context, event):
        # load custom settings
        context.window_manager.looptools.bridge_loft = self.loft
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        edge_faces, edgekey_to_edge, old_selected_faces, smooth = \
            bridge_initialise(mesh, self.interpolation)
        settings_write(self)
        
        # check cache to see if we can save time
        input_method = bridge_input_method(self.loft, self.loft_loop)
        cached, single_loops, loops, derived, mapping = cache_read("Bridge",
            object, mesh, input_method, False)
        if not cached:
            # get loops
            loops = bridge_get_input(mesh)
            if loops:
                # reorder loops if there are more than 2
                if len(loops) > 2:
                    if self.loft:
                        loops = bridge_sort_loops(mesh, loops, self.loft_loop)
                    else:
                        loops = bridge_match_loops(mesh, loops)
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Bridge", object, mesh, input_method, False, False,
                loops, False, False)
        
        if loops:
            # calculate new geometry
            vertices = []
            faces = []
            max_vert_index = len(mesh.vertices)-1
            for i in range(1, len(loops)):
                if not self.loft and i%2 == 0:
                    continue
                lines = bridge_calculate_lines(mesh, loops[i-1:i+1],
                    self.mode, self.twist, self.reverse)
                vertex_normals = bridge_calculate_virtual_vertex_normals(mesh,
                    lines, loops[i-1:i+1], edge_faces, edgekey_to_edge)
                segments = bridge_calculate_segments(mesh, lines,
                    loops[i-1:i+1], self.segments)
                new_verts, new_faces, max_vert_index = \
                    bridge_calculate_geometry(mesh, lines, vertex_normals,
                    segments, self.interpolation, self.cubic_strength,
                    self.min_width, max_vert_index)
                if new_verts:
                    vertices += new_verts
                if new_faces:
                    faces += new_faces
            # make sure faces in loops that aren't used, aren't removed
            if self.remove_faces and old_selected_faces:
                bridge_save_unused_faces(mesh, old_selected_faces, loops)
            # create vertices
            if vertices:
                bridge_create_vertices(mesh, vertices)
            # create faces
            if faces:
                bridge_create_faces(mesh, faces, self.twist)
                bridge_select_new_faces(mesh, len(faces), smooth)
            # edge-data could have changed, can't use cache next run
            if faces and not vertices:
                cache_delete("Bridge")
            # delete internal faces
            if self.remove_faces and old_selected_faces:
                bridge_remove_internal_faces(mesh, old_selected_faces)
            # make sure normals are facing outside
            bridge_recalculate_normals()
        
        terminate(global_undo)
        return{'FINISHED'}


# circle operator
class Circle(bpy.types.Operator):
    bl_idname = "mesh.looptools_circle"
    bl_label = "Circle"
    bl_description = "Move selected vertices into a circle shape"
    bl_options = {'REGISTER', 'UNDO'}
    
    custom_radius = bpy.props.BoolProperty(name = "Radius",
        description = "Force a custom radius",
        default = False)
    fit = bpy.props.EnumProperty(name = "Method",
        items = (("best", "Best fit", "Non-linear least squares"),
            ("inside", "Fit inside","Only move vertices towards the center")),
        description = "Method used for fitting a circle to the vertices",
        default = 'best')
    flatten = bpy.props.BoolProperty(name = "Flatten",
        description = "Flatten the circle, instead of projecting it on the " \
            "mesh",
        default = True)
    influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    radius = bpy.props.FloatProperty(name = "Radius",
        description = "Custom radius for circle",
        default = 1.0,
        min = 0.0,
        soft_max = 1000.0)
    regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the " \
            "circle",
        default = True)
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(self, "fit")
        col.separator()
        
        col.prop(self, "flatten")
        row = col.row(align=True)
        row.prop(self, "custom_radius")
        row_right = row.row(align=True)
        row_right.active = self.custom_radius
        row_right.prop(self, "radius", text="")
        col.prop(self, "regular")
        col.separator()
                
        col.prop(self, "influence")
    
    def invoke(self, context, event):
        # load custom settings
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        settings_write(self)
        # check cache to see if we can save time
        cached, single_loops, loops, derived, mapping = cache_read("Circle",
            object, mesh, False, False)
        if cached:
            derived, mesh_mod = get_derived_mesh(object, mesh, context.scene)
        else:
            # find loops
            derived, mesh_mod, single_vertices, single_loops, loops = \
                circle_get_input(object, mesh, context.scene)
            mapping = get_mapping(derived, mesh, mesh_mod, single_vertices,
                False, loops)
            single_loops, loops = circle_check_loops(single_loops, loops,
                mapping, mesh_mod)
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Circle", object, mesh, False, False, single_loops,
                loops, derived, mapping)
        
        move = []
        for i, loop in enumerate(loops):
            # best fitting flat plane
            com, normal = calculate_plane(mesh_mod, loop)
            # if circular, shift loop so we get a good starting vertex
            if loop[1]:
                loop = circle_shift_loop(mesh_mod, loop, com)
            # flatten vertices on plane
            locs_2d, p, q = circle_3d_to_2d(mesh_mod, loop, com, normal)
            # calculate circle
            if self.fit == 'best':
                x0, y0, r = circle_calculate_best_fit(locs_2d)
            else: # self.fit == 'inside'
                x0, y0, r = circle_calculate_min_fit(locs_2d)
            # radius override
            if self.custom_radius:
                r = self.radius / p.length
            # calculate positions on circle
            if self.regular:
                new_locs_2d = circle_project_regular(locs_2d[:], x0, y0, r)
            else:
                new_locs_2d = circle_project_non_regular(locs_2d[:], x0, y0, r)
            # take influence into account
            locs_2d = circle_influence_locs(locs_2d, new_locs_2d,
                self.influence)
            # calculate 3d positions of the created 2d input
            move.append(circle_calculate_verts(self.flatten, mesh_mod,
                locs_2d, com, p, q, normal))
            # flatten single input vertices on plane defined by loop
            if self.flatten and single_loops:
                move.append(circle_flatten_singles(mesh_mod, com, p, q,
                    normal, single_loops[i]))
        
        # move vertices to new locations
        move_verts(mesh, mapping, move, -1)
        
        # cleaning up 
        if derived:
            bpy.context.blend_data.meshes.remove(mesh_mod)
        terminate(global_undo)
        
        return{'FINISHED'}


# curve operator
class Curve(bpy.types.Operator):
    bl_idname = "mesh.looptools_curve"
    bl_label = "Curve"
    bl_description = "Turn a loop into a smooth curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    boundaries = bpy.props.BoolProperty(name = "Boundaries",
        description = "Limit the tool to work within the boundaries of the "\
            "selected vertices",
        default = False)
    influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Simple and fast linear algorithm")),
        description = "Algorithm used for interpolation",
        default = 'cubic')
    regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the" \
            "curve",
        default = True)
    restriction = bpy.props.EnumProperty(name = "Restriction",
        items = (("none", "None", "No restrictions on vertex movement"),
            ("extrude", "Extrude only","Only allow extrusions (no "\
                "indentations)"),
            ("indent", "Indent only", "Only allow indentation (no "\
                "extrusions)")),
        description = "Restrictions on how the vertices can be moved",
        default = 'none')
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(self, "interpolation")
        col.prop(self, "restriction")
        col.prop(self, "boundaries")
        col.prop(self, "regular")
        col.separator()
        
        col.prop(self, "influence")
    
    def invoke(self, context, event):
        # load custom settings
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        settings_write(self)
        # check cache to see if we can save time
        cached, single_loops, loops, derived, mapping = cache_read("Curve",
            object, mesh, False, self.boundaries)
        if cached:
            derived, mesh_mod = get_derived_mesh(object, mesh, context.scene)
        else:
            # find loops
            derived, mesh_mod, loops = curve_get_input(object, mesh,
                self.boundaries, context.scene)
            mapping = get_mapping(derived, mesh, mesh_mod, False, True, loops)
            loops = check_loops(loops, mapping, mesh_mod)
        verts_selected = [v.index for v in mesh_mod.vertices if v.select \
            and not v.hide]
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Curve", object, mesh, False, self.boundaries, False,
                loops, derived, mapping)
        
        move = []
        for loop in loops:
            knots, points = curve_calculate_knots(loop, verts_selected)
            pknots = curve_project_knots(mesh_mod, verts_selected, knots,
                points, loop[1])
            tknots, tpoints = curve_calculate_t(mesh_mod, knots, points,
                pknots, self.regular, loop[1])
            splines = calculate_splines(self.interpolation, mesh_mod,
                tknots, knots)
            move.append(curve_calculate_vertices(mesh_mod, knots, tknots,
                points, tpoints, splines, self.interpolation,
                self.restriction))
        
        # move vertices to new locations
        move_verts(mesh, mapping, move, self.influence)
        
        # cleaning up 
        if derived:
            bpy.context.blend_data.meshes.remove(mesh_mod)
        
        terminate(global_undo)
        return{'FINISHED'}


# flatten operator
class Flatten(bpy.types.Operator):
    bl_idname = "mesh.looptools_flatten"
    bl_label = "Flatten"
    bl_description = "Flatten vertices on a best-fitting plane"
    bl_options = {'REGISTER', 'UNDO'}
    
    influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    plane = bpy.props.EnumProperty(name = "Plane",
        items = (("best_fit", "Best fit", "Calculate a best fitting plane"),
            ("normal", "Normal", "Derive plane from averaging vertex "\
            "normals"),
            ("view", "View", "Flatten on a plane perpendicular to the "\
            "viewing angle")),
        description = "Plane on which vertices are flattened",
        default = 'best_fit')
    restriction = bpy.props.EnumProperty(name = "Restriction",
        items = (("none", "None", "No restrictions on vertex movement"),
            ("bounding_box", "Bounding box", "Vertices are restricted to "\
            "movement inside the bounding box of the selection")),
        description = "Restrictions on how the vertices can be moved",
        default = 'none')
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(self, "plane")
        #col.prop(self, "restriction")
        col.separator()
        
        col.prop(self, "influence")
    
    def invoke(self, context, event):
        # load custom settings
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        settings_write(self)
        # check cache to see if we can save time
        cached, single_loops, loops, derived, mapping = cache_read("Flatten",
            object, mesh, False, False)
        if not cached:
            # order input into virtual loops
            loops = flatten_get_input(mesh)
            loops = check_loops(loops, mapping, mesh)
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Flatten", object, mesh, False, False, False, loops,
                False, False)
        
        move = []
        for loop in loops:
            # calculate plane and position of vertices on them
            com, normal = calculate_plane(mesh, loop, method=self.plane,
                object=object)
            to_move = flatten_project(mesh, loop, com, normal)
            if self.restriction == 'none':
                move.append(to_move)
            else:
                move.append(to_move)
        move_verts(mesh, False, move, self.influence)
        
        terminate(global_undo)
        return{'FINISHED'}


# relax operator
class Relax(bpy.types.Operator):
    bl_idname = "mesh.looptools_relax"
    bl_label = "Relax"
    bl_description = "Relax the loop, so it is smoother"
    bl_options = {'REGISTER', 'UNDO'}
    
    input = bpy.props.EnumProperty(name = "Input",
        items = (("all", "Parallel (all)", "Also use non-selected "\
                "parallel loops as input"),
            ("selected", "Selection","Only use selected vertices as input")),
        description = "Loops that are relaxed",
        default = 'selected')
    interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Simple and fast linear algorithm")),
        description = "Algorithm used for interpolation",
        default = 'cubic')
    iterations = bpy.props.EnumProperty(name = "Iterations",
        items = (("1", "1", "One"),
            ("3", "3", "Three"),
            ("5", "5", "Five"),
            ("10", "10", "Ten"),
            ("25", "25", "Twenty-five")),
        description = "Number of times the loop is relaxed",
        default = "1")
    regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the" \
            "loop",
        default = True)
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(self, "interpolation")
        col.prop(self, "input")
        col.prop(self, "iterations")
        col.prop(self, "regular")
    
    def invoke(self, context, event):
        # load custom settings
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        settings_write(self)
        # check cache to see if we can save time
        cached, single_loops, loops, derived, mapping = cache_read("Relax",
            object, mesh, self.input, False)
        if cached:
            derived, mesh_mod = get_derived_mesh(object, mesh, context.scene)
        else:
            # find loops
            derived, mesh_mod, loops = get_connected_input(object, mesh,
                context.scene, self.input)
            mapping = get_mapping(derived, mesh, mesh_mod, False, False, loops)
            loops = check_loops(loops, mapping, mesh_mod)
        knots, points = relax_calculate_knots(loops)
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Relax", object, mesh, self.input, False, False, loops,
                derived, mapping)
        
        for iteration in range(int(self.iterations)):
            # calculate splines and new positions
            tknots, tpoints = relax_calculate_t(mesh_mod, knots, points,
                self.regular)
            splines = []
            for i in range(len(knots)):
                splines.append(calculate_splines(self.interpolation, mesh_mod,
                    tknots[i], knots[i]))
            move = [relax_calculate_verts(mesh_mod, self.interpolation,
                tknots, knots, tpoints, points, splines)]
            move_verts(mesh, mapping, move, -1)
        
        # cleaning up 
        if derived:
            bpy.context.blend_data.meshes.remove(mesh_mod)
        terminate(global_undo)
        
        return{'FINISHED'}


# space operator
class Space(bpy.types.Operator):
    bl_idname = "mesh.looptools_space"
    bl_label = "Space"
    bl_description = "Space the vertices in a regular distrubtion on the loop"
    bl_options = {'REGISTER', 'UNDO'}
    
    influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    input = bpy.props.EnumProperty(name = "Input",
        items = (("all", "Parallel (all)", "Also use non-selected "\
                "parallel loops as input"),
            ("selected", "Selection","Only use selected vertices as input")),
        description = "Loops that are spaced",
        default = 'selected')
    interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Vertices are projected on existing edges")),
        description = "Algorithm used for interpolation",
        default = 'cubic')
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(self, "interpolation")
        col.prop(self, "input")
        col.separator()
        
        col.prop(self, "influence")
    
    def invoke(self, context, event):
        # load custom settings
        settings_load(self)
        return self.execute(context)
    
    def execute(self, context):
        # initialise
        global_undo, object, mesh = initialise()
        settings_write(self)
        # check cache to see if we can save time
        cached, single_loops, loops, derived, mapping = cache_read("Space",
            object, mesh, self.input, False)
        if cached:
            derived, mesh_mod = get_derived_mesh(object, mesh, context.scene)
        else:
            # find loops
            derived, mesh_mod, loops = get_connected_input(object, mesh,
                context.scene, self.input)
            mapping = get_mapping(derived, mesh, mesh_mod, False, False, loops)
            loops = check_loops(loops, mapping, mesh_mod)
        
        # saving cache for faster execution next time
        if not cached:
            cache_write("Space", object, mesh, self.input, False, False, loops,
                derived, mapping)
        
        move = []
        for loop in loops:
            # calculate splines and new positions
            if loop[1]: # circular
                loop[0].append(loop[0][0])
            tknots, tpoints = space_calculate_t(mesh_mod, loop[0][:])
            splines = calculate_splines(self.interpolation, mesh_mod,
                tknots, loop[0][:])
            move.append(space_calculate_verts(mesh_mod, self.interpolation,
                tknots, tpoints, loop[0][:-1], splines))
        
        # move vertices to new locations
        move_verts(mesh, mapping, move, self.influence)
        
        # cleaning up 
        if derived:
            bpy.context.blend_data.meshes.remove(mesh_mod)
        terminate(global_undo)
        
        return{'FINISHED'}


##########################################
####### GUI and registration #############
##########################################

# menu containing all tools
class VIEW3D_MT_edit_mesh_looptools(bpy.types.Menu):
    bl_label = "LoopTools"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("mesh.looptools_bridge", text="Bridge").loft = False
        layout.operator("mesh.looptools_circle")
        layout.operator("mesh.looptools_curve")
        layout.operator("mesh.looptools_flatten")
        layout.operator("mesh.looptools_bridge", text="Loft").loft = True
        layout.operator("mesh.looptools_relax")
        layout.operator("mesh.looptools_space")


# panel containing all tools
class VIEW3D_PT_tools_looptools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_label = "LoopTools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        lt = context.window_manager.looptools
        
        # bridge - first line
        split = col.split(percentage=0.15)
        if lt.display_bridge:
            split.prop(lt, "display_bridge", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_bridge", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_bridge", text="Bridge").loft = False
        # bridge - settings
        if lt.display_bridge:
            box = col.column(align=True).box().column()
            #box.prop(self, "mode")
            
            # top row
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            col_left = row.column(align=True)
            col_right = row.column(align=True)
            col_right.active = lt.bridge_segments != 1
            col_left.prop(lt, "bridge_segments")
            col_right.prop(lt, "bridge_min_width", text="")
            # bottom row
            bottom_left = col_left.row()
            bottom_left.active = lt.bridge_segments != 1
            bottom_left.prop(lt, "bridge_interpolation", text="")
            bottom_right = col_right.row()
            bottom_right.active = lt.bridge_interpolation == 'cubic'
            bottom_right.prop(lt, "bridge_cubic_strength")
            # boolean properties
            col_top.prop(lt, "bridge_remove_faces")
            
            # override properties
            col_top.separator()
            row = box.row(align = True)
            row.prop(lt, "bridge_twist")
            row.prop(lt, "bridge_reverse")
        
        # circle - first line
        split = col.split(percentage=0.15)
        if lt.display_circle:
            split.prop(lt, "display_circle", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_circle", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_circle")
        # circle - settings
        if lt.display_circle:
            box = col.column(align=True).box().column()
            box.prop(lt, "circle_fit")
            box.separator()
            
            box.prop(lt, "circle_flatten")
            row = box.row(align=True)
            row.prop(lt, "circle_custom_radius")
            row_right = row.row(align=True)
            row_right.active = lt.circle_custom_radius
            row_right.prop(lt, "circle_radius", text="")
            box.prop(lt, "circle_regular")
            box.separator()
            
            box.prop(lt, "circle_influence")
        
        # curve - first line
        split = col.split(percentage=0.15)
        if lt.display_curve:
            split.prop(lt, "display_curve", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_curve", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_curve")
        # curve - settings
        if lt.display_curve:
            box = col.column(align=True).box().column()
            box.prop(lt, "curve_interpolation")
            box.prop(lt, "curve_restriction")
            box.prop(lt, "curve_boundaries")
            box.prop(lt, "curve_regular")
            box.separator()
            
            box.prop(lt, "curve_influence")
        
        # flatten - first line
        split = col.split(percentage=0.15)
        if lt.display_flatten:
            split.prop(lt, "display_flatten", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_flatten", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_flatten")
        # flatten - settings
        if lt.display_flatten:
            box = col.column(align=True).box().column()
            box.prop(lt, "flatten_plane")
            #box.prop(lt, "flatten_restriction")
            box.separator()
            
            box.prop(lt, "flatten_influence")
        
        # loft - first line
        split = col.split(percentage=0.15)
        if lt.display_loft:
            split.prop(lt, "display_loft", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_loft", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_bridge", text="Loft").loft = True
        # loft - settings
        if lt.display_loft:
            box = col.column(align=True).box().column()
            #box.prop(self, "mode")
            
            # top row
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            col_left = row.column(align=True)
            col_right = row.column(align=True)
            col_right.active = lt.bridge_segments != 1
            col_left.prop(lt, "bridge_segments")
            col_right.prop(lt, "bridge_min_width", text="")
            # bottom row
            bottom_left = col_left.row()
            bottom_left.active = lt.bridge_segments != 1
            bottom_left.prop(lt, "bridge_interpolation", text="")
            bottom_right = col_right.row()
            bottom_right.active = lt.bridge_interpolation == 'cubic'
            bottom_right.prop(lt, "bridge_cubic_strength")
            # boolean properties
            col_top.prop(lt, "bridge_remove_faces")
            col_top.prop(lt, "bridge_loft_loop")
            
            # override properties
            col_top.separator()
            row = box.row(align = True)
            row.prop(lt, "bridge_twist")
            row.prop(lt, "bridge_reverse")
        
        # relax - first line
        split = col.split(percentage=0.15)
        if lt.display_relax:
            split.prop(lt, "display_relax", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_relax", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_relax")
        # relax - settings
        if lt.display_relax:
            box = col.column(align=True).box().column()
            box.prop(lt, "relax_interpolation")
            box.prop(lt, "relax_input")
            box.prop(lt, "relax_iterations")
            box.prop(lt, "relax_regular")
        
        # space - first line
        split = col.split(percentage=0.15)
        if lt.display_space:
            split.prop(lt, "display_space", text="", icon='DOWNARROW_HLT')
        else:
            split.prop(lt, "display_space", text="", icon='RIGHTARROW')
        split.operator("mesh.looptools_space")
        # space - settings
        if lt.display_space:
            box = col.column(align=True).box().column()
            box.prop(lt, "space_interpolation")
            box.prop(lt, "space_input")
            box.separator()
            
            box.prop(lt, "space_influence")


# property group containing all properties for the gui in the panel
class LoopToolsProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.looptools
    """
    
    # general display properties
    display_bridge = bpy.props.BoolProperty(name = "Bridge settings",
        description = "Display settings of the Bridge tool",
        default = False)
    display_circle = bpy.props.BoolProperty(name = "Circle settings",
        description = "Display settings of the Circle tool",
        default = False)
    display_curve = bpy.props.BoolProperty(name = "Curve settings",
        description = "Display settings of the Curve tool",
        default = False)
    display_flatten = bpy.props.BoolProperty(name = "Flatten settings",
        description = "Display settings of the Flatten tool",
        default = False)
    display_loft = bpy.props.BoolProperty(name = "Loft settings",
        description = "Display settings of the Loft tool",
        default = False)
    display_relax = bpy.props.BoolProperty(name = "Relax settings",
        description = "Display settings of the Relax tool",
        default = False)
    display_space = bpy.props.BoolProperty(name = "Space settings",
        description = "Display settings of the Space tool",
        default = False)
    
    # bridge properties
    bridge_cubic_strength = bpy.props.FloatProperty(name = "Strength",
        description = "Higher strength results in more fluid curves",
        default = 1.0,
        soft_min = -3.0,
        soft_max = 3.0)
    bridge_interpolation = bpy.props.EnumProperty(name = "Interpolation mode",
        items = (('cubic', "Cubic", "Gives curved results"),
            ('linear', "Linear", "Basic, fast, straight interpolation")),
        description = "Interpolation mode: algorithm used when creating "\
            "segments",
        default = 'cubic')
    bridge_loft = bpy.props.BoolProperty(name = "Loft",
        description = "Loft multiple loops, instead of considering them as "\
            "a multi-input for bridging",
        default = False)
    bridge_loft_loop = bpy.props.BoolProperty(name = "Loop",
        description = "Connect the first and the last loop with each other",
        default = False)
    bridge_min_width = bpy.props.IntProperty(name = "Minimum width",
        description = "Segments with an edge smaller than this are merged "\
            "(compared to base edge)",
        default = 0,
        min = 0,
        max = 100,
        subtype = 'PERCENTAGE')
    bridge_mode = bpy.props.EnumProperty(name = "Mode",
        items = (('basic', "Basic", "Fast algorithm"), ('shortest',
            "Shortest edge", "Slower algorithm with better vertex matching")),
        description = "Algorithm used for bridging",
        default = 'shortest')
    bridge_remove_faces = bpy.props.BoolProperty(name = "Remove faces",
        description = "Remove faces that are internal after bridging",
        default = True)
    bridge_reverse = bpy.props.BoolProperty(name = "Reverse",
        description = "Manually override the direction in which the loops "\
            "are bridged. Only use if the tool gives the wrong result.",
        default = False)
    bridge_segments = bpy.props.IntProperty(name = "Segments",
        description = "Number of segments used to bridge the gap "\
            "(0 = automatic)",
        default = 1,
        min = 0,
        soft_max = 20)
    bridge_twist = bpy.props.IntProperty(name = "Twist",
        description = "Twist what vertices are connected to each other",
        default = 0)
    
    # circle properties
    circle_custom_radius = bpy.props.BoolProperty(name = "Radius",
        description = "Force a custom radius",
        default = False)
    circle_fit = bpy.props.EnumProperty(name = "Method",
        items = (("best", "Best fit", "Non-linear least squares"),
            ("inside", "Fit inside","Only move vertices towards the center")),
        description = "Method used for fitting a circle to the vertices",
        default = 'best')
    circle_flatten = bpy.props.BoolProperty(name = "Flatten",
        description = "Flatten the circle, instead of projecting it on the " \
            "mesh",
        default = True)
    circle_influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    circle_radius = bpy.props.FloatProperty(name = "Radius",
        description = "Custom radius for circle",
        default = 1.0,
        min = 0.0,
        soft_max = 1000.0)
    circle_regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the " \
            "circle",
        default = True)
    
    # curve properties
    curve_boundaries = bpy.props.BoolProperty(name = "Boundaries",
        description = "Limit the tool to work within the boundaries of the "\
            "selected vertices",
        default = False)
    curve_influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    curve_interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Simple and fast linear algorithm")),
        description = "Algorithm used for interpolation",
        default = 'cubic')
    curve_regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the" \
            "curve",
        default = True)
    curve_restriction = bpy.props.EnumProperty(name = "Restriction",
        items = (("none", "None", "No restrictions on vertex movement"),
            ("extrude", "Extrude only","Only allow extrusions (no "\
                "indentations)"),
            ("indent", "Indent only", "Only allow indentation (no "\
                "extrusions)")),
        description = "Restrictions on how the vertices can be moved",
        default = 'none')
    
    # flatten properties
    flatten_influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    flatten_plane = bpy.props.EnumProperty(name = "Plane",
        items = (("best_fit", "Best fit", "Calculate a best fitting plane"),
            ("normal", "Normal", "Derive plane from averaging vertex "\
            "normals"),
            ("view", "View", "Flatten on a plane perpendicular to the "\
            "viewing angle")),
        description = "Plane on which vertices are flattened",
        default = 'best_fit')
    flatten_restriction = bpy.props.EnumProperty(name = "Restriction",
        items = (("none", "None", "No restrictions on vertex movement"),
            ("bounding_box", "Bounding box", "Vertices are restricted to "\
            "movement inside the bounding box of the selection")),
        description = "Restrictions on how the vertices can be moved",
        default = 'none')
    
    # relax properties
    relax_input = bpy.props.EnumProperty(name = "Input",
        items = (("all", "Parallel (all)", "Also use non-selected "\
                "parallel loops as input"),
            ("selected", "Selection","Only use selected vertices as input")),
        description = "Loops that are relaxed",
        default = 'selected')
    relax_interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Simple and fast linear algorithm")),
        description = "Algorithm used for interpolation",
        default = 'cubic')
    relax_iterations = bpy.props.EnumProperty(name = "Iterations",
        items = (("1", "1", "One"),
            ("3", "3", "Three"),
            ("5", "5", "Five"),
            ("10", "10", "Ten"),
            ("25", "25", "Twenty-five")),
        description = "Number of times the loop is relaxed",
        default = "1")
    relax_regular = bpy.props.BoolProperty(name = "Regular",
        description = "Distribute vertices at constant distances along the" \
            "loop",
        default = True)
    
    # space properties
    space_influence = bpy.props.FloatProperty(name = "Influence",
        description = "Force of the tool",
        default = 100.0,
        min = 0.0,
        max = 100.0,
        precision = 1,
        subtype = 'PERCENTAGE')
    space_input = bpy.props.EnumProperty(name = "Input",
        items = (("all", "Parallel (all)", "Also use non-selected "\
                "parallel loops as input"),
            ("selected", "Selection","Only use selected vertices as input")),
        description = "Loops that are spaced",
        default = 'selected')
    space_interpolation = bpy.props.EnumProperty(name = "Interpolation",
        items = (("cubic", "Cubic", "Natural cubic spline, smooth results"),
            ("linear", "Linear", "Vertices are projected on existing edges")),
        description = "Algorithm used for interpolation",
        default = 'cubic')


# draw function for integration in menus
def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_looptools")
    self.layout.separator()


# define classes for registration
classes = [VIEW3D_MT_edit_mesh_looptools,
    VIEW3D_PT_tools_looptools,
    LoopToolsProps,
    Bridge,
    Circle,
    Curve,
    Flatten,
    Relax,
    Space]


# registering and menu integration
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_func)
    bpy.types.WindowManager.looptools = bpy.props.PointerProperty(\
        type = LoopToolsProps)


# unregistering and removing menus
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    try:
        del bpy.types.WindowManager.looptools
    except:
        pass


if __name__ == "__main__":
    register()
