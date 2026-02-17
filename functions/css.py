custom_css = """
<style>
.stMainBlockContainer{
    padding-top: 50px;
}

.st-emotion-cache-198znwi hr {
    margin-top: -5px;
    margin-bottom: 25px;
    }
</style>

"""

# .stMainBlockContainer
# main container

# .st-emotion-cache-198znwi hr
# CSS for streamlit divider elmement
# st-emotion-cache-1nbl5uk - if not coloured

###############################################################################

footer_css = """
<style>

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: rgb(247, 163, 78);
    text-align: center;
    padding: 10px 0;
    z-index: 999;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
}

.footer a {
    color: rgb(46, 46, 46);
    text-decoration: none;
    display: flex;
    align-items: center;

}

.footer a:hover {
    text-decoration: underline;
    color: rgb(255, 197, 138);
}

</style>

<div class="footer">
    <a href="https://github.com/ajhenne/chat2playlist" target="_blank">GitHub</a>
    <a href="https://www.linkedin.com/in/ajhennessy/" target="_blank">LinkedIn</a>
    <a href="./?v=privacy" target="_blank">Privacy Statement</a>
</div>
"""

###############################################################################

dialog_css = """
<style>
.stDialog {
    background-color: rgba(255, 255, 255, 0);
}
</style>"""