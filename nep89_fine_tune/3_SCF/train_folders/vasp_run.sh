#!/bin/bash
# 文件名: vasp_run.sh
echo "=== 顺序执行VASP作业（2核并行）==="
for dir in */; do
    dir=${dir%/}
    echo "正在处理: $dir"
    
    # 检查必要文件（INCAR、POSCAR、POTCAR、KPOINTS）
    if [ ! -f "$dir/INCAR" ] || [ ! -f "$dir/POSCAR" ] || [ ! -f "$dir/POTCAR" ] || [ ! -f "$dir/KPOINTS" ]; then
        echo "  跳过 - 缺少输入文件"
        continue
    fi
    
    # 检查是否已完成（存在OUTCAR且包含"Voluntary"关键字）
    if [ -f "$dir/OUTCAR" ] && grep -q "Voluntary" "$dir/OUTCAR" 2>/dev/null; then
        echo "  跳过 - 已完成"
        continue
    fi
    
    # 进入目录并运行VASP（2核并行）
    cd "$dir"
    echo "  开始运行..."
    mpirun -np 2 vasp_std
    echo "  运行结束"
    cd ..
    
    echo "等待 3 秒..."
    sleep 3
done
echo "所有作业处理完毕!"