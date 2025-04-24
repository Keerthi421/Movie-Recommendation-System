import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import preprocess
from processing.display import Main

# Setting the wide mode as default
st.set_page_config(layout="wide")

# Live starfield animated background
starfield_css = """
<style>
body {
    margin: 0;
    padding: 0;
    overflow: hidden;
}
.stApp {
    background: transparent;
}
#starfield {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #1e1e2f 0%, #11121a 100%);
    background-image:
        radial-gradient(2px 2px at 20% 20%, #fff, transparent),
        radial-gradient(2px 2px at 40% 60%, #fff, transparent),
        radial-gradient(2px 2px at 65% 40%, #fff, transparent),
        radial-gradient(2px 2px at 80% 80%, #fff, transparent),
        radial-gradient(1px 1px at 100px 200px, #fff, transparent);
    background-size: 200px 200px;
    animation: starAnim 200s linear infinite;
    z-index: -1;
}
@keyframes starAnim {
    from {background-position: 0 0;}
    to {background-position: -200px -200px;}
}
</style>
<div id="starfield"></div>
"""
st.markdown(starfield_css, unsafe_allow_html=True)

# Custom CSS for hover effect
hover_css = """
<style>
div[data-testid*='stButton'] > button:hover {
    background-color: #f63366; /* Primary color from theme */
    color: white;
    border-color: #f63366;
}
div[data-testid*='stButton'] > button {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>
"""
st.markdown(hover_css, unsafe_allow_html=True)

# Improve UI: card backgrounds, spacing, and typography
ui_css = """
<style>
/* Style the main app container as a semi-transparent card */
section.main > div[data-testid="main-container"] {
    background: rgba(30, 30, 40, 0.8);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem auto;
    max-width: 1200px;
}

/* Center and enlarge the page title */
h1 {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 2rem;
}

/* Style the horizontal menu bar as a card */
div[data-testid="stHorizontalBlock"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

/* Increase selectbox and button sizes */
div[data-baseweb="select"] {
    width: 100%;
    max-width: 400px;
    margin: 0 auto 1rem;
}
div[data-testid*='stButton'] > button {
    font-size: 1.1rem;
    padding: 0.75rem 1.5rem;
    margin: 0 auto;
    display: block;
}

/* Style movie recommendation grid with spacing */
.stImage {
    padding: 1rem;
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    margin: 0.5rem;
}
</style>
"""
st.markdown(ui_css, unsafe_allow_html=True)

displayed = []

if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""


