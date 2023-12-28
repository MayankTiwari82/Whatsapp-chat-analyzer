import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns


st.sidebar.title("Whatsapp chat Analyser")

upload_file=st.sidebar.file_uploader("Chosse a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    #fetch unique users




    user_list=df['users'].unique().tolist()
    user_list.remove('gropu_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show analysis with respect to",user_list)


    if st.sidebar.button("Show Analysis"):
        num_message, words, num_media_message, link_media_message, link=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(num_media_message)

        with col4:
            st.header("Total link Media Messages")
            st.title(link_media_message)
        with col5:
            st.header("All shared links")
            st.title(link)


        #monthly-timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily-timeline
        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['date_only'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values,color='orange')
            st.pyplot(fig)


        #Heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig, ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #finding the busiest users in the group
        if selected_user=='Overall':
            st.title("Most busy users")
            x, new_df=helper.most_busy_user(df)
            fig, ax=plt.subplots()
            col1, col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    #wordcloud
    st.title("WordCloud")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    #most common words
    most_common_df=helper.most_common_words(selected_user,df)

    fig, ax=plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

