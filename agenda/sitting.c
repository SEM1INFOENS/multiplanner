/* sitting.c */
#include <stdio.h>
#include <stdlib.h>
#include <glpk.h>

/*Executing :
 * gcc -c sitting.c
 * gcc sitting.o -lglpk -lm
 * ./a.out
 */

//returns the index of the column corresponding to g(j,i)
int col_index_g(int guest,int table,size_t nb_tables){
	return (guest - 1) * nb_tables + (table - 1) + 1;
}

//returns the index of the column corresponding to p(j,k,i)
int col_index_p(int guestj,int guestk,int tablei,size_t nb_tables, size_t nb_guests){
    return nb_guests*nb_tables + ((guestj - 1)*nb_guests + (guestk - 1))*nb_tables + (tablei - 1) + 1;
}

//returns an array of ints valled assignements, such that assignements[i] = t means that guest i should sit at table t
int* sitting(size_t group,int affection[group][group],int* tables,size_t nb_tables){
	
	glp_prob *lp;
	lp = glp_create_prob();//create the problem
	glp_set_prob_name(lp,"Sitting arrangement");
    glp_set_obj_dir(lp, GLP_MAX);//indicated that we want to maximize
    size_t nb_col = group*nb_tables + group*group*nb_tables;//number of variables
    glp_add_cols(lp, nb_col); //number of variables
    
    //Set the variables names and bounds (for the g(j,i) columns)
    for(size_t j = 1; j <= group; ++j){
		for(size_t i = 1; i <= nb_tables; ++i){
			size_t index = col_index_g(j,i,nb_tables);
			char *name = malloc(125);
            sprintf(name, "g(%zu,%zu)", j, i);
			glp_set_col_name(lp, index, name);
			glp_set_obj_coef(lp, index, 0);
			glp_set_col_kind(lp, index, GLP_BV);
		}
	}
	
	//Set the variables names and bounds (for the p(j,k,i) columns)		
	for(size_t j = 1; j <= group; ++j){
		for(size_t k = 1; k <= group;++k){
			for(size_t i = 1; i <= nb_tables; ++i){
				size_t index = col_index_p(j,k,i,nb_tables,group);
				char *name = malloc(125);
				sprintf(name, "p(%zu,%zu,%zu)", j, k, i);
				glp_set_col_name(lp, index, name);
				glp_set_obj_coef(lp, index, affection[j-1][k-1]);
				glp_set_col_kind(lp, index, GLP_BV);
			}
		}			
	}
		
		
	/* ADD CONSTRAINTS */	
		
	size_t row_counter = 0;
	
	//Makes sure every person is seated at exactly one table
	for(size_t j = 1; j <= group; ++j){
		glp_add_rows(lp,1);
		++row_counter;
		glp_set_row_bnds(lp,row_counter,GLP_FX,1.0,1.0);
		int indexes[1 + nb_tables];
		double coef[1 + nb_tables];
		for(size_t i = 1; i <= nb_tables; ++i){
			indexes[i] = col_index_g(j,i,nb_tables);
			coef[i] = 1;
		}
		glp_set_mat_row(lp,row_counter,nb_tables,indexes,coef);	
	}	
	
	//Makes sure the number of people at a given table doesn't exceed its capacity
	for(size_t i = 1; i <= nb_tables;++i){
		glp_add_rows(lp,1);
		++row_counter;
		glp_set_row_bnds(lp,row_counter,GLP_DB,0.0,tables[i-1]);
		int indexes[1 + group];
		double coef[1 + group];
		for(size_t j = 1; j<= group;++j){
			indexes[j] = col_index_g(j,i,nb_tables);
			coef[j] = 1;
		}
		glp_set_mat_row(lp,row_counter,group,indexes,coef);
	}
		
	//Constraints to linarize the whole problem (p(j,k,i) = g(j,i)*g(k,i)) (first set of constraints)	
	for(size_t i = 1; i <= nb_tables; ++i){
		for(size_t k = 1; k <= group; ++k){
			glp_add_rows(lp,1);
			++row_counter;
			glp_set_row_bnds(lp,row_counter,GLP_UP,0.0,0.0);
			int indexes[1 + group + 1];
		    double coef[1 + group + 1];
		    for(size_t j = 1; j <= group;++j){
				indexes[j] = col_index_p(j,k,i,nb_tables,group);
				coef[j] = 1;
			}
			indexes[group + 1] = col_index_g(k,i,nb_tables);
			coef[group + 1] = -tables[i-1];
			glp_set_mat_row(lp,row_counter,group + 1,indexes,coef);
		}
	}	
	
	//Constraints to linarize the whole problem (p(j,k,i) = g(j,i)*g(k,i))	(second set of constraints)
	for(size_t i = 1; i <= nb_tables; ++i){
		for(size_t j = 1; j <= group; ++j){
			glp_add_rows(lp,1);
			++row_counter;
			glp_set_row_bnds(lp,row_counter,GLP_UP,0.0,0.0);
			int indexes[1 + group + 1];
		    double coef[1 + group + 1];
		    for(size_t k = 1; k <= group; ++k){
				indexes[k] = col_index_p(j,k,i,nb_tables,group);
				coef[k] = 1;
			}
			indexes[group + 1] = col_index_g(j,i,nb_tables);
			coef[group + 1] = -tables[i-1];
			glp_set_mat_row(lp,row_counter,group + 1,indexes,coef);
		}
	}		
		
		
	glp_simplex(lp, NULL);//first solve using the simplex method
	glp_intopt(lp,NULL);//then optimize using the intopt method
	
	/*printf("%d\n",glp_intopt(lp,NULL));
    printf("happiness mip: %lf\n",glp_mip_obj_val(lp));
    for(size_t c= 1; c <= group*nb_tables; ++c){
		double val = glp_mip_col_val(lp,c);
		if(val == 1){
		const char * n = glp_get_col_name(lp,c);
		printf("%s",n);
		printf(" = %g \n",val);
		}
	}*/
    
    //prepares the result array containing the corresponding tables for each guest
    int *assignements  = malloc(sizeof(int)*group);
	for(size_t j = 1; j <= group; ++j){
		for(size_t i = 1; i<=nb_tables;++i){
			if(glp_mip_col_val(lp,col_index_g(j,i,nb_tables)) == 1){
				assignements[j - 1] = i;
			}
		}
	}
	
	glp_delete_prob(lp);//deletes the problem	
    return assignements;	
}

