from ase.io import read, write
from ase import Atoms
model = read("model.xyz")
model_cell = model.get_cell()
repeat_x = 2  #设定扩胞倍数,需考虑源文件实际尺寸
repeat_y = 2
repeat_z = 1
new_model = model.repeat((repeat_x,repeat_y,repeat_z))
new_model.set_pbc([True,True,True])
write('new_model.extxyz',new_model)
