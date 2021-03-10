#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <iterator>
#include <sys/time.h>
#include "mm_helper.cpp"
#include <set> 


double gettime() {
  struct timeval t;
  gettimeofday(&t,NULL);
  return t.tv_sec+t.tv_usec*1e-6;
}

typedef struct score_blocks_t {

	int block_num;
	float score;

} score_block;

bool doCompareScore(score_block elem1, score_block elem2)
{
    if (elem1.score < elem2.score) {
        return true;
    }
    return false;
}


float scoreBlock(CSR csr, int start, int end, int choice) {
	
	if (choice == 1) {
		float num = 0.0;
		float den = csr.row_indx[end + 1] - csr.row_indx[start]; 

		for (int i = csr.row_indx[start]; i < csr.row_indx[end + 1]; i++) {
			if (csr.col_id[i] >= start && csr.col_id[i] <= end)
				num ++;
		}

		return num / (den + 1);
	}
	else {
		std::set<int, std::greater<int> > s;
		float nnz = csr.row_indx[end + 1] - csr.row_indx[start];
		for (int i = csr.row_indx[start]; i < csr.row_indx[end + 1]; i++) {
			s.insert(csr.col_id[i]);
		}
		return nnz / ((float)s.size() + 1);
	}
	
}

std::vector<int> shuffle_csr(CSR csr, int num_nodes, int num_edges, int choice) {
	
	int num_blocks = (num_nodes / 64) + 1;
	int count = 1;
	int start = 0;
	int end = 0;

	score_block *scores;
	std::vector<int> reorder;
	std::vector<float> blockscores;

	scores = (score_block *)malloc(sizeof(score_block) * num_blocks);

	// while(count <= num_blocks) {
	// #pragma omp parallel num_threads(8)
	for (count = 1; count <= num_blocks; count++) {

		if (count < num_blocks) {
			
			start = (count - 1) * (num_nodes / num_blocks + 1);
			end = start + (num_nodes / num_blocks ) ;
			scores[count - 1].block_num = count - 1;
			scores[count - 1].score = scoreBlock(csr, start, end, choice);
			// printf("%d %d ", start, end);
		}
		else {
			
			start = (num_blocks - 1) * (num_nodes / num_blocks + 1);
			end = num_nodes - 1;
			scores[count - 1].block_num = count - 1;
			scores[count - 1].score = scoreBlock(csr, start, end, choice);
			// printf("%d %d ", start, end);
		}
	}

	std::stable_sort(scores, scores + num_blocks, doCompareScore);

	// printf("%f", scoreBlock_EdgeDensity(csr, 4, 7));
	for (int i = 0; i < num_blocks; i++){
		blockscores.push_back(scores[i].score);
		// printf("%f ", scores[i].score);
		// printf("%d ", scores[i].block_num);
	}

	for (int i = 0; i < num_blocks; i++) {
		// printf("%d ", scores[i].block_num);
		int s = i * (num_nodes / num_blocks + 1);
		int beg = scores[i].block_num * (num_nodes / num_blocks + 1);
		int fin = beg + (num_nodes / num_blocks + 1) - 1;
		if (fin > (num_nodes - 1))
			fin = num_nodes - 1;

		// // printf("%d %d\n", beg, fin);
		// printf("%d ", s);
		for (int j = beg; j <= fin; j++) {
			reorder.push_back(j);
		}
	}

	// for (int i = 0; i < num_nodes; i++) {
	// printf("%d ", int(reorder.size()));
	// }
	return reorder;
	// return blockscores;
}


int main(int argc, char **argv) {

	char *tmpchar;
	int choice = 1; // 1 for edge density, 0 for column density

    if (argc == 3) {
        tmpchar = argv[1]; // Graph inputfile
        choice = atoi(argv[2]);
    } else {
        fprintf(stderr, "You did something wrong!\n");
        exit(1);
    }

    CSR csr = read_matrix_market_to_CSR(tmpchar);
    printf("Graph: %s, nodes: %d, edges: %d\n", tmpchar, csr.nrows, csr.nnz);

    double time = gettime();
    std::vector<int> r = shuffle_csr(csr, csr.nrows, csr.nnz, choice);
    printf("%lf",(gettime() - time ));
    // printf("%d", int(r.size()));

    std::ofstream output_file("reorder.txt");
    std::ostream_iterator<int> output_iterator(output_file, "\n");
    std::copy(r.begin(), r.end(), output_iterator);

    // for (int i = 0; i < csr.nrows + 1; i ++)
    // 	printf("%d ",csr.row_indx[i]);

    // printf("\n");

    // for (int i = 0; i < csr.nnz; i ++)
    // 	printf("%d ",csr.col_id[i]);

	return 0;
}
    