#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <iterator>
#include <sys/time.h>
#include "mm_helper.cpp"
#include <set>

int main(int argc, char **argv) {

	char *tmpchar;
	std::ofstream output_file("Weights.csv");

    if (argc == 2) {
        tmpchar = argv[1]; // Graph inputfile
    } else {
        fprintf(stderr, "You did something wrong!\n");
        exit(1);
    }

    CSR csr = read_matrix_market_to_CSR(tmpchar);
    printf("Graph: %s, nodes: %d, edges: %d\n", tmpchar, csr.nrows, csr.nnz);

    int num_blocks = std::ceil(csr.nrows / 64);
    std::vector<int> offset(csr.nrows);

    for (int i = 0; i < csr.nrows; i++)
    	offset[i] = i;

    int start = 0, count = 1, end;
    int step = std::ceil(csr.nrows / 8);

    std::vector<std::vector<float>> weights;

    while (count <= num_blocks) {
    	std::vector<float> weight;
    	if (count < num_blocks) {
    		start = (count - 1) * std::ceil(csr.nrows / num_blocks);
        	end = start + std::ceil(csr.nrows / num_blocks);
        } else {
        	start = (num_blocks - 1) * std::ceil(csr.nrows / num_blocks);
        	end = csr.nrows;
        }
		int mc1 = 0;
		int mc2 = 0;
		int mc3 = 0;
		int mc4 = 0;
		int mc5 = 0;
		int mc6 = 0;
		int mc7 = 0;
		int mc8 = 0;
		

    	for (int i = start; i < end; i ++) {
    		int node = offset[i];
    		std::vector<int> neighbors(csr.row_indx[node + 1] - csr.row_indx[node]);
    		for (int j = csr.row_indx[node]; j < csr.row_indx[node + 1]; j++) 
    			neighbors.push_back(csr.col_id[j]);
    		for (auto neighbor: neighbors) {

    			if (neighbor < start or neighbor > end) {

    				if (neighbor <= step)
                    	mc1 += 1;
                	if (neighbor > step & neighbor <= 2 * step)
                    	mc2 += 1;
                	if (neighbor > 2 * step & neighbor <= 3 * step)
                    	mc3 += 1;
                	if (neighbor > 3 * step & neighbor <= 4 * step)
                    	mc4 += 1;
                	if (neighbor > 4 * step & neighbor <= 5 * step)
                    	mc5 += 1;
                	if (neighbor > 5 * step & neighbor <= 6 * step)
                    	mc6 += 1;
                	if (neighbor > 6 * step & neighbor <= 7 * step)
                    	mc7 += 1;
                	if (neighbor > 7 * step)
                    	mc8 += 1;	
    			}

    		}
    	}

    	int total = mc1 + mc2 + mc3 + mc4 + mc5 + mc6 + mc7 + mc8 + 1;
    	weight.push_back(float(mc1) / float(total));
    	weight.push_back(float(mc2) / float(total));
    	weight.push_back(float(mc3) / float(total));
    	weight.push_back(float(mc4) / float(total));
    	weight.push_back(float(mc5) / float(total));
    	weight.push_back(float(mc6) / float(total));
    	weight.push_back(float(mc7) / float(total));
    	weight.push_back(float(mc8) / float(total));

    	count += 1;

    	weights.push_back(weight);
    	std::ostream_iterator<float> output_iterator(output_file, ",");
    	std::copy(weight.begin(), weight.end(), output_iterator);
    	output_file << "\n";
    }


    
    

    return 0;
}