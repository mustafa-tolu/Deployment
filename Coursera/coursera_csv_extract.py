import streamlit as st
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

from random import randint
from time import sleep



html_temp = """
<div style="background-color:rgba(50, 155, 20, 0.3)">
<h1 style="color:white;text-align:center;">  Coursera - Courses List Extraction as CSV file </h1>
</div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)
st.write("\n\n")
st.subheader('When scraping is finished, you can download CSV file')


#sidebar
html_temp2 = """
<div style="background-color:rgba(0, 255, 0, 0.3)">
<h1 style="color:white;text-align:center;">  Coursera Courses by Categories </h1>
</div><br>"""
st.sidebar.markdown(html_temp2, unsafe_allow_html=True)
st.sidebar.subheader("Select a category to create courses list about it")



course_category = st.sidebar.radio("Categories", ("Data Science", "Business", "Computer Science", "Information Technology", "Language Learning", "Health", "Personal Development", "Physical Science and Engineering", "Social Sciences", "Arts and Humanities", "Math and Logic"))

# DataScience Business ComputerScience InformationTechnology LanguageLearning
# Health PersonalDevelopment PhysicalScienceEngineering
# SocialSciences ArtsHumanities MathLogic

def home(request):
    return HttpResponse('''
        <strong><p>Warning! Please wait a few seconds after clicking. When scraping is finished, you can download CSV file</strong>
        <ul>
            <li><a href='/data-science'>Data Science</a></li>
            <li><a href='/business'>Business</a></li>
            <li><a href='/computer-science'>Computer Science</a></li>
            <li><a href='/information-technology'>Information Technology</a></li>
            <li><a href='/language-learning'>Language Learning</a></li>
            <li><a href='/health'>Health</a></li>
            <li><a href='/personal-development'>Personal Development</a></li>
            <li><a href='/physical-science-and-engineering'>Physical Science and Engineering</a></li>
            <li><a href='/social-sciences'>Social Sciences</a></li>
            <li><a href='/arts-and-humanities'>Arts and Humanities</a></li>
            <li><a href='/math-and-logic'>Math and Logic</a></li>
        </ul>
    ''')

def get_data_from_url(target_url):
    response_data = requests.get(target_url)
    return BeautifulSoup(response_data.text, 'html.parser')

def get_data(request, category):
# Get data from /browse + category
    course_soup = get_data_from_url('https://www.coursera.org/browse/' + category)
    
    for url in course_soup.find_all('a', attrs={'class':'CardText-link'}):
        # To select courses, find urls starts with "learn"
        if url['href'].startswith('/learn'):
            # In Courses:
            course_data = get_data_from_url('https://www.coursera.org' + url['href'])
            
            # Scrap required data from courses
            CourseName = course_data.find('h1', attrs={'class':'banner-title banner-title-without--subtitle m-b-0'}).text
            CourseProvider = course_data.find('h3', attrs={'class':'headline-4-text bold rc-Partner__title'}).text
            # Sleep a random number of seconds (between 1 and 5)
            sleep(randint(1, 5))
            CourseDescription = course_data.find('div', attrs={'class':'content-inner'}).find('p').text
            StudentsEnrolled = course_data.find('div', attrs={'class':'_1fpiay2'}).find('span').text
            Ratings = course_data.find('span', attrs={'data-test':'number-star-rating'}).text

            CourseList, ProviderList, DescriptionList, EnrolledList, RatingsList = [],[],[],[],[]

            for i,j,k,l,m in zip(CourseName, CourseProvider, CourseDescription, StudentsEnrolled, Ratings):
                CourseList.append(i)
                ProviderList.append(j)
                DescriptionList.append(k)
                EnrolledList.append(l)
                RatingsList.append(m)

            courses = pd.DataFrame({
                'Course Name': CourseList,
                'Course Provider': ProviderList,
                'Course Description': DescriptionList,
                'Students Enrolled': EnrolledList,
                'Ratings': RatingsList
            })

            
    
    return courses.to_csv((category + ".csv"), encoding='LATIN-1', index=False)


if st.button("Extract"):
    st.write("CSV file is extracting.")
    get_data(request, category)
    with st.spinner('Wait for extraction...'):
        time.sleep(7)
    st.success('CSV file is ready!')
    st.table(courses)
    st.download_button('Download CSV', courses, (category + ".csv"), 'text/csv')
    button_style = """
        <style>
        .stdownload_button > button {
            color: green;
            background: gray;
            width: 100px;
            height: 100px;
            font-size: 25px;
        }
        </style>
        """
    st.markdown(button_style, unsafe_allow_html=True)


st.write("\n\n")