/*void test(int to_test){
	if(to_test == 0){
		printf("ERROR\n");
	}else{
		printf("PASS\n");
	}
}

int main(void)
{ 
   	
  //CASE  : 1 guest, 1 table
  size_t nb_guests = 1;
  size_t nb_tables = 1;
  int affection1[1][1] = {{0}};
  int tables1[1] = {1};
  int* a = sitting(nb_guests,affection1,tables1,nb_tables);
  test(a[0] == 1);
  printf("\n");
  
  //CASE 2 : 3 guests, 2 tables 	
  nb_guests = 3;
  nb_tables = 2;
  int affection2[3][3] = {{0,2,10},{5,0,1},{8,-1,0}};
  int tables[2] = {2,2};
  a = sitting(nb_guests,affection2,tables,nb_tables);
  for(size_t i = 0; i < 3;++i){
	  printf("%d\n",a[i]);
  }
  test(a[0] == a[2]);
  test(a[1] != a[0]);
  test(a[2] != a[1]);
  printf("\n");
 
  //CASE 3 : 4 guests, 2 tables
  nb_guests = 4;
  int affection3[4][4] = {{0,5,8,-6},{2,0,-10,10},{9,-5,0,3},{10,8,1,0}};
  a = sitting(nb_guests,affection3,tables,nb_tables);
  test(a[0] == a[2]);
  test(a[1] == a[3]);
  test(a[0] != a[1]);
  printf("\n");
  for(size_t i = 0; i < 4;++i){
	  printf("%d\n",a[i]);
  }
  
  return 0;	
}*/
