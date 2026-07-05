import streamlit as st
import pandas as pd
import datetime
import helper_fun as h

df=pd.read_csv(r"C:\Users\HP\Downloads\Book1.csv")
df_cook_history=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\cook_history.csv")

###                         ###

df['time_now']=df.time_now.astype('datetime64[ns]')
date_filt=df.time_now.dt.month==datetime.datetime.now().month
add_this_month=df[date_filt]

df_cook_history['date_cooked']=df_cook_history.date_cooked.astype('datetime64[ns]')
date_filter=df_cook_history.date_cooked.dt.month==datetime.datetime.now().month
cook_this_month=df_cook_history[date_filter]

fav_rec_series=df_cook_history.recipe_now.value_counts()
fav_rec_name=fav_rec_series.index[0]
fav_rec_name1=fav_rec_series.index[1]
fav_rec_name2=fav_rec_series.index[2]

oldest_lst=df_cook_history.drop_duplicates(keep='last', subset='recipe_now',ignore_index=True).head(3)

df_cook_history_recent=(df_cook_history.tail(3)) 
col=["Recipe Name", "Serving Size", "Date cooked"]
df_cook_history_recent.columns=["Recipe Name", "Serving Size", "Date cooked"]
df_cook_history_recent['Date cooked'] = df_cook_history_recent['Date cooked'].dt.date

###                        ###


with st.sidebar:
    st.title('Menu')
    r_button= st.radio('',['Home','Add Recipe', 'Search Recipes', 'Cook Now Calculator'])


if r_button=='Home':
    st.title('The Recipe Manager')
    st.subheader('Your kitchen companion')
    st.divider()
    st.subheader('Highlights')
    
    col1, col2,col3 = st.columns(3)
    col1.metric("Total No. of Recipes", len(df.recipe_name), border=True)
    col2.metric("New Recipes added this month", len(add_this_month), border=True)
    col3.metric("No. of recipes cooked this month", len(cook_this_month), border=True)
        
    col4, col5 = st.columns(2)
    with col4.container(border=True):
        st.write("Your favourite Recipes: ")
        st.write("-", fav_rec_name)
        st.write("-", fav_rec_name1)
        st.write("-", fav_rec_name2)

    
    with col5.container(border=True):
        st.write("Recipes you haven't cooked for a long time:")
        st.write("-", oldest_lst.recipe_now[0])
        st.write("-", oldest_lst.recipe_now[1])
        st.write("-", oldest_lst.recipe_now[2])
    
    

    st.divider()
    
    st.subheader('Recently cooked')
    st.table(df_cook_history_recent,width="stretch", hide_index=True, border="horizontal")



if r_button=='Add Recipe':
    
    st.title("Add your new recipe here")
    
    with st.form("my_form"):
        
        left1,right1=st.columns(2)
        
        
        recipe_name = left1.text_input("The Recipe Name", "")
        serv_size = right1.number_input("The serving size is:", min_value=1 )
        
        
        recipe_desc = st.text_input("Recipe Description", "")
        
        
        recipe_cat = st.selectbox(
            "Recipe Category",
            ("Breakfast", "Lunch", "Dinner","Dessert"), index=None, placeholder="Select recipe category...",
                                                        )

        st.space()
        with st.container(border=True):
            left2, center, right2=st.columns(3)
            left2.write('The food rating is:')
            food_rating = ["1.0", "2.0", "3.0", "4.0", "5.0"]
            selected_food_rating = left2.feedback("stars")

    
            difficulty_level = right2.radio(
        "The difficulty level is:",
        ["Easy", "Medium", "Hard"],
    )
        st.space()
        prep_time = st.slider("Preparation Time (in mins) is:", 0, 200, step=5)
        

        ing_lst=st.text_input("The ingredients are:", placeholder="eg: 3 slices cheese, 0.5 tbsp salt, etc...")

           
    
        cook_steps = st.text_area("Cooking steps:",placeholder="1. \n2. \n3. \n4.")

        cook_notes = st.text_area("Any other notes",placeholder="eg: Cut to small pieces, etc...")
  
    
        submitted = st.form_submit_button("Add Recipe")

        
        time_now = datetime.datetime.now().date()
            
        dic={
            "recipe_name":[recipe_name],
            'recipe_desc':[recipe_desc], 
            'recipe_cat': [recipe_cat],
            'serv_size' : [serv_size],
            'food_rating':[selected_food_rating],
            'ing_lst': [ing_lst],
            'prep_time':[prep_time],
            'difficulty_level':[difficulty_level],
            'cook_steps':[cook_steps],
            'cook_notes':[cook_notes], 
            'time_now' : [time_now],
            }

        new_row=pd.DataFrame(dic)
        if submitted:
            df=pd.concat([df, new_row], ignore_index=True)
            df.to_csv(r"C:\Users\HP\Downloads\Book1.csv", index=False)

            st.write(new_row)

    
