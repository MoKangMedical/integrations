#!/bin/bash
echo "🔗 MoKangMedical 集成中心"
echo "========================="
python3 -m py_compile src/hub.py && echo "✅ hub.py"
mkdir -p output
echo "✅ 部署完成"
