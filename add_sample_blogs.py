from main import add_blog
# creates the sample blogs
if __name__ == "__main__":
    newblog = add_blog(
        username="yash_garg",
        blog_title="How to make a flask app",
        blog_content=" It is not possible to write front-end course every time user make changes in his/her profile. We use a template and it generates code according to the content. Flask is one of the web development frameworks written in Python. Through flask, a loop can be run in the HTML code using jinja template and automatically HTML code can be generated using this. The code will be stored in Directories in the format of Flask. So we will be making two directories",
    )
    print(newblog)
    newblog1 = add_blog(
    username="yash_garg",
    blog_title="Mastering Data Visualization with Matplotlib",
    blog_content="Data visualization is a crucial aspect of data analysis and interpretation. Matplotlib is a powerful Python library that enables users to create a wide variety of static, animated, and interactive visualizations. In this blog series, we will explore various techniques and best practices for mastering data visualization with Matplotlib. From basic plots to advanced customization, join us on a journey to unlock the full potential of data visualization."
    )
    print(newblog1)
    newblog2 = add_blog(
    username="yash_garg",
    blog_title="Building Scalable Web Applications with Django",
    blog_content="Django is a high-level Python web framework that promotes rapid development and clean, pragmatic design. In this series, we will delve into the process of building scalable web applications using Django. From setting up a project to deploying it to production, we'll cover essential concepts such as models, views, templates, forms, and authentication. Whether you're a beginner or an experienced developer, this series will equip you with the knowledge and skills to build robust web applications with Django."
    )
    print(newblog2)
    newblog3 = add_blog(
    username="yash_garg",
    blog_title="The Power of Machine Learning: An Introduction",
    blog_content="Machine learning is revolutionizing industries across the globe, from healthcare to finance to entertainment. In this introductory series, we'll demystify the concepts and algorithms behind machine learning. We'll explore supervised and unsupervised learning techniques, delve into popular algorithms such as linear regression and k-means clustering, and discuss real-world applications of machine learning. Whether you're a novice or a seasoned professional, this series will lay the groundwork for your journey into the fascinating world of machine learning."
    )
    print(newblog3)