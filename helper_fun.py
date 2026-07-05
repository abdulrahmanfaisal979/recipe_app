def filter_recipe(df,filter_option,filter_value):
    '''
    Filters the recipe dataframe based on the selected filter option and value.
    Takes three values:
        - df: Recipe dataframe.
        - filter_option: Category to filter by
        - filter_value: Selected value for filtering.
        
    returns one value
        - df_filtered: Filtered dataframe

    '''
    # df[df.ing_lst.str.contains('ing')]
    if filter_option=="Food Ratings":
        if filter_value=='1 ⭐':
            the_filter= df.food_rating==1
        elif filter_value=='2 ⭐':
            the_filter= df.food_rating==2
        elif filter_value=='3 ⭐':
            the_filter= df.food_rating==3
        elif filter_value=='4 ⭐':
            the_filter= df.food_rating==4
        elif filter_value=='5 ⭐':
            the_filter= df.food_rating==5
            
    elif filter_option=="Ingredients":
        the_filter=df.ing_lst.str.contains(filter_value)
        

    elif filter_option=='Preparation Time':
        if filter_value=='0-15 mins':
            the_filter= (df.prep_time>=0) & (df.prep_time<15)
        elif filter_value=='15-30 mins':
            the_filter= (df.prep_time>=15) & (df.prep_time<30)
        elif filter_value=='30-45 mins':
            the_filter= (df.prep_time>=30) & (df.prep_time<45)
        elif filter_value=='45-60 mins':
            the_filter= (df.prep_time>=45) & (df.prep_time<60)
        elif filter_value=='More than 60 mins':
            the_filter= (df.prep_time>=60)

    elif filter_option=="Difficulty":
        the_filter=df.difficulty_level==filter_value
        

    else:
        filtered_df=df

    
    filtered_df=df[the_filter]
    return filtered_df


def sort_recipe(df,sort_option,sort_value):
    '''
    sorts the recipe dataframe based on the selected sort option and value.
    Takes three values:
        - df: Recipe dataframe.
        - filter_option: Category to sort by
        - filter_value: ascending or descending.
        
    returns one value
        - df_filtered: sorted dataframe

    '''
    if sort_option=="Highest Ratings":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='food_rating', ascending=True) 
            return sorted_df
        else:
            sorted_df=df.sort_values(by='food_rating', ascending=False)
            return sorted_df
            
            
    
    if sort_option=="Recipe Name":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='recipe_name', ascending=True)
            return sorted_df
        else:
            sorted_df=df.sort_values(by='recipe_name', ascending=False)
            return sorted_df
    
    if sort_option=="Ingredients":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='ing_lst', ascending=True)
            return sorted_df
        else:
            sorted_df=df.sort_values(by='ing_lst', ascending=False)
            return sorted_df
            
    if sort_option=="Difficulty Level":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='difficulty_level', ascending=True)
            return sorted_df
        else:
            sorted_df=df.sort_values(by='difficulty_level', ascending=False)
            return sorted_df
            
    if sort_option=="Preparation Time":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='prep_time', ascending=True)
            return sorted_df
        else:
            sorted_df=df.sort_values(by='prep_time', ascending=False)
            return sorted_df
            
    if sort_option=="Date Added":
        if sort_value=="A to Z":
            sorted_df=df.sort_values(by='time_now', ascending=True)
            return sorted_df
        else:
            sorted_df=df.sort_values(by='time_now', ascending=False)
            return sorted_df


    else:
        sorted_df=df
        return sorted_df





def gen_shop_lst(filtered_df, serv_now):
    '''
    Generates an adjusted ingredient list based on the desired serving size.

    Takes 2 values:
        filtered_df: Dataframe containing the selected recipe.
        serv_now: Desired number of servings.

    Returns 1 value:
        new_quant: Ingredient list with quantities adjusted.
    '''
    lsts=filtered_df['ing_lst'][0].split(" ")
    serv_size=filtered_df.serv_size[0]
    new_lsts=[]
    for i in lsts: 
        try:
            i=str(float(i)*(serv_now/serv_size))
        except:
            pass
        new_lsts.append(i)
        
    new_quant=' '.join(new_lsts)

    return new_quant
            
                
                   
    