def main():
    # Home page hero section
    if st.session_state['user_menu'] == "":
        st.markdown(
            """
            <div style='text-align:center; margin-top:4rem;'>
                <h1>Welcome to Movie Recommender 🎬</h1>
                <p style='font-size:1.2rem;'>Get your personalized recommendations in one click.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # 'Get Your Recommendation Now' button
        if st.button('Get Your Recommendation Now'):
            st.session_state['user_menu'] = 'Recommend me a similar movie'
        return

    def initial_options():
        # To display menu
        st.session_state.user_menu = streamlit_option_menu.option_menu(
            menu_title='What are you looking for? 👀',
            options=['Recommend me a similar movie', 'Describe me a movie', 'Check all Movies'],
            icons=['film', 'film', 'film'],
            menu_icon='list',
            orientation="horizontal",
        )

        if st.session_state.user_menu == 'Recommend me a similar movie':
            recommend_display()

        elif st.session_state.user_menu == 'Describe me a movie':
            display_movie_details()

        elif st.session_state.user_menu == 'Check all Movies':
            paging_movies()

    def recommend_display():

        st.title('Movie Recommender System')

        selected_movie_name = st.selectbox(
            'Select a Movie...', new_df['title'].values
        )

        rec_button = st.button('Recommend')
        if rec_button:
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tags.pkl',"are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_genres.pkl',"on the basis of genres are")
            recommendation_tags(new_df, selected_movie_name,
                                r'Files/similarity_tags_tprduction_comp.pkl',"from the same production company are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_keywords.pkl',"on the basis of keywords are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tcast.pkl',"on the basis of cast are")

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path,str):

        movies, posters = preprocess.recommend(new_df, selected_movie_name, pickle_file_path)
        st.subheader(f'Best Recommendations {str}...')

        rec_movies = []
        rec_posters = []
        cnt = 0
        # Adding only 5 uniques recommendations
        for i, j in enumerate(movies):
            if cnt == 5:
                break
            if j not in displayed:
                rec_movies.append(j)
                rec_posters.append(posters[i])
                displayed.append(j)
                cnt += 1

        # Columns to display informations of movies i.e. movie title and movie poster
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(rec_movies[0])
            st.image(rec_posters[0])
        with col2:
            st.text(rec_movies[1])
            st.image(rec_posters[1])
        with col3:
            st.text(rec_movies[2])
            st.image(rec_posters[2])
        with col4:
            st.text(rec_movies[3])
            st.image(rec_posters[3])
        with col5:
            st.text(rec_movies[4])
            st.image(rec_posters[4])

    def display_movie_details():

        selected_movie_name = st.session_state.selected_movie_name
        # movie_id = movies[movies['title'] == selected_movie_name]['movie_id']
        info = preprocess.get_details(selected_movie_name)

        with st.container():
            image_col, text_col = st.columns((1, 2))
            with image_col:
                st.text('\n')
                st.image(info[0])

            with text_col:
                st.text('\n')
                st.text('\n')
                st.title(selected_movie_name)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Rating")
                    st.write(info[8])
                with col2:
                    st.text("No. of ratings")
                    st.write(info[9])
                with col3:
                    st.text("Runtime")
                    st.write(info[6])

                st.text('\n')
                st.write("Overview")
                st.write(info[3], wrapText=False)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Release Date")
                    st.text(info[4])
                with col2:
                    st.text("Budget")
                    st.text(info[1])
                with col3:
                    st.text("Revenue")
                    st.text(info[5])

                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    str = ""
                    st.text("Genres")
                    for i in info[2]:
                        str = str + i + " . "
                    st.write(str)

                with col2:
                    str = ""
                    st.text("Available in")
                    for i in info[13]:
                        str = str + i + " . "
                    st.write(str)
                with col3:
                    st.text("Directed by")
                    st.text(info[12][0])
                st.text('\n')

        # Displaying information of casts.
        st.header('Cast')
        cnt = 0
        urls = []
        bio = []
        for i in info[14]:
            if cnt == 5:
                break
            url, biography= preprocess.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt += 1

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(urls[0])
            # Toggle button to show information of cast.
            stoggle(
                "Show More",
                bio[0],
            )
        with col2:
            st.image(urls[1])
            stoggle(
                "Show More",
                bio[1],
            )
        with col3:
            st.image(urls[2])
            stoggle(
                "Show More",
                bio[2],
            )
        with col4:
            st.image(urls[3])
            stoggle(
                "Show More",
                bio[3],
            )
        with col5:
            st.image(urls[4])
            stoggle(
                "Show More",
                bio[4],
            )

    def paging_movies():
        # To create pages functionality using session state.
        max_pages = movies.shape[0] / 10
        max_pages = int(max_pages) - 1

        col1, col2, col3 = st.columns([1, 9, 1])

        with col1:
            st.text("Previous page")
            prev_btn = st.button("Prev")
            if prev_btn:
                if st.session_state['movie_number'] >= 10:
                    st.session_state['movie_number'] -= 10

        with col2:
            new_page_number = st.slider("Jump to page number", 0, max_pages, st.session_state['movie_number'] // 10)
            st.session_state['movie_number'] = new_page_number * 10

        with col3:
            st.text("Next page")
            next_btn = st.button("Next")
            if next_btn:
                if st.session_state['movie_number'] + 10 < len(movies):
                    st.session_state['movie_number'] += 10

        display_all_movies(st.session_state['movie_number'])

    def display_all_movies(start):

        i = start
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        st.session_state['page_number'] = i

    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options()


if __name__ == '__main__':
    main()

