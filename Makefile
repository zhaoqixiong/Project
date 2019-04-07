BUILD_DIR = results

Extract_SCRIPT = ./feature.py
Csv = ./results/machinelearning.csv


Tree = ./decisiontree.py
Decision = ./results/tree.txt

Runtime =  ./runtime.py
Json = ./results/runtime.json
Action = ./action.txt


build: 
	mkdir results

class:
	$(Extract_SCRIPT) -i $(M) -o $(Csv) -c $(C) 

	
tree:
	$(Tree) -i $(Csv) -o $(Decision)

runtime:
	$(Runtime) -i1 $(Decision) -i2 $(Action) -o $(Json)
	

clean: 
	rm -rf $(BUILD_DIR) 

	
      
