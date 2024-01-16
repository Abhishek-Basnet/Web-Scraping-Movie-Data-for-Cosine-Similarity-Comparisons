#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Data Extraction from web page "www.metacritic.com" :
import requests
from bs4 import BeautifulSoup

hyperlink_list = []
movie_name_list=[]
movie_dic={}
headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
for i in range(1, 50): #for loop is used here to loop through the page from 1 to 49 to extract the movie link available in the page,range has been increased to account the loss of movies due to dynamic nature.
    y = str(i)
    x = 'https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2023&page=' + y #adds a changing part in the web address
    fhand = requests.get(x, headers=headers)
    soup = BeautifulSoup(fhand.content, "html.parser")
    hyperlinks = soup.find_all('a', class_='c-finderProductCard_container g-color-gray80 u-grid')
    
    for link in hyperlinks: # the extracted text on the above hyperlink list is passed through for loop to extract the link of each movie
        href = link.get('href')
        full_url = 'https://www.metacritic.com' + href #link remaining part is added to make it functional
        hyperlink_list.append(full_url)

for j in hyperlink_list: #for loop is used to iterate through the list movies hyperlink from which the movie name and link of view all page is extracted
    movie_page = requests.get(j, headers = headers)
    movie_page_soup = BeautifulSoup(movie_page.content, "html.parser")
    movie_name_datalist = movie_page_soup.find_all('div', class_ = "c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium")
    for i in movie_name_datalist: # extracted data is runed through for loop to extract the movie name
        movie_name=i.get_text().strip()
        
    view_all = movie_page_soup.find_all('a', class_ = "c-globalHeader_viewMore g-color-gray50 g-text-xxsmall u-text-uppercase")
    for i in view_all: # with the link of view all page the table of credit table list is extracted 
        view_all_link = 'https://www.metacritic.com' + i['href']
        view_all_page = requests.get(view_all_link, headers = headers)
        view_all_soup = BeautifulSoup(view_all_page.content, "html.parser")

        credit_tables_list = view_all_soup.find_all('div', class_ = "c-productCredits g-outer-spacing-bottom-xlarge")
        director_namelist=[] 
        cast_name_list = []
        subkey={}
        for i in credit_tables_list: #inside the credit table list director and cast tables names are extracted
            if "Directed By" in i.get_text().strip(): #looks for the specific "Directed By" table content
                director_names = i.find_all('a')
                for j in director_names: #extracts the directors name from the table
                    director_names=j.get_text().strip()
                    director_namelist.append(director_names)
            table_title=i.find ("h3")
            if table_title.get_text().strip()=="Cast" : 
            #if "Cast" in i.get_text().strip():
                cast_names = i.find_all('a')
                for j in cast_names:
                    cast_name = j.get_text().strip()
                    cast_name_list.append(cast_name)


        director=tuple(director_namelist)
        subkey[director]=cast_name_list
    movie_dic[movie_name]=subkey
print(len(movie_dic)) 


# In[ ]:


#Data importing into CSV file:
import csv

# Define the header for the CSV file
header = ['Movie Title', 'Director(s)', 'Cast']

# Open the CSV file in write mode
with open('Abhishek_Basnet_movies.csv', mode='w', newline='') as movie_file:  # line 1
    # Create a CSV writer object
    movie_writer = csv.writer(movie_file)  # line 2
    
    # Write the header to the CSV file
    movie_writer.writerow(header)
    
    # Iterate through the dictionary and write each movie's information to the CSV file
    for key1, value1 in movie_dic.items():
        for key2, value2 in value1.items():
            # Join the lists of directors and cast members into strings
            cast_namelist = ', '.join(value2)
            directors_namelist = ', '.join(key2)
            
            # Write the movie information to the CSV file
            movie_writer.writerow([key1, directors_namelist, cast_namelist])


# In[ ]:


# Analysis of Data:
import math

# Function to calculate the dot product of two vectors
def dot_product(A, B): 
    return sum(x * y for x, y in zip(A, B))

# Function to calculate the magnitude of a vector
def magnitude(v): 
    return math.sqrt(sum(x**2 for x in v))

# Function to calculate the cosine similarity between two vectors
def cosine_similarity(A, B):
    dot_prod = dot_product(A, B)
    mag_1 = magnitude(A)
    mag_2 = magnitude(B)
        
    if mag_1 == 0 or mag_2 == 0:
        return 0  # Avoid division by zero
    
    return dot_prod / (mag_1 * mag_2)

# Initialize a variable to check if the input movie or director is not found
notfound = 0

# Get user input for what to check on Metacritic
choice = input('What do you want to check on Metacrtitics? (Please choose ‘movie’, ‘director’, or ‘comparison’ \n Input:')

