 # ----------------------------------LIBS -------------------------------------------------------------   
import streamlit as st
# st.set_page_config(  # Alternate names: setup_page, page, layout
# 	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
# 	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
# 	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
# 	page_icon=None,  # String, anything supported by st.image, or None.
# )


#basic
from PIL import Image
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')
import datetime as dt 


#utils
from utils import style
from utils import login

# multiple page apps
from mypages import historical_page
from mypages import build_model
from mypages import how_it_works


#config
st.set_page_config(page_title="Search Job", layout="wide")
#style.sidebarwidth()
#style.style_menu()
style.style_0()


 # ----------------------------------DEFS -------------------------------------------------------------   
def main():

 # ----------------------------------MENU -------------------------------------------------------------   
    #if login.check_password():

        #css design for all pages
        #style.style_0()
        #hide steamlit buttons
        #style.hidden_menu_and_footer()
        #hide steamlit buttons
        #sidebar width
        #style.sidebarwidth()


    with st.sidebar:
    
        style.sidebarwidth() 
        #image = Image.open('logo_orange_2.jpg')
        #image = Image.open('images/bix_logo.png')
        #st.image(image, use_column_width=True)

        n_sprites = option_menu('Menu',["How it works", "Build a model","Historical data"],
                            icons=['robot','book','bar-chart-fill'],
                            default_index=0, menu_icon="app-indicator",   #orientation='horizontal',
                            styles={
            "container": {"padding": "2!important", "background-color": "#ffffff"}, # ,"background-size": "cover","margin": "0px"},
            "nav-link": {"font-size": "12px", "text-align": "left", "--hover-color": "#eee","font-weight": "bold"}, #,"position": "relative","display": "inline"},
            "nav-link-selected": {"background-color": "#3843bf"},
            }) 

# ----------------------------------PAGES -------------------------------------------------------------     

    if n_sprites == "Historical data":
        historical_page.show_page({})
    
    if n_sprites == "Build a model":
        build_model.show_page({})

    if n_sprites == "How it works":
        how_it_works.show_page({})

    # else:
    #     st.write('Entre com a senha')
        
if __name__ == '__main__':
    main()

