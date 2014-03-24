neig=(3 10 20)
its=(20 200 1000)

for i in ${neig[@]}
do
	for j in ${its[@]}
	do
		python testMain.py VivaldiMatrix.txt $i $j >> results.txt
	done
done