# Check if the user wants to check information about a movie
if choice.lower().strip() == 'movie':
    choice1 = input('Which movie do you want to check?:')
    while True: 
        # Loop through the movie dictionary to find the specified movie
        for key1, value1 in movie_dic.items():
            for key2, value2 in value1.items():
                if key1.lower().strip() == choice1.lower().strip():
                    print('The director of the movie', key1 , 'is  \n',' , '.join(key2))
                    print('The cast of the movie', key1 , 'includes  \n', ' , '.join(value2))
                    notfound = 1  # Set notfound to 1 to indicate the movie is found
        if notfound == 1:
            break
        else:
            choice1 = input('Please provide correct movie name to check?:')

# Check if the user wants to check information about a director
elif choice.lower().strip() == "director":
    choice2 = input('Which director do you want to check?:')
    movie_list = []
    cast_list = []
    cast_list_dic = {}
    cast_number = []
    while True: 
        # Loop through the movie dictionary to find movies directed by the specified director
        for key1, value1 in movie_dic.items():
            for key2, value2 in value1.items():
                for director_name in key2:
                    if director_name.lower().strip() == choice2.lower().strip():
                        movie_list.append(key1)
                        cast_list.extend(value2)
                        notfound = 1  # Set notfound to 1 to indicate the director is found
        if notfound == 1: 
            print(choice2,'has directed in \n ', ' , '.join(movie_list))
            for i in cast_list:
                cast_list_dic[i] = cast_list_dic.get(i,0) + 1
            for i, j in cast_list_dic.items():
                j = str(j)
                cast_number.append(i + '-' + j)
            print('\n He has worked together with these people: \n',' , '.join(cast_number))
            break
        else:
            choice2 = input('Please provide correct director name to check?:')

# Check if the user wants to compare two directors based on cast similarity
elif choice.lower().strip() == "comparison":
    print('Who do you want to compare?')
    
    movie_list1 = []
    cast_list1 = []
    cast_list_dic1 = {}
    cast_number1 = []
    
    # Get input for the first director
    while True:
        director1 = input('First name:')
        for key1, value1 in movie_dic.items():
                for key2, value2 in value1.items():
                    for director_name in key2:
                        if director_name.lower().strip() == director1.lower().strip():
                            movie_list1.append(key1)
                            cast_list1.extend(value2)
                            notfound = 2
        if notfound == 2:
            break
        print("Please provide the correct Name")   
        
    movie_list2 = []
    cast_list2 = []
    cast_list_dic2 = {}
    cast_number2 = []
    
    # Get input for the second director
    while True:
        director2 = input('Second name:')
        for key1, value1 in movie_dic.items():
                for key2, value2 in value1.items():
                    for director_name in key2:
                        if director_name.lower().strip() == director2.lower().strip():
                            movie_list2.append(key1)
                            cast_list2.extend(value2)
                            notfound = 3
        if notfound == 3:
             break
           
        print("Please provide the correct Name")
        
    print('\n',director1,'has directed in \n ', ' , '.join(movie_list1)) #displaying first director movie and cast list
    cast_set1 = set(cast_list1)
    for i in cast_list1:
        cast_list_dic1[i] = cast_list_dic1.get(i,0) + 1
    for i, j in cast_list_dic1.items():
        j = str(j)
        cast_number1.append(i + '-' + j)
    print('\n He has worked together with these people: \n ',' , '.join(cast_number1))

    print('\n',director2,'has directed in \n ', ' , '.join(movie_list2)) #displaying second director movie and cast list
    cast_set2 = set(cast_list2)
    for i in cast_list2:
        cast_list_dic2[i] = cast_list_dic2.get(i,0) + 1
    for i, j in cast_list_dic2.items():
        j = str(j)
        cast_number2.append(i + '-' + j)
    print('\n He has worked together with these people:\n ',' , '.join(cast_number2))
    
    # Calculate cosine similarity based on the cast lists of the two directors
    common_cast_set = cast_set1.union(cast_set2)  
    common_cast_list = list(common_cast_set)
    common_cast_dic1 = {}
    common_cast_dic2 = {}
    
    # Initialize dictionaries for the common cast lists
    for i in common_cast_list:
        common_cast_dic1[i] = 0
        common_cast_dic2[i] = 0
    
    # Update dictionaries with the frequency of each cast member
    common_cast_dic1.update(cast_list_dic1)
    common_cast_dic2.update(cast_list_dic2)
    
    A = list(common_cast_dic1.values())
    B = list(common_cast_dic2.values())
    
    # Calculate and print the cosine similarity score
    similarity = cosine_similarity(A, B)
    similarity= round(similarity,5)
    print('\n Based on that, they have a cosine similarity score of %s' % similarity)
else:
    print("please provide a valid input")

