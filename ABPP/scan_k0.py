#!/usr/bin/env python
import sys, os
from string import Template
from math import log10, pow

template = """
<Model>
   <Description>cys</Description>
   <NumberOfReactions>3</NumberOfReactions>
   <NumberOfSpecies>8</NumberOfSpecies>
   <ParametersList>
     <Parameter>
       <Id>k1</Id>
       <Expression>0.0001</Expression>
     </Parameter>
     <Parameter>
       <Id>k2</Id>
       <Expression>0.00001</Expression>
     </Parameter>
     <Parameter>
       <Id>k0</Id>
       <Expression>$k0</Expression>
     </Parameter>
     <Parameter>
       <Id>IA</Id>
       <Expression>$IA</Expression>
     </Parameter>
   </ParametersList>
   <ReactionsList>
     <Reaction>
       <Id>R1</Id>
       <Description> a+b->c+d </Description>
       <Type>mass-action</Type>
       <Rate>k1</Rate>
       <Reactants>
           <SpeciesReference id="a" stoichiometry="1"/>
           <SpeciesReference id="b" stoichiometry="1"/>
       </Reactants>
       <Products>
           <SpeciesReference id="c" stoichiometry="1"/>
           <SpeciesReference id="d" stoichiometry="1"/>
       </Products>
     </Reaction>
     <Reaction>
       <Id>R2</Id>
       <Description> A+b->C+d </Description>
       <Type>mass-action</Type>
       <Rate>k0</Rate>
       <Reactants>
           <SpeciesReference id="A" stoichiometry="1"/>
           <SpeciesReference id="b" stoichiometry="1"/>
       </Reactants>
       <Products>
           <SpeciesReference id="C" stoichiometry="1"/>
           <SpeciesReference id="d" stoichiometry="1"/>
       </Products>
     </Reaction>
     <Reaction>
       <Id>R3</Id>
       <Description> m+b->M+d </Description>
       <Type>mass-action</Type>
       <Rate>k2</Rate>
       <Reactants>
           <SpeciesReference id="m" stoichiometry="1"/>
           <SpeciesReference id="b" stoichiometry="1"/>
       </Reactants>
       <Products>
           <SpeciesReference id="M" stoichiometry="1"/>
           <SpeciesReference id="d" stoichiometry="1"/>
       </Products>
     </Reaction>
  </ReactionsList>
  <SpeciesList>
     <Species>
       <Id>a</Id>
       <Description>Species a</Description>
       <InitialPopulation>1000</InitialPopulation>
     </Species>
     <Species>
       <Id>b</Id>
       <Description>Species b</Description>
       <InitialPopulation>IA</InitialPopulation>
     </Species>
     <Species>
       <Id>c</Id>
       <Description>Species c</Description>
       <InitialPopulation>0</InitialPopulation>
     </Species>
     <Species>
       <Id>d</Id>
       <Description>Species d</Description>
       <InitialPopulation>0</InitialPopulation>
     </Species>
     <Species>
       <Id>A</Id>
       <Description>Species A</Description>
       <InitialPopulation>100000</InitialPopulation>
     </Species>
     <Species>
       <Id>C</Id>
       <Description>Species C</Description>
       <InitialPopulation>0</InitialPopulation>
     </Species>
     <Species>
       <Id>m</Id>
       <Description>Species m</Description>
       <InitialPopulation>2000</InitialPopulation>
     </Species>
     <Species>
       <Id>M</Id>
       <Description>Species M</Description>
       <InitialPopulation>0</InitialPopulation>
     </Species>
  </SpeciesList>
</Model>
"""

xmltemplate = Template(template)

#k0=0.0000001 - 0.00001
#logk0 = -6 ~ -4
#IA=10000, 100000

def sim_R( k0 ):
    scr = { 'k0': k0, 'IA': 10000 }
    xml = xmltemplate.substitute( scr )
    fp1 = open("tmp1.xml", 'w')
    fp1.write(xml)
    fp1.close()
    os.system("../../StochKit/ssa -m tmp1.xml -t 20 -r 10 -i 0 -f --species c C M")
    scr = { 'k0': k0, 'IA': 100000 }
    xml = xmltemplate.substitute( scr )
    fp2 = open("tmp2.xml", 'w')
    fp2.write(xml)
    fp2.close()
    os.system("../../StochKit/ssa -m tmp2.xml -t 20 -r 10 -i 0 -f --species c C M")

    fp1 = open("tmp1_output/stats/means.txt", 'r')
    fp2 = open("tmp2_output/stats/means.txt", 'r')
    line1 = fp1.readlines()[0].split()
    line2 = fp2.readlines()[0].split()

    print("k0=", log10(float(k0)), float(line2[1])/float(line1[1]), float(line2[2])/float(line1[2]), float(line2[3])/float(line1[3]))


for logk in [-5.0, -5.2, -5.4, -5.6, -5.8, -6, -6.4, -6.8, -7.2, -8]:
    sim_R( pow(10.0, logk) )
