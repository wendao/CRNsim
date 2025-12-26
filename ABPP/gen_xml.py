import xml.etree.ElementTree as ET
from xml.dom import minidom
from math import pow

def generate_chemical_model(k_values, a_initials, IA_value=1e8):
    # 创建根节点
    model = ET.Element("Model")
    
    # 基础信息
    num_reactions = len(k_values)
    num_species = (num_reactions * 2) + 2  # 每个反应有一对 A_n/C_n，外加公共的 b 和 d
    
    ET.SubElement(model, "Description").text = "Generated Multi-Reaction Model"
    ET.SubElement(model, "NumberOfReactions").text = str(num_reactions)
    ET.SubElement(model, "NumberOfSpecies").text = str(num_species)

    # 1. Reactions List
    reactions_list = ET.SubElement(model, "ReactionsList")
    for i in range(1, num_reactions + 1):
        rxn = ET.SubElement(reactions_list, "Reaction")
        ET.SubElement(rxn, "Id").text = f"R{i}"
        ET.SubElement(rxn, "Description").text = f"A{i}+b->C{i}+d"
        ET.SubElement(rxn, "Type").text = "mass-action"
        ET.SubElement(rxn, "Rate").text = str(k_values[i-1])
        
        # Reactants: Ai + b
        reacs = ET.SubElement(rxn, "Reactants")
        ET.SubElement(reacs, "SpeciesReference", id=f"A{i}", stoichiometry="1")
        ET.SubElement(reacs, "SpeciesReference", id="b", stoichiometry="1")
        
        # Products: Ci + d
        prods = ET.SubElement(rxn, "Products")
        ET.SubElement(prods, "SpeciesReference", id=f"C{i}", stoichiometry="1")
        ET.SubElement(prods, "SpeciesReference", id="d", stoichiometry="1")

    # 2. Species List
    species_list = ET.SubElement(model, "SpeciesList")
    
    # 公共物种 b 和 d
    for s_id, pop in [("b", IA_value), ("d", 0)]:
        spec = ET.SubElement(species_list, "Species")
        ET.SubElement(spec, "Id").text = s_id
        ET.SubElement(spec, "Description").text = f"Common Species {s_id}"
        ET.SubElement(spec, "InitialPopulation").text = str(int(pop))

    # 循环生成的物种 Ai 和 Ci
    for i, a_pop in enumerate(a_initials, 1):
        # Species Ai
        spec_a = ET.SubElement(species_list, "Species")
        ET.SubElement(spec_a, "Id").text = f"A{i}"
        ET.SubElement(spec_a, "Description").text = f"Species A{i}"
        ET.SubElement(spec_a, "InitialPopulation").text = str(a_pop)
        
        # Species Ci
        spec_c = ET.SubElement(species_list, "Species")
        ET.SubElement(spec_c, "Id").text = f"C{i}"
        ET.SubElement(spec_c, "Description").text = f"Species C{i}"
        ET.SubElement(spec_c, "InitialPopulation").text = "0"

    # 美化 XML 输出
    xml_str = ET.tostring(model, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    pretty_xml = pretty_xml.replace("&gt;", ">")
    return pretty_xml

# --- 使用示例 ---
#k_array = [0.0001, 0.00005, 0.00001]      # 反应速率常数数组
#a_init_array = [1000, 5000, 100000]       # A1, A2, A3 的初值数组

import sys

k_array = []
a_init_array = []
sum_a = 0
lines = open(sys.argv[1], 'r').readlines()
for l in lines:
    es = l.strip().split(',')
    x = float(es[0])
    y = float(es[1])
    if y-x >= 7: continue #skip highhigh
    logk = -3.5 - x * 0.5
    logN = 2.8 + y * 0.4
    k = pow(10, logk)
    N = round(pow(10, logN))
    #print(k, N)
    k_array.append(k)
    a_init_array.append(N)
    sum_a += N

# 打印或保存到文件
xml_output = generate_chemical_model(k_array, a_init_array, int(sys.argv[2]))
print(xml_output)
print(sum_a, file=sys.stderr)
