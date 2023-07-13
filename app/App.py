 # ----------------------------------LIBS -------------------------------------------------------------   
import streamlit as st
import hydralit_components as hc

# st.set_page_config(  # Alternate names: setup_page, page, layout
# 	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
# 	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
# 	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
# 	page_icon=None,  # String, anything supported by st.image, or None.
# )

#basic
from PIL import Image
import warnings
warnings.filterwarnings('ignore')
import datetime as dt 

# support
from collections import OrderedDict

#utils
from utils import style
#from utils import login

# multiple page apps
from mypages import how_it_works
from mypages import build_model
from mypages import historical_page


#config
st.set_page_config(page_title="Job Searcher", layout="wide")
style.style_menu()
style.style_0()


def main():

 # ----------------------------------MENU -------------------------------------------------------------   
        
    # style
    over_theme = {'menu_background': '#3843bf'}

    font_fmt = {'font-class':'h2','font-size':'150%'}

    main_menu_items = OrderedDict()
    main_menu_items["How it works"] = how_it_works
    #main_menu_items["Build a model"] = build_model
    main_menu_items["Historical data"] = historical_page

    chart_menu = []
    for item_name in main_menu_items:
        chart_menu.append({'icon': "far fa-chart-bar", 'label': item_name})
    
    menu_id = hc.nav_bar(
        key="TopMenu",
        menu_definition=chart_menu,
        home_name=None,
        hide_streamlit_markers=True,
        override_theme=over_theme
    )

    selected_page = main_menu_items[menu_id]
    selected_page.show_page({})
        
if __name__ == '__main__':
    main()

