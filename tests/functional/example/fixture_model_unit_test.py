# seeds/upstream_model_1.csv
upstream_model_1 = """
id,name,some_date
1,Easton,1981-05-20T06:46:51
2,Lillian,1978-09-03T18:10:33
3,Jeremiah,1982-03-11T03:59:51
""".lstrip()

# seeds/upstream_model_2.csv
upstream_model_2 = """
id,favorite_color
1,red
2,green
3,blue
""".lstrip()

# seeds/expected.csv
expected = """
id,name,favorite_color
1,Easton,red
2,Lillian,green
3,Jeremiah,blue
""".lstrip()
