for i in $(seq 0 9)
do
  #awk 'NR % 10 == '$i ../1kset/gaussian_points.csv > sample_$i.csv

  python ../gen_xml.py sample_$i.csv 10000000 > model_$i.xml 
  ../../../StochKit/ssa -m model_$i.xml -t 10 -r 10 -i 100 --label
  mv *output IA10/
  tail -n1 IA10/model_${i}_output/stats/means.txt > result_${i}.txt

  python ../gen_xml.py sample_$i.csv 20000000 > model_$i.xml 
  ../../../StochKit/ssa -m model_$i.xml -t 10 -r 10 -i 100 --label
  mv *output IA20/
  tail -n1 IA20/model_${i}_output/stats/means.txt >> result_${i}.txt

  python ../gen_xml.py sample_$i.csv 50000000 > model_$i.xml 
  ../../../StochKit/ssa -m model_$i.xml -t 10 -r 10 -i 100 --label
  mv *output IA50/
  tail -n1 IA50/model_${i}_output/stats/means.txt >> result_${i}.txt

  python ../gen_xml.py sample_$i.csv 100000000 > model_$i.xml 
  ../../../StochKit/ssa -m model_$i.xml -t 10 -r 10 -i 100 --label
  mv *output IA100/
  tail -n1 IA100/model_${i}_output/stats/means.txt >> result_${i}.txt

  python parse.py result_${i}.txt | sort -nk4 > ratio_${i}.txt
done
