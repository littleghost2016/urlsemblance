from main import Relate


left = 'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_14708660642074285655%22%7D&n_type=0&p_from=1'
right = 'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_8827170254307770850%22%7D&n_type=0&p_from=4'
semblance = Relate(Left_URL=left, Right_URL=right).main_run()
print(semblance)