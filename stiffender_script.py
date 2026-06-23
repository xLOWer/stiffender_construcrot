import bpy
import math

class BuildStiffenderProps(bpy.types.PropertyGroup):
	x0: bpy.props.FloatProperty(
			name="X",
			description="Начальная точка по X (мм)",
			default=0,
			unit='LENGTH'
		)
	y0: bpy.props.FloatProperty(
			name="Y",
			description="Начальная точка по Y (мм)",
			default=0,
			unit='LENGTH'
		)
	Ax: bpy.props.FloatProperty(
			name="Размер X",
			description="Введите размер X (мм)",
			default=10/1000,
			unit='LENGTH'
		)
	By: bpy.props.FloatProperty(
			name="Размер Y",
			description="Введите размер Y (мм)",
			default=10/1000,
			unit='LENGTH'
		)
	T: bpy.props.FloatProperty(
			name="Толщина ребра",
			description="Толщина ребра жесткости (мм)",
			default=1/1000,
			unit='LENGTH'
		)
	pieces: bpy.props.IntProperty(
			name="Размер частей",
			description="Размер частей от ширины/длины",
			default=4,
			min=4,
			max=20,
		)
	mode_fat_center: bpy.props.BoolProperty(
		name="Толстый центр",
		description="Утолщение в точке пересечения",
		default=True,
	)
	mode_square_center: bpy.props.BoolProperty(
		name="Вырез в центре",
		description="Вырез в утолщении в центре",
		default=True,
	)

class BuildStiffender(bpy.types.Operator):
	bl_idname = "wm.build_stiffender"
	bl_label = "Построить ребро жесткости"
	def execute(self, context):
		props = context.scene.BuildStiffenderProps_
		
		vertices = []
		faces = []
		
		x0 = props.x0	#начало координат по х
		y0 = props.y0	#начало координат по у
		Ax = (props.Ax)	#размер по х
		By = (props.By)	#размер по у
		T = (props.T)	#толщина ребра жесткости

		pieces=props.pieces	#на сколько частей делим всю длину/ширину чтобы дойти до ребра-квадрата

		Am = T * math.sin(math.atan(Ax / By))
		Bm = T * math.sin(math.atan(By / Ax))

		Cx1 = Ax / pieces
		Cx2 = Cx1 * (pieces-1)
		Cy1 = By / pieces
		Cy2 = Cy1 * (pieces-1)

		X1 = x0
		X2 = x0 + Am
		X3 = x0 + Cx1
		X4 = x0 + Cx1 + Am
		X5 = x0 + Cx1 + T
		X6 = x0 + Cx2 - T
		X7 = x0 + Cx2 - Am
		X8 = x0 + Cx2
		X9 = x0 + Ax - Am
		X10= x0 + Ax

		Y1 = y0
		Y2 = y0 + Bm
		Y3 = y0 + Cy1
		Y4 = y0 + Cy1 + Bm
		Y5 = y0 + Cy1 + T
		Y6 = y0 + Cy2 - T
		Y7 = y0 + Cy2 - Bm
		Y8 = y0 + Cy2
		Y9 = y0 + By - Bm
		Y10= y0 + By

		Z = 0

		vertices += [(X2, Y1, Z), (X9, Y1 ,Z), (X7, Y3 ,Z), (X4, Y3 ,Z)]; 	# A_face
		vertices += [(X1, Y2 ,Z), (X3, Y4 ,Z), (X3, Y7 ,Z), (X1, Y9 ,Z)];	# B_face
		if(props.mode_square_center):
			vertices += [(X5, Y5 ,Z), (X6, Y5 ,Z), (X6, Y6 ,Z), (X5, Y6 ,Z)];# C_face (прямоугольник-вырез)
		vertices += [(X10, Y2 ,Z), (X8, Y4 ,Z), (X8, Y7 ,Z), (X10, Y9 ,Z)];	# D_face
		vertices += [(X2, Y10 ,Z), (X9, Y10 ,Z), (X7, Y8 ,Z), (X4, Y8 ,Z)];	# E_face

		faces.append([0, 1, 2, 3]);
		faces.append([4, 5, 6, 7]);
		faces.append([8, 9, 10, 11]);
		faces.append([12, 13, 14, 15]);
		if(props.mode_square_center):
			faces.append([16, 17, 18, 19]);

		mesh_name = "Ребра жесткости"
		obj_name = "Ребра жесткости"
		mesh_data = bpy.data.meshes.new(mesh_name)
		obj = bpy.data.objects.new(obj_name, mesh_data)
		mesh_data.from_pydata(vertices, [], faces)
		mesh_data.update()
		bpy.context.collection.objects.link(obj)
		
# 2. Создание кнопки на панели
class BuildStiffender_Panel(bpy.types.Panel):
	bl_label = "Жесткость"
	bl_idname = "BuildStiffender"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Ребра жесткости"

	def draw(self, context):
		layout = self.layout
		props = context.scene.BuildStiffenderProps_
		# Добавление кнопки оператора
		layout.operator(BuildStiffender.bl_idname, text="Создать")
		layout.prop(props, "x0")
		layout.prop(props, "y0")
		layout.prop(props, "Ax")
		layout.prop(props, "By")
		layout.prop(props, "T")
		layout.prop(props, "pieces")
		layout.prop(props, "mode_fat_center")
		layout.prop(props, "mode_square_center")

classes = (
	BuildStiffenderProps,
	BuildStiffender,
	BuildStiffender_Panel,
)

# 3. Регистрация в Blender
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Scene.BuildStiffenderProps_ = bpy.props.PointerProperty(type=BuildStiffenderProps)

def unregister():
	for cls in classes:
		bpy.utils.register_class(cls)
	del bpy.types.Scene.BuildStiffenderProps_

if __name__ == "__main__":
	register()
