import maya.cmds as cmds
import maya.mel as mel
from rigcent_helpers import RigcentHelpers
from rigcent_curve_library import RigcentCurveLibrary


class BallAutoRig(object):
    def __init__(self):
        self.primary_color = [0.0, 1.0, 0.0]
        self.secondary_color = [1.0, 1.0, 0.0]
        
    def set_colors(self, primary, secondary):
        self.primary_color = primary
        self.secondary_color = secondary
        
    def construct_rig(self, name="ball"):
        cmds.select(clear=True)
        
        root_grp = cmds.group(name=name, empty=True, world=True)
        anim_controls_grp = cmds.group(name="anim_controls", empty=True, parent=root_grp)
        geometry_grp = cmds.group(name="geo_DO_NOT_TOUCH", empty=True, parent=anim_controls_grp)
        
        ball_geo = self.create_ball("ball_geo", parent=geometry_grp)
        ball_ctrl = self.create_ball_rigg("ball_ctrl", parent=anim_controls_grp)
        
        cmds.parentConstraint(ball_ctrl, ball_geo, maintainOffset=True, weight=1)
        
        squash_grp = cmds.group(name="squash_grp", empty=True, parent=anim_controls_grp)
        squash_ctrl = self.create_squash_ctrl("squash_ctrl", parent=squash_grp)
        
        cmds.pointConstraint(ball_ctrl, squash_grp, offset=[0,0,0], weight=1)
        
        self.create_squash_deformer(ball_geo, squash_ctrl)
        
        RigcentHelpers.create_display_layer("ball_geometry", [ball_geo], True)
        
    def create_ball(self, name, parent=None):
        ball_geo = cmds.sphere(pivot=(0,0,0), axis=(0,1,0), radius=1, name=name)[0]
        if parent:
            ball_geo = cmds.parent(ball_geo, parent)[0]
        
        self.create_ball_shader(ball_geo)
            
        return ball_geo
        
    def create_ball_shader(self, ball_geo):
        ball_shape = RigcentHelpers.get_shape_from_transform(ball_geo)
        ball_shader = RigcentHelpers.create_and_assign_lambert_shader("ballShader", ball_shape)
        
        ramp = cmds.shadingNode("ramp", name="ballRamp", asTexture=True)
        RigcentHelpers.set_attr(ramp, "colorEntryList[0].color", self.primary_color, value_type="double3")
        RigcentHelpers.set_attr(ramp, "colorEntryList[0].position", 0.0)
        RigcentHelpers.set_attr(ramp, "colorEntryList[1].color", self.secondary_color, value_type="double3")
        RigcentHelpers.set_attr(ramp, "colorEntryList[1].position", 0.5)
        RigcentHelpers.set_attr(ramp, "interpolation", 0.0)
        
        place2d_util = cmds.shadingNode("place2dTexture", name="ballPlace2dTexture", asUtility=True)
        RigcentHelpers.set_attr(place2d_util, "repeatU", 1)
        RigcentHelpers.set_attr(place2d_util, "repeatV", 3)
        
        RigcentHelpers.connect_attr(place2d_util, "outUV", ramp, "uv")
        RigcentHelpers.connect_attr(place2d_util, "outUvFilterSize", ramp, "uvFilterSize")
        
        RigcentHelpers.connect_attr(ramp, "outColor", ball_shader, "color")    
        
    def create_ball_rigg(self, name, parent=None):
        ball_ctrl = RigcentCurveLibrary.two_way_arrow(name=name)
        if parent:
            ball_ctrl = cmds.parent(ball_ctrl, parent)[0]
            
        RigcentHelpers.lock_and_hide_attr(ball_ctrl, ["sx", "sy", "sz", "v"])
        RigcentHelpers.set_attr(ball_ctrl, "rotateOrder", 3)
            
        return ball_ctrl
        
    def create_squash_ctrl(self, name, parent=None):
        squash_ctrl = RigcentCurveLibrary.disc(radius=1.6, name=name)
        if parent:
            squash_ctrl = cmds.parent(squash_ctrl, parent)[0]
        
        RigcentHelpers.lock_and_hide_attr(squash_ctrl, ["sx", "sy", "sz", "v"])
        RigcentHelpers.set_attr(squash_ctrl, "rotateOrder", 3)
        RigcentHelpers.add_attr(squash_ctrl, "squashStretch", "double", 0, keyable=True)
        
        return squash_ctrl
        
    def create_squash_deformer(self, squash_obj, squash_ctrl):
        cmds.select(squash_obj, replace=True)
        cmds.Squash()
        
        squash_handle, squash_deformer = cmds.ls(sl=True, long=True)
        
        squash_handle = cmds.rename(squash_handle, "ball_squash")
        
        RigcentHelpers.set_attr(squash_handle, "visibility", False)
        RigcentHelpers.lock_and_hide_attr(squash_handle, ["v"], hide=False)
        
        cmds.parent(squash_handle, squash_ctrl)
        
        RigcentHelpers.connect_attr(squash_ctrl, "squashStretch", squash_deformer, "factor", force=True)
        
        cmds.select(clear=True)
        
        
if __name__ == "__main__":     
    
    from ball_auto_rig_ui import BallAutoRigUi 
    ballUi = BallAutoRigUi()
    ballUi.show()
    
    
