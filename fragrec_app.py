import os
import streamlit as st
# from streamlit import HTML

from frag_recommender import get_fragrecs

def app():
    
    # Add CSS styles
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f7f7f7;
        }
        .sidebar .sidebar-content .block-container {
            padding: 2rem;
        }
        
        </style>
        """
        
        """
        <style>
        #fragrance-table {
            width: 100%;
            margin-top: 2rem;
            border-collapse: collapse;
        }
        #fragrance-table th,
        #fragrance-table td {
            padding: 0.5rem;
            text-align: left;
            border: 1px solid #ddd;
        }
        #fragrance-table th {
            background-color: #f7f7f7;
        }
        </style>
        """
        ,
        unsafe_allow_html=True
    )

    # Define HTML template for the sidebar menu
    sidebar_menu = """
        <div class="sidebar-item">
            <a href="#">Fragrance Recommendations</a>
        </div>

    """


    
    # Define HTML template for the header
    header_template = """
        <div style="background-color: #5C2D91; padding: 2rem;">
            <h1 style="color: white; text-align: center;">Fragrance Recommendations</h1>
        </div>
    """

    st.markdown(header_template, unsafe_allow_html=True)

    
    
#     st.title('Fragrance Recommendations')
#     st.markdown("Enter the user's profile and what you are looking for in a fragrance.")
    
#     all_inputs = []
    
    with st.sidebar:
        st.markdown(sidebar_menu, unsafe_allow_html=True)
        
        st.markdown(
        """
        <style>
            div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
                font-size: 20px;
            }
            div[class*="stTextInput"] > label > div[data-testid="stMarkdownContainer"] > p {
                font-size: 20px;
            }
        </style>
        """
            , unsafe_allow_html=True)

        st.radio(
            "What gender is the fragrance targeted at?",
            ('Female', 'Male', 'Unisex'),
            key='gender'
        )
        st.radio(
            "What's the age range?",
            ('14-18', '19-24', '25-34', '35-44', '45-60', '60+'),
            key='age'
        )
        st.radio(
            "What season/temperature is it more suited for?",
            ('Hot', 'Cold', 'Year-Round'),
            key='weather'
        )
        st.radio(
            "What time of the day is it for?",
            ('Day', 'Night', 'Any'),
            key='time_of_day'
        )
        st.radio(
            "What type of occasion is it for?",
            ('Office', 'Date', 'Bar or Club', 'Special Occasion', 'Any'),
            key='occasion'
        )
        st.radio(
            "Do you want a popular fragrance that everyone likes or a unique fragrance that sets the wearer apart?",
            ('Popular', 'Unique', 'Irrelevant'),
            key='popularity'
        )

    #     min_price = 
    #     max_price = 

        st.text_input('\nPlease explain in words what else you are looking for in a fragrance:', max_chars=1400, key='comments')
        st.text_input('\nDo you know any fragrance that is similar to what you are looking for but not quite?', max_chars=100, key='similar_frags')
        st.checkbox('Include rare fragrances in search.', key='rarity')

    
#     depth = st.number_input('Min_depth', 0, 10000, step = 500, value=5000)
#     gradient = st.number_input('Min gradient', 0., 0.1, value=0.01, step=0.005, format='%0.3f')
    
#     st.write(f'Looking for a depth greater than {depth} and gradient greater than {gradient}.')
    
    recs = get_fragrecs(st.session_state)
    
    st.table(recs)


if __name__ == '__main__':
    app()