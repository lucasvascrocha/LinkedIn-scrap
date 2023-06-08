import streamlit as st

def show_page(params):

    # def embed_google_slides(url):
    #     embed_url = url + "&rm=minimal"
    #     st.components.v1.iframe(embed_url, height=600)

    # # Exemplo de uso
    # #url_do_slide = "https://docs.google.com/presentation/d/1SBYkodzx5rXOCOg_3JZPRL3LGQeBKAP5/edit?usp=sharing&ouid=105497879988811146259&rtpof=true&sd=true"
    # url_do_slide = "https://drive.google.com/file/d/15LseFTNFd9ab2PRvZ9Ogh5ayYlELSHWh/view?usp=sharing"
    
    # embed_google_slides(url_do_slide)

    def embed_google_drive_pdf(file_id):
        #url = f"https://drive.google.com/file/d/{file_id}/preview"
        url = f"https://drive.google.com/file/d/{file_id}/preview?embedded=true"

        st.components.v1.iframe(url, height=600)

    # Exemplo de uso
    pdf_file_id = "15LseFTNFd9ab2PRvZ9Ogh5ayYlELSHWh"
    embed_google_drive_pdf(pdf_file_id)