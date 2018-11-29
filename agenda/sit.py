from swiglpk import *


#returns the index of the column corresponding to g(j,i)
def col_index_g(guest,table,nb_tables):
	return (guest - 1) * nb_tables + (table - 1) + 1;


#returns the index of the column corresponding to p(j,k,i)
def col_index_p(guestj,guestk,tablei,nb_tables, nb_guests):
	return nb_guests*nb_tables + ((guestj - 1)*nb_guests + (guestk - 1))*nb_tables + (tablei - 1) + 1;


# returns an array of ints valled assignements, such that assignements[i] = t means that guest i should sit at table t
def sitting(event, tables):
    group = len(event.attendees.members.all())
    nb_tables = len(tables)
    affection = event.attendees.relationship_matrix()

    if(sum(tables) < group):
        return None

    lp = glp_create_prob();  # create the problem
    glp_set_prob_name(lp, "Sitting arrangement");
    glp_set_obj_dir(lp, GLP_MAX);  # indicated that we want to maximize
    nb_col = group * nb_tables + group * group * nb_tables;  # number of variables
    glp_add_cols(lp, nb_col);  # add the right number of columns

    # Set the variables names and bounds (for the g(j,i) columns)
    for j in range(1, group + 1):
        for i in range(1, nb_tables + 1):
            index = col_index_g(j, i, nb_tables);
            glp_set_obj_coef(lp, index, 0);
            glp_set_col_kind(lp, index, GLP_BV);

    # Set the variables names and bounds (for the p(j,k,i) columns)
    for j in range(1, group + 1):
        for k in range(1, group + 1):
            for i in range(1, nb_tables + 1):
                index = col_index_p(j, k, i, nb_tables, group);
                if(j != k):
                    glp_set_obj_coef(lp, index, affection[j - 1][
                    k - 1] + 10); # added +10 to the coefficients to make them positive (going from [-10,10] to [0,20])
                else:
                    glp_set_obj_coef(lp, index, 10);
                glp_set_col_kind(lp, index, GLP_BV);

    # ADD CONSTRAINTS #

    row_counter = 0;

    # Makes sure every person is seated at exactly one table
    for j in range(1, group + 1):
        glp_add_rows(lp, 1);
        row_counter = row_counter + 1
        glp_set_row_bnds(lp, row_counter, GLP_FX, 1.0, 1.0);
        indexes = intArray(1 + nb_tables)
        coef = doubleArray(1 + nb_tables);
        for i in range(1, nb_tables + 1):
            indexes[i] = col_index_g(j, i, nb_tables);
            coef[i] = 1;
        glp_set_mat_row(lp, row_counter, nb_tables, indexes, coef);

    # Makes sure the number of people at a given table doesn't exceed its capacity
    for i in range(1, nb_tables + 1):
        glp_add_rows(lp, 1);
        row_counter = row_counter + 1;
        glp_set_row_bnds(lp, row_counter, GLP_DB, 0.0, tables[i - 1]);
        indexes = intArray(1 + group);
        coef = doubleArray(1 + group);

        for j in range(1, group + 1):
            indexes[j] = col_index_g(j, i, nb_tables);
            coef[j] = 1;
        glp_set_mat_row(lp, row_counter, group, indexes, coef);

    # Constraints to linarize the whole problem (p(j,k,i) = g(j,i)*g(k,i)) (first set of constraints)
    for i in range(1, nb_tables + 1):
        for k in range(1, group + 1):
            glp_add_rows(lp, 1);
            row_counter = row_counter + 1
            glp_set_row_bnds(lp, row_counter, GLP_UP, 0.0, 0.0);
            indexes = intArray(1 + group + 1);
            coef = doubleArray(1 + group + 1);
            for j in range(1, group + 1):
                indexes[j] = col_index_p(j, k, i, nb_tables, group);
                coef[j] = 1;
            indexes[group + 1] = col_index_g(k, i, nb_tables);
            coef[group + 1] = -tables[i - 1];
            glp_set_mat_row(lp, row_counter, group + 1, indexes, coef);

    # Constraints to linarize the whole problem (p(j,k,i) = g(j,i)*g(k,i))	(second set of constraints)
    for i in range(1, nb_tables + 1):
        for j in range(1, group + 1):
            glp_add_rows(lp, 1);
            row_counter = row_counter + 1;
            glp_set_row_bnds(lp, row_counter, GLP_UP, 0.0, 0.0);
            indexes = intArray(1 + group + 1);
            coef = doubleArray(1 + group + 1);
            for k in range(1, group + 1):
                indexes[k] = col_index_p(j, k, i, nb_tables, group);
                coef[k] = 1;
            indexes[group + 1] = col_index_g(j, i, nb_tables);
            coef[group + 1] = -tables[i - 1];
            glp_set_mat_row(lp, row_counter, group + 1, indexes, coef);

    glp_simplex(lp, None);  # first solve using the simplex method

    # for(size_t c= 1; c <= group*nb_tables; ++c){
    #	double val = glp_get_col_prim(lp,c);
    #	const char * n = glp_get_col_name(lp,c);
    #	printf("%s",n);
    #	printf(" = %g \n",val);
    # }

    glp_intopt(lp, None);  # then optimize using the intopt method

    status = glp_mip_status(lp);

    if(status == GLP_NOFEAS):
        glp_delete_prob(lp);
        return None
    # prepares the result array containing the corresponding tables for each guest
    assignements = intArray(group);
    for j in range(1, group + 1):
        for i in range(1, nb_tables + 1):
            if (glp_mip_col_val(lp, col_index_g(j, i, nb_tables)) == 1):
                assignements[j - 1] = i;

    glp_delete_prob(lp);
    return assignements;

