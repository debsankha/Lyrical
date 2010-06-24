/*  
    Hardy-Weinberg Simulation
	Simulates the effect of drift and population size and
	investigates the Hardy-Weinberg equilibrium. This
	program generates the data which is later used by hwgame.

    Copyright (C) 2007-2008	Abhishek Dasgupta
		  2007-2008	Sambit Bikas Pal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// Evolve Hardy Weinberg game
// Assuming 2 alleles per loci only.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>

float sf=0.5;
int childindex=0, pop=1000, offspring=10; // defaults.
#define MAXPOP 10000
#ifndef LOCI
	#define LOCI 10
#endif

//void shuffle(int gen[MAXPOP][LOCI][2]);
void mother(int gen[MAXPOP][LOCI][2]);
void mate(int gen_n1[MAXPOP][LOCI][2], int gen_n2[MAXPOP][LOCI][2]);
void allele_freq_count(int gen[MAXPOP][LOCI][2], float allele_freq[LOCI]);
void genome(int gen[MAXPOP][LOCI][2]);
void genomeind(int gen[MAXPOP][LOCI][2], int i);

int main(int argc, char* argv[]) {

	srand(time(NULL));
	int i, nog = 10; // no of generation
	for(i = 1; i < argc; i++) {
		switch(i) {
			case 1:
			pop = atoi(argv[1]);
			break;
			
			case 2:
			offspring = atoi(argv[2]);
			break;
			
			case 3:
			nog = atoi(argv[3]);
			break;

			case 4:
			sf = atof(argv[4]);
			break;
			
			default:
			printf("Syntax: pop offs nog\n");
		}
	}
	int gen_n1[MAXPOP][LOCI][2];
	int gen_n2[MAXPOP][LOCI][2];
	int matings=pop/offspring;
	float allelefreq[LOCI];
	FILE* fp;
	fp = fopen("/tmp/evohw.dat","w"); // gnuplot data file...
	int h,k,mm;
	
	// initialise allelefreq.
	mother(gen_n1);
	int ll;
	
	for(i=0; i < nog; i++) {
		childindex = 0;
		// allele frequencies
		//genome(gen_n1);
		for(ll=0;ll < LOCI;ll++) allelefreq[ll]=0.00;
		//printf("%d ", i);
		fprintf(fp,"%d ",i);
		allele_freq_count(gen_n1, allelefreq);
		for(ll=0; ll < LOCI; ll++)	{
			//printf("%f ", allelefreq[ll]);
			fprintf(fp, "%f ", allelefreq[ll]);
		}
		fprintf(fp,"\n");
		//printf("\n");
		for(mm=0;mm < matings; mm++) mate(gen_n1, gen_n2);
		// copy n2 to n1
		for(h = 0;h < MAXPOP; h++) {
			for(k = 0; k < LOCI; k++) {
				gen_n1[h][k][0] = gen_n2[h][k][0];
				gen_n1[h][k][1] = gen_n2[h][k][1];
			}
		}	
	}	
	return 0;
}

void mother(int gen[MAXPOP][LOCI][2]) {
	// create the initial "mother" population
	int h,k,l;
	for(h = 0; h < pop; h++) {
		for(k = 0; k < LOCI; k++) {
			for(l = 0; l < 2; l++)
				gen[h][k][l] = 
				(rand() / ((double)RAND_MAX + 1)) > (1-sf) ? 1: 0;
		}
	}
}			

void genome(int gen[MAXPOP][LOCI][2]) {
	// print chromosomal sequences of gen.
	int i,j,k;
	for(i = 0; i < pop; i++) {
		for(j = 0; j < 2; j++) {
			for(k = 0; k < LOCI; k++)
				printf("%d",gen[i][k][j]);
			printf(",");
		}
		printf("\n");
	}
}
void genomeind(int gen[MAXPOP][LOCI][2], int in) {
	// print chromosomal sequences of gen.
	int j,k;
	for(j = 0; j < 2; j++) {
		for(k = 0; k < LOCI; k++)
			printf("%d",gen[in][k][j]);
		printf(",");
	}
	printf("\n");
}
void mate(int gen_n1[MAXPOP][LOCI][2], int gen_n2[MAXPOP][LOCI][2]){
	// create generation n2 from n1
	// choose two random individiuals
	int rand1, rand2;
	rand1 = rand()/(int)(((double)RAND_MAX + 1) / pop);
	rand2 = rand()/(int)(((double)RAND_MAX + 1) / pop);
	//printf("mating between %d and %d\n", rand1, rand2);
	//genomeind(gen_n1, rand1); genomeind(gen_n1, rand2);
	int temploci,i; // i is the ith offspring in one mating.
	int xx1,xx2;	
	for(i=0;i < offspring && childindex < pop;i++){
		
		for(temploci=0;temploci < LOCI;temploci++){
			// we must choose between 0 and 1 here, to pick
			// from the parent.
			xx1 = (rand() / ((double)RAND_MAX + 1)) > 0.5 ? 1: 0;
			xx2 = (rand() / ((double)RAND_MAX + 1)) > 0.5 ? 1: 0;

			//printf("rand %d %d\n", xx1,xx2);
			gen_n2[childindex][temploci][0]= 
			gen_n1[rand1][temploci][xx1];
			//printf("chose %d from %d for %d locus\n", 
			//		gen_n2[childindex][temploci][0], rand1, temploci);
			gen_n2[childindex][temploci][1]= 
			gen_n1[rand2][temploci][xx2];
			//printf("chose %d from %d for %d locus\n", 
			//		gen_n2[childindex][temploci][0], rand2, temploci);
		}
		//printf("offspring %d:", i);
		//genomeind(gen_n2, childindex);
		childindex++;
	}
	return;
}

//void shuffle(int gen[MAXPOP][LOCI][2]){

void allele_freq_count(int gen[MAXPOP][LOCI][2],float allele_freq[LOCI]){
	int i,j;
	for(i=0; i< pop ; i++){
		for(j=0;j<LOCI;j++)
			allele_freq[j] += (gen[i][j][0] + gen[i][j][1])/(float)(2.0* pop);
	}
}

