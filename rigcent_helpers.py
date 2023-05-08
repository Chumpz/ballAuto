import maya.cmds as cmds


class RigcentHelpers(object):
    
    @classmethod
    def add_attr(cls, node, long_name, attr_type, default_value, keyable=False):
        cmds.addAttr(node, longName=long_name, defaultValue=default_value, attributeType=attr_type, keyable=keyable)
    
    @classmethod
    def set_attr(cls, node, attr, value, value_type=None):
        if value_type:
            #expect a list that will be unpacked for the command
            cmds.setAttr("{0}.{1}".format(node, attr), *value, type=value_type)
        else:
            cmds.setAttr("{0}.{1}".format(node, attr), value)
            
    @classmethod
    def connect_attr(cls, node_a, attr_a, node_b, attr_b, force=False):
        cmds.connectAttr("{0}.{1}".format(node_a, attr_a), "{0}.{1}".format(node_b, attr_b), force=force)
        
    @classmethod
    def disconnect_attr(cls, node_a, attr_a, node_b, attr_b):
        cmds.disconnectAttr("{0}.{1}".format(node_a, attr_a), "{0}.{1}".format(node_b, attr_b))
        
    @classmethod
    def lock_and_hide_attr(cls, node, attrs, hide=True, lock=True, channelBox=False):
        keyable = not hide
        
        for attr in attrs:
            full_name = "{0}.{1}".format(node, attr)
            cmds.setAttr(full_name, keyable=keyable, lock=lock, channelBox=channelBox)
            
    @classmethod
    def make_unselectable(cls, transform_node):
        shape_node =  cls.get_shape_from_transform(transform_node)
        
        cls.set_attr(shape_node, "overrideEnabled", True)
        cls.set_attr(shape_node, "overrideDisplayType", 2)
            
    @classmethod
    def create_display_layer(cls, name, members, reference=False):
        display_layer = cmds.createDisplayLayer(name=name, empty=True)
        
        if reference:
            cmds.setAttr("{0}.displayType".format(display_layer), 2)
            
        if members:
            cmds.editDisplayLayerMembers(display_layer, members, noRecurse=True)
        
        return display_layer
        
    @classmethod
    def create_and_assign_lambert_shader(cls, name, shape_node):
        shader = cmds.shadingNode("lambert", name=name, asShader=True)
        shader_sg = cmds.sets(name="{0}SG".format(shader), renderable=True, noSurfaceShader=True, empty=True)
        
        cls.connect_attr(shader, "outColor", shader_sg, "surfaceShader")
        
        cmds.sets([shape_node], e=True, forceElement=shader_sg)
        
        return shader
        
    @classmethod
    def get_shape_from_transform(cls, transform_node):
        return cmds.listRelatives(transform_node, shapes=True, fullPath=True)[0]