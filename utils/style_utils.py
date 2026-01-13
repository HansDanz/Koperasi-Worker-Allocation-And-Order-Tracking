import streamlit as st
import streamlit.components.v1 as components

def render_tailwind(html_content, height=200):
    """
    Renders HTML content with Tailwind CSS enabled using a Streamlit component (iframe).
    """
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="p-4">
        {html_content}
    </body>
    </html>
    """
    components.html(full_html, height=height, scrolling=False)
