import maya.cmds as cmds
from rigcent_helpers import RigcentHelpers

class RigcentCurveLibrary(object):
    
    @classmethod
    def circle(cls, radius=1, name="circle_crv"):
        return cmds.circle(center=(0,0,0), normal=(0,1,0), radius=radius, name=name)[0]
        
    @classmethod
    def cube(cls, name="cube_crv"):
        return cmds.curve(degree=1,
                         point=[(1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0), (-1.0, -1.0, 1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0), (1.0, 1.0, 1.0)],
                         knot=[0,1,2,3,4,5,6,7,8,9],
                         name=name)
        
    @classmethod
    def diamond(cls, name="diamond_crv"):
        return cmds.curve(degree=1, 
                          point=[(0, 0.904618, 0), (0.65229, 0.0911447, 0), (0, -0.722329, 0), (1.28983e-09, 0.0911445, 0.65229), ( 0, 0.904618, 0 ), ( -0.65229, 0.0911447, -5.7025e-08 ), ( 0, -0.722329, 0 ), ( 8.55375e-08, 0.0911447, -0.65229 ), ( 0.65229, 0.0911447, 0 ), ( 1.28983e-09, 0.0911445, 0.65229 ), ( -0.65229, 0.0911447, -5.7025e-08 ), ( 8.55375e-08, 0.0911447, -0.65229 ), ( 0, 0.904618, 0)],
                          knot=[0,1,2,3,4,5,6,7,8,9,10,11,12],
                          name=name)
    
        
    @classmethod
    def two_way_arrow(cls, name="two_way_arrow_crv"):
        return cmds.curve(degree=1, 
                          point=[(0,0,4),(-2,0,2),(-1,0,2),(-1,0,-2),(-2,0,-2),(0,0,-4),(2,0,-2),(1,0,-2),(1,0,2),(2,0,2),(0,0,4)], 
                          knot=[0,1,2,3,4,5,6,7,8,9,10],
                          name=name)
                          
    @classmethod
    def disc(cls, radius=2, name="disc"):
        outer_circle = cls.circle(radius=radius, name="outer_circle_crv")
        RigcentHelpers.make_unselectable(outer_circle)
        
        inner_circle = cls.circle(radius=radius*0.1, name="inner_circle_crv")
        RigcentHelpers.make_unselectable(inner_circle)
        
        disc_geo = cmds.loft(outer_circle, inner_circle, uniform=True, ar=True, d=3, po=False, rsn=True, name=name)[0]
        
        outer_circle, inner_circle = cmds.parent(outer_circle, inner_circle, disc_geo)
        
        cmds.delete(outer_circle, inner_circle, disc_geo, ch=True)
        
        disc_geo_shape = RigcentHelpers.get_shape_from_transform(disc_geo)
        
        disc_shader = RigcentHelpers.create_and_assign_lambert_shader("discShader", disc_geo_shape)
        RigcentHelpers.set_attr(disc_shader, "color", [0.25, 0.66, 0.82], value_type="double3")
        RigcentHelpers.set_attr(disc_shader, "transparency", [0.75, 0.75, 0.75], value_type="double3")
        
        return disc_geo
        
if __name__ == "__main__":
    RigcentCurveLibrary.cube()
    
    # print(cmds.listRelatives("cube", c=1, s=1))
    
    cmds.ls(dag=True, ap=True, sl=True)