if r_button=='Search Recipes':
    st.title('Search Recipes')
    col7, col8, col9, col10 = st.columns(4)

    filter_option=col7.selectbox(
    "Filter By:",
    ("Food Ratings","Ingredients", "Preparation Time", "Difficulty"), index=None, placeholder="Select filter category...",
)

    if filter_option=="Food Ratings":
        filter_value=col8.selectbox("Value",('1 ⭐','2 ⭐','3 ⭐','4 ⭐','5 ⭐'),index=None, placeholder="Select filter value...", )
        if filter_value!=None:
            df_filtered=h.filter_recipe(df,filter_option,filter_value)
        else:
            df_filtered=df
    
        
    elif filter_option=="Ingredients":
        filter_value=col8.selectbox("Value",('cheese','milk','rice','butter','salt','oil','sugar','flour','tomato','carrot'),index=None, placeholder="Select filter value...",) # make this dynamic
        if filter_value!=None:
            df_filtered=h.filter_recipe(df,filter_option,filter_value) 
        else:
            df_filtered=df # also allow more than 1 option
        
          
    elif filter_option=="Preparation Time":
        filter_value=col8.selectbox("Value",("0-15 mins",'15-30 mins','30-45 mins','45-60 mins','More than 60 mins'),index=None, placeholder="Select filter value...",)
        if filter_value!=None:
            df_filtered=h.filter_recipe(df,filter_option,filter_value)
        else:
            df_filtered=df 
        

    elif filter_option=="Difficulty":
        filter_value=col8.selectbox("Value",("Easy",'Medium','Hard'),index=None, placeholder="Select filter value...",)
        if filter_value!=None:
            df_filtered=h.filter_recipe(df,filter_option,filter_value)
        else:
            df_filtered=df 

    else:
        df_filtered=df 
        
       
    sort_option=col9.selectbox(
    "Sort By:",
    ("Highest Ratings","Recipe Name","Ingredients", "Difficulty Level", "Preparation Time","Date Added"),index=None, placeholder="Select sort category",)
    
    if sort_option!=None:
        sort_value=col10.selectbox(
        "Sort Order:",
        ("A to Z","Z to A", ),index=None, placeholder="Select sort value...",)
    
        df_filtered=h.sort_recipe(df_filtered,sort_option,sort_value)


## https://stackoverflow.com/questions/15902835/changing-iteration-variable-inside-for-loop-in-python
    dic_card={}
    for i in range(0,len(df_filtered),1):
        df_filtered.reset_index(drop=True, inplace=True)
        dic_card[f"card{i}"] = st.container(border=True)
        dic_card[f"card{i}"].header(df_filtered.recipe_name[i])
        dic_card[f"card{i}"].write(df_filtered.recipe_desc[i])
        dic_card[f"card{i}"].write(f"Preparation Time: {df_filtered.prep_time[i]}")
        dic_card[f"card{i}"].write(f"Difficulty:      {df_filtered.difficulty_level[i]}")
        dic_card[f"card{i}"].write(f"Ingredients: {df_filtered.ing_lst[i]}")
             
        
recipe_name_lst=[i for i in df.recipe_name]

recipe_name_lst.insert(0,"I'm not sure, generate randomly for me")


if r_button=='Cook Now Calculator':
    st.title("Let's start cooking")
    
    recipe_now=st.selectbox(
    "What would you like to cook today?",
    (recipe_name_lst), index=None, placeholder="Select recipe...",
)
    if recipe_now=="I'm not sure, generate randomly for me":
        serv_now = st.number_input("For how many people?", min_value=1 )
        filtered_df=df.sample()
        filtered_df.reset_index(drop=True, inplace=True)
        st.write(f"Random recipe: {filtered_df.recipe_name[0]}") 
        shopping_lst=h.gen_shop_lst(filtered_df, serv_now)
        check_lst = shopping_lst.split(",")
        
    elif recipe_now!=None:
        serv_now = st.number_input("For how many people?", min_value=1 )
    
        filtered_df=df[df.recipe_name==recipe_now]
        filtered_df.reset_index(drop=True, inplace=True) 
        shopping_lst=h.gen_shop_lst(filtered_df, serv_now)
        check_lst = shopping_lst.split(",")
        
    else:
        filtered_df=df
        serv_now = st.number_input("For how many people?", min_value=1 )
        shopping_lst=h.gen_shop_lst(filtered_df, serv_now)
        check_lst = shopping_lst.split(",")
    
    st.divider()
    st.subheader(f"The shopping list is:")

    
# https://stackoverflow.com/questions/15902835/changing-iteration-variable-inside-for-loop-in-python
    d = {}
    for i in range(len(check_lst)):
        d[f"string{i}"] = st.checkbox(check_lst[i])

    date_cooked = datetime.datetime.now().date()
    
    cook_history_dic={
                "recipe_now":[recipe_now], 
                'serv_now' : [serv_now], 
                'date_cooked':[date_cooked]
                }
    
    new_cooked_row=pd.DataFrame(cook_history_dic)
    
    st.space()
    st.space()

    left, middle, right = st.columns(3)
    if middle.button("DONE COOKING", type="primary", width="stretch"):
        st.write(f"{recipe_now} has been added to your cooking history")
        df_cook_history=pd.concat([df_cook_history, new_cooked_row], ignore_index=True)
        df_cook_history.to_csv(r"C:\Users\HP\OneDrive\Desktop\cook_history.csv", index=False)
    